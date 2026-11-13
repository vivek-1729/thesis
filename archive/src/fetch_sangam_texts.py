"""Acquire the Sangam poems and find which of them name our ports.

`DATA.md` lists the Tamil Sangam corpus as held "at second hand only", meaning
every Sangam reference in this project is quoted from a modern scholar rather
than read. That is the weakest link in the textual stream, because the Sangam
poems are the only indigenous body of text contemporary with the Periplus, and
what they do and do not name is evidence about the ports in its own right.

Project Madurai publishes the corpus in Tamil, public domain, as plain HTML. It
does not publish translations, and the standard English versions are in
copyright, so this does not remove the need to read a translation. What it does
give is the thing a translation cannot be searched for reliably: which poems
contain the port names, in the original, counted rather than recalled.

The index is a sortable table in Tamil script, so the works are matched on their
Tamil titles and the port names are searched in Tamil too.
"""
import csv, html, json, pathlib, re, subprocess, time

ROOT = pathlib.Path(__file__).resolve().parents[2]
DEST = ROOT / "library" / "sangam"
OUT = pathlib.Path(__file__).resolve().parents[1] / "data" / "processed"
BASE = "https://www.projectmadurai.org"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"

# The eight anthologies and ten songs, by their Tamil titles. Transliterations
# are given because the rest of this project is written in them.
WORKS = {
    "அகநானூறு": "Akananuru", "புறநானூறு": "Purananuru",
    "நற்றிணை": "Natrinai", "குறுந்தொகை": "Kurunthogai",
    "ஐங்குறுநூறு": "Ainkurunuru", "பதிற்றுப்பத்து": "Patirruppattu",
    "பரிபாடல": "Paripadal", "கலித்தொகை": "Kalittokai",
    "பட்டினப்பாலை": "Pattinappalai", "மதுரைக்காஞ்சி": "Maduraikkanci",
    "பெரும்பாணாற்றுப்படை": "Perumpanarruppatai",
    "பொருநராற்றுப்படை": "Porunararruppatai",
    "சிறுபாணாற்றுப்படை": "Cirupanarruppatai",
    "முல்லைப்பாட்டு": "Mullaippattu", "நெடுநல்வாடை": "Netunalvatai",
    "குறிஞ்சிப்பாட்டு": "Kurincippattu", "மலைபடுகடாம்": "Malaipatukatam",
    "திருமுருகாற்றுப்படை": "Tirumurukarruppatai",
    "சிலப்பதிகார": "Silappadikaram", "மணிமேகலை": "Manimekalai",
}

# What we are looking for, and whether a plain search for it means anything.
#
# Most of these words are not only place names. Searching the corpus for them
# and reporting the counts produces numbers that are mostly the common noun:
# naravu is toddy, and the commentaries gloss it as kal; vanci is an oath, a
# deceit, a creeper and a poetic genre before it is the Cera capital; pakai in
# this spelling turns up inside a poet's epithet, a sweet syrup and a headwrap.
# A first pass reported 57 occurrences of Naura and 313 of Vanci on that basis,
# which would have been wrong in the direction that looks like a finding.
#
# So each token carries whether its count can be read as a place. Only the
# reliable ones are totalled.
PORTS = {
    "முசிறி": ("Muciri (Muziris)", True,
               "unambiguous; the commentaries gloss it as the town of that name"),
    "தொண்டி": ("Tondi (Tyndis)", True,
               "a place name in these texts, though more than one Tondi exists"),
    "கொற்கை": ("Korkai", True, "the Pandya pearl port; unambiguous"),
    "நறவு": ("Naravu (Naura)", False,
             "also toddy, which is what nearly every occurrence is"),
    "வஞ்சி": ("Vanci (Cera capital)", False,
              "also an oath, a deceit, a creeper and a poetic genre"),
    "பாகை": ("Pakai (Bakarē)", False,
             "also a headwrap and a syrup, and part of a poet's epithet"),
    "யவன": ("Yavana (western foreigner)", True,
             "a people rather than a port, and the one word that bears on all of them"),
    "நெல்கிண்ட": ("Nelkinda (Nelkynda)", True, "absent from the corpus"),
}

def index():
    DEST.mkdir(parents=True, exist_ok=True)
    p = DEST / "pmworks.html"
    if not p.exists():
        subprocess.run(["curl", "-sL", "-A", UA, "--max-time", "120",
                        "-o", str(p), f"{BASE}/pmworks.html"], check=True)
    return p.read_text(encoding="utf-8", errors="ignore")


def rows(idx):
    """Work number, title, author and the Unicode HTML link, per table row."""
    out = []
    for tr in re.findall(r"<tr>(.*?)</tr>", idx, re.S):
        tds = re.findall(r"<td>(.*?)</td>", tr, re.S)
        if len(tds) < 6:
            continue
        title = html.unescape(re.sub(r"<[^>]+>", "", tds[1])).strip()
        link = re.search(r'href="([^"]*utf8/[^"]+\.html)"', tds[5])
        if not link:
            continue
        out.append({"no": re.sub(r"<[^>]+>", "", tds[0]).strip(),
                    "title": title,
                    "author": html.unescape(re.sub(r"<[^>]+>", "", tds[2])).strip(),
                    "href": link.group(1)})
    return out


def main():
    idx = index()
    all_rows = rows(idx)
    wanted = []
    for r in all_rows:
        for ta, en in WORKS.items():
            if ta in r["title"]:
                wanted.append({**r, "work": en})
                break
    print(f"{len(all_rows)} works in the index, {len(wanted)} are Sangam-corpus texts\n")

    hits, got = [], 0
    for r in wanted:
        p = DEST / f"{r['work']}_{r['no']}.html"
        if not p.exists() or p.stat().st_size < 2000:
            subprocess.run(["curl", "-sL", "-A", UA, "--max-time", "120",
                            "-o", str(p), BASE + r["href"]], capture_output=True)
            time.sleep(0.8)
        if not p.exists() or p.stat().st_size < 2000:
            print(f"  -- failed  {r['work']} ({r['title'][:30]})")
            continue
        got += 1
        t = p.read_text(encoding="utf-8", errors="ignore")
        t = re.sub(r"<[^>]+>", " ", t)
        counts = {v[0]: len(re.findall(ta, t)) for ta, v in PORTS.items()}
        named = {k: v for k, v in counts.items() if v}
        hits.append({"work": r["work"], "title": r["title"], "no": r["no"],
                     "file": p.name, "chars": len(t), **counts})
        reliable = {v[0] for v in PORTS.values() if v[1]}
        named = {k: v for k, v in named.items() if k in reliable}
        if named:
            print(f"  {r['work']:22s} " +
                  ", ".join(f"{k.split()[0]} {v}" for k, v in named.items()))

    dest = OUT / "sangam_port_mentions.csv"
    if hits:
        with open(dest, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(hits[0]))
            w.writeheader(); w.writerows(hits)
    print(f"\n{got} texts held in library/sangam -> {dest.name}")
    print("\n   countable:")
    for name, ok, why in PORTS.values():
        if not ok:
            continue
        tot = sum(h.get(name, 0) for h in hits)
        works = sum(1 for h in hits if h.get(name, 0))
        print(f"     {name:34s} {tot:4d} occurrences in {works} texts")
    print("\n   not countable, because the word is also an ordinary one:")
    for name, ok, why in PORTS.values():
        if ok:
            continue
        print(f"     {name:34s} {why}")


if __name__ == "__main__":
    main()

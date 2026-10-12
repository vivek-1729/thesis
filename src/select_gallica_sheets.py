"""Choose which of the 915 catalogued Gallica sheets are worth downloading.

Taking all of them is about five gigabytes and most would never be opened. The
Malabar block in particular is dominated by Bombay, Goa, Surat and Mahé, which
are 400 to 1,000 km north of any port this thesis is about, because the
catalogue harvest matched on the word Malabar and the Malabar coast of the
charts is longer than the Malabar coast of the Periplus.

So the unit of selection is the place name. A sheet is kept when its title names
somewhere near a candidate, under whatever spelling the chartmakers used, or
when it advertises soundings on one of our coasts, since depth is the one thing
no modern source supplies for these approaches.

Writes a selection rather than downloading, so the list can be read before five
gigabytes are committed to.
"""
import csv, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[2]
CAT = ROOT / "library" / "charts-gallica" / "catalogue.csv"
OUT = pathlib.Path(__file__).resolve().parents[1] / "data" / "processed"

# Old chart spellings, which are various. Cranganore alone appears as Cranganor,
# Crangano and Cranganore, and Kollam appears as Coylang, Coylan and Quilon.
#
# Every alternative is bounded, because the short ones are substrings of
# ordinary words and of ships. Unbounded, "quilon" matches the French frigate
# l'Aquilon and pulled in three surveys of the Gulf of Ajaccio.
PLACES = {
    "Muziris": r"\b(?:crangano|cranganor|cranganore|kodungallur|paravur|aycotta|"
               r"chetwai|chettuva)\b",
    "Muziris and Nelkynda": r"\b(?:cochin|cochain|cochim|cochim|vypin|vaipin)\b",
    "Tyndis": r"\b(?:calicut|callecut|calecut|ponnani|ponany|beypore|beypour|"
              r"kadalundi|tanor|tannore|chaliyam|mont d.?el[yi]|tellicherry|"
              r"tellichery|mah[ée]|billiapattam|durmapatam|cananor|cannanore)\b",
    "Nelkynda and Bakarē": r"\b(?:coylang|coylan|quilon|coulan|porcad|porca|"
                           r"purakkad|alleppey|alepey|anjengo|travancou?re?|"
                           r"niranam|kayamkulam|cap[e]? comorin|comaroone)\b",
    "Barbarikon": r"\b(?:indus|sind[eh]?|scinde|karachi|kurrachee|guadar|gwadar|"
                  r"mekran|makran|kutch|cutch|cambaye|diul|lahori)\b",
    # Deliberately narrow. "mer rouge" and "arabie" alone return 234 sheets,
    # two thirds of the whole selection, for the one coast the water record
    # shows has not moved: Aynuna is 209 of 210 km2 permanent water and 0.1 per
    # cent lost since 1984. So this keeps the northern Hijaz and the Gulf of
    # Aqaba, which is the Leukē Kōmē neighbourhood, and lets the general Red Sea
    # charts through only when they carry soundings.
    "Leukē Kōmē": r"aqaba|akaba|moilah|mouilah|mowilah|wedj|wejh|yambo|yanbu|"
                  r"midian|midyan|hedjaz|hejaz|sherm|dsjedda|tiran|"
                  r"golfe arabique|mer rouge.{0,40}(nord|septentrional)",
    "Rhapta": r"\b(?:zanzibar|zanguebar|zinzibar|mombas|quiloa|kilwa|mafia|"
              r"rufiji|pemba|melinde|malindi|dar es|mozambique|delgad)\w*",
}

# Two names that read as places on these coasts and are not. Cochinchina is in
# Vietnam and accounts for nineteen sheets on its own, and Noel Cochin was an
# engraver whose signature sits in the title of every plate he cut, including
# sieges in Lorraine and Catalonia.
NOT_A_PLACE = (r"cochin[\s-]?chin|\bcochin china|(?:n\.|noel)\s+cochin|"
               # One Gallica title truncates Cochinchina to "Cochin", so the
               # Vietnamese ports on the same sheet are what identifies it.
               r"xum day|vung l|pulo |nha shang|cape varelle|turon|tonquin")

# Depth is the scarce quantity, so a sheet advertising soundings earns its place
# whatever it is named. See GEOGRAPHIC-FINDINGS section 9.
SOUNDINGS = r"sonde|soundings|brasse|fathom|bancs? de sable|mud bank"

# What the chart cannot be about and still be relevant. These are the northern
# Konkan and Gujarat places that dominate the "malabar" harvest.
AWAY = (r"bombay|bomba[ÿy]|goa\b|surat|surrate|carwar|karwar|chaul|choul|"
        r"geriah|gyria|vizendruk|iz-?druk|angria|rajapour|rajapuri|dabul|"
        r"salset|salcette|trombay|bassein|basseen|demaon|daman|bulsaur|gundivee|"
        r"nunsaree|danno|angassea|belapore|bancoot|vingorla|merjee|onore|onor|"
        r"comptee|mayham|vassava|varsavah|gujarat|guzarat|guzerat|coromandel|"
        r"bengal|ceylan|ceylon|madras|madur|laquedives|laccadives|maldives")


def year(d):
    m = re.search(r"\b(1[3-9]\d{2})\b", d or "")
    return int(m.group(1)) if m else None


def classify(r):
    t = (r["title"] or "")
    if re.search(NOT_A_PLACE, t, re.I):
        return [], False, False, False
    hits = [p for p, pat in PLACES.items() if re.search(pat, t, re.I)]
    sounds = bool(re.search(SOUNDINGS, t, re.I))
    away = bool(re.search(AWAY, t, re.I))
    # A sheet naming one of our places keeps it even if it also names a far one,
    # since a coastal run from Goa to Cochin still covers Cochin.
    keep = bool(hits) or (sounds and not away)
    return hits, sounds, away, keep


def main():
    rows = list(csv.DictReader(open(CAT)))
    out = []
    for r in rows:
        hits, sounds, away, keep = classify(r)
        if not keep:
            continue
        out.append({
            "ports": "; ".join(hits), "soundings": "Y" if sounds else "",
            "also_distant": "Y" if away else "",
            "year": year(r["date"]) or "", "date": r["date"],
            "region": r["region"], "ark": r["ark"],
            "title": r["title"], "url": r["url"],
        })
    # Earliest first: an earlier survey tightens the bound on how far the coast
    # has moved, which is the whole reason for wanting these.
    out.sort(key=lambda d: (d["year"] or 9999))
    dest = OUT / "gallica_selection.csv"
    with open(dest, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]))
        w.writeheader(); w.writerows(out)

    from collections import Counter
    print(f"{len(out)} of {len(rows)} sheets selected -> {dest.name}\n")
    c = Counter(p for d in out for p in (d["ports"].split("; ") if d["ports"] else ["(soundings only)"]))
    for k, v in c.most_common():
        print(f"   {k:24s} {v}")
    pre1800 = sum(1 for d in out if d["year"] and d["year"] < 1800)
    print(f"\n   {pre1800} dated before 1800, "
          f"{sum(1 for d in out if d['soundings'] == 'Y')} advertise soundings")


if __name__ == "__main__":
    main()

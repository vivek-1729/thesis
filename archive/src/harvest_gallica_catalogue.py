"""Full metadata catalogue of Gallica maps covering our four coasts.

Metadata first, images second. There are several hundred sheets across the four
searches and at 50 to 95 megapixels each they would run to tens of gigabytes, so
this builds the catalogue and a later pass pulls only what is worth having.
"""
import csv, html, pathlib, re, time, urllib.parse, urllib.request

OUT = pathlib.Path(__file__).resolve().parents[2] / "library" / "charts-gallica"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

QUERIES = {
    "malabar":  'gallica all "Malabar" and dc.type all "carte"',
    "cochin":   'gallica all "Cochin" and dc.type all "carte"',
    "coromandel-malabar": 'gallica all "cote de Malabar" and dc.type all "carte"',
    "indus":    'gallica all "Indus" and dc.type all "carte"',
    "sind":     'gallica all "Scinde" and dc.type all "carte"',
    "redsea":   'gallica all "mer Rouge" and dc.type all "carte"',
    "arabia":   'gallica all "Arabie" and dc.type all "carte"',
    "zanzibar": 'gallica all "Zanzibar" and dc.type all "carte"',
    "zanguebar":'gallica all "Zanguebar" and dc.type all "carte"',
}


def page(query, start, n=50):
    u = ("https://gallica.bnf.fr/SRU?operation=searchRetrieve&version=1.2"
         f"&maximumRecords={n}&startRecord={start}&query=" + urllib.parse.quote(query))
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=90
                                  ).read().decode("utf-8", "ignore")


def parse(x):
    out = []
    for r in re.split(r"<srw:record>", x)[1:]:
        def one(tag):
            m = re.findall(rf"<dc:{tag}>(.*?)</dc:{tag}>", r, re.S)
            return html.unescape(" ".join(m[0].split())) if m else ""
        ident = re.findall(r"<dc:identifier>(https?://gallica[^<]+)</dc:identifier>", r)
        if not ident:
            continue
        out.append({"ark": ident[0].rstrip("/").split("/")[-1],
                    "title": one("title")[:300], "date": one("date"),
                    "creator": one("creator")[:120], "publisher": one("publisher")[:120],
                    "url": ident[0]})
    return out


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    rows, seen = [], set()
    for region, q in QUERIES.items():
        start, total = 1, None
        while True:
            try:
                x = page(q, start)
            except Exception as e:
                print(f"  {region} start={start} failed: {type(e).__name__}")
                break
            if total is None:
                m = re.search(r"<srw:numberOfRecords>(\d+)", x)
                total = int(m.group(1)) if m else 0
                print(f"{region:20s} {total} records")
            got = parse(x)
            if not got:
                break
            for g in got:
                if g["ark"] in seen:
                    continue
                seen.add(g["ark"])
                g["region"] = region
                rows.append(g)
            start += len(got)
            if start > min(total, 400):
                break
            time.sleep(0.7)

    dest = OUT / "catalogue.csv"
    with open(dest, "w", newline="") as f:
        w = csv.DictWriter(f, ["region", "ark", "date", "title", "creator", "publisher", "url"])
        w.writeheader()
        w.writerows(rows)
    print(f"\n{len(rows)} unique sheets -> {dest}")

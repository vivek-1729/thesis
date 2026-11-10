"""Download the Rumsey sheets the catalogue already found.

`harvest_rumsey.py` catalogued 49 sheets across the four coasts and fetched
none of them. The media URLs in that catalogue are direct, so this is a plain
download; the only care needed is that Rumsey serves several sizes and the
catalogue recorded Size4, which is a working resolution rather than the
largest. Anything that later needs georeferencing can be re-pulled at full size
through IIIF, which is why the sheet id is kept in the index.
"""
import csv, json, pathlib, re, subprocess, time

ROOT = pathlib.Path(__file__).resolve().parents[2]
DEST = ROOT / "library" / "charts-rumsey"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")


def slug(r):
    t = re.sub(r"[^A-Za-z0-9]+", "-", r["title"] or "untitled")[:70].strip("-")
    d = re.sub(r"[^0-9]", "", r.get("date") or "")[:4]
    return f"{re.sub(r'[^a-z0-9]+','-',r['term'].lower()).strip('-')}_{d or 'nd'}_{t}.jpg"


def main():
    rows = list(csv.DictReader(open(DEST / "catalogue.csv")))
    print(f"{len(rows)} catalogued sheets\n")
    index, ok, skip, fail = [], 0, 0, 0
    for r in rows:
        url = r.get("url")
        if not url:
            fail += 1
            continue
        p = DEST / slug(r)
        if p.exists() and p.stat().st_size > 50000:
            skip += 1
        else:
            subprocess.run(["curl", "-sL", "-A", UA, "--max-time", "180",
                            "-o", str(p), url], capture_output=True)
            if not p.exists() or p.stat().st_size < 50000:
                p.unlink(missing_ok=True)
                fail += 1
                print(f"  -- failed  {r['title'][:66]}", flush=True)
                continue
            ok += 1
            print(f"  OK {p.stat().st_size//1024:>6}KB  {p.name[:76]}", flush=True)
            time.sleep(0.4)
        index.append({"file": p.name, "term": r["term"], "id": r["id"],
                      "date": r.get("date", ""), "title": r["title"],
                      "detail": r.get("link", "")})
    (DEST / "index.json").write_text(json.dumps(index, indent=1, ensure_ascii=False))
    mb = sum((DEST / i["file"]).stat().st_size for i in index) / 1e6
    print(f"\ndownloaded {ok}, already held {skip}, failed {fail}  ({mb:.0f} MB)")


if __name__ == "__main__":
    main()

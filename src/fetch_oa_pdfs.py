"""Download the open-access PDFs the sweep turned up, and index them.

Only on-topic works with a resolvable PDF are fetched. Everything else is left
for the acquisition list, since a paywalled DOI is a request to the library,
not a failure of the script.
"""
import csv, re, pathlib, urllib.request, time

ROOT = pathlib.Path(__file__).resolve().parents[2]
DEST = ROOT / "library" / "oa-harvest"
D = pathlib.Path(__file__).resolve().parents[1] / "data" / "processed"
UA = {"User-Agent": "Mozilla/5.0 (thesis-research; mailto:vivekshah@college.harvard.edu)"}

def slug(r):
    a = (r["authors"].split(",")[0] or "anon").strip() or "anon"
    t = re.sub(r"[^A-Za-z0-9]+", "-", r["title"])[:60].strip("-")
    return re.sub(r"[^A-Za-z0-9-]", "", f"{r['port'].replace(' ','')}_{a}{r['year']}_{t}")[:120] + ".pdf"

def main():
    DEST.mkdir(parents=True, exist_ok=True)
    rows = [r for r in csv.DictReader(open(D / "literature_candidates.csv"))
            if r.get("on_topic") == "Y" and r["is_oa"] == "Y" and r["oa_pdf"]
            and r.get("strand") in ("archaeology", "palaeoenvironment", "both")]
    print(f"{len(rows)} open-access on-topic PDFs to try\n")
    ok = fail = skip = 0
    log = []
    for r in rows:
        p = DEST / slug(r)
        if p.exists() and p.stat().st_size > 20000:
            skip += 1; continue
        try:
            req = urllib.request.Request(r["oa_pdf"], headers=UA)
            b = urllib.request.urlopen(req, timeout=90).read()
            if not b.startswith(b"%PDF") or len(b) < 20000:
                fail += 1; log.append((r, "not a PDF")); continue
            p.write_bytes(b); ok += 1
            print(f"  OK {len(b)//1024:>6}KB  {p.name[:76]}", flush=True)
        except Exception as e:
            fail += 1; log.append((r, str(e)[:40]))
        time.sleep(0.5)
    print(f"\ndownloaded {ok}, already held {skip}, failed {fail}")
    with open(D / "oa_harvest_log.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["port", "year", "title", "doi", "reason"])
        for r, why in log:
            w.writerow([r["port"], r["year"], r["title"], r["doi"], why])

if __name__ == "__main__":
    main()

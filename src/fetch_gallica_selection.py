"""Download the Gallica sheets that `select_gallica_sheets.py` chose.

Gallica serves IIIF, so a sheet comes down as one image at whatever size is
asked for. `full/full` gives the scan at native resolution, which runs from
about 50 to 95 megapixels and six megabytes a sheet. That is the size worth
keeping, because the thing these charts are wanted for is the soundings printed
along the approach, and those do not survive downsampling.
"""
import csv, json, pathlib, subprocess, re, time

ROOT = pathlib.Path(__file__).resolve().parents[2]
DEST = ROOT / "library" / "charts-gallica"
SEL = pathlib.Path(__file__).resolve().parents[1] / "data" / "processed" / "gallica_selection.csv"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
IIIF = "https://gallica.bnf.fr/iiif/ark:/12148/{ark}/f1/full/full/0/native.jpg"


def slug(r):
    port = re.sub(r"[^a-z]+", "-", (r["ports"].split(";")[0] or r["region"]).lower()).strip("-")
    t = re.sub(r"[^A-Za-z0-9]+", "-", r["title"])[:62].strip("-")
    return f"{port}_{r['year'] or 'nd'}_{t}_{r['ark'][-6:]}.jpg"


def main():
    rows = list(csv.DictReader(open(SEL)))
    print(f"{len(rows)} selected sheets\n")
    ok = skip = fail = 0
    held = []
    for r in rows:
        p = DEST / slug(r)
        if p.exists() and p.stat().st_size > 200000:
            skip += 1
            held.append((p, r))
            continue
        subprocess.run(["curl", "-sL", "-A", UA, "--max-time", "300",
                        "-o", str(p), IIIF.format(ark=r["ark"])], capture_output=True)
        if not p.exists() or p.stat().st_size < 200000:
            p.unlink(missing_ok=True)
            fail += 1
            print(f"  -- failed  {r['title'][:66]}", flush=True)
            continue
        ok += 1
        held.append((p, r))
        print(f"  OK {p.stat().st_size//1048576:>4} MB  {p.name[:80]}", flush=True)
        time.sleep(0.6)

    idx = [{"file": p.name, "ark": r["ark"], "ports": r["ports"],
            "year": r["year"], "soundings": r["soundings"], "title": r["title"]}
           for p, r in held]
    (DEST / "selection_index.json").write_text(
        json.dumps(idx, indent=1, ensure_ascii=False))
    mb = sum(p.stat().st_size for p, _ in held) / 1e6
    print(f"\ndownloaded {ok}, already held {skip}, failed {fail}  ({mb:.0f} MB total)")


if __name__ == "__main__":
    main()

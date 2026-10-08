"""Fetch the open-access PDFs from the geographic sweep, and log what resisted.

Two things make this harder than the first harvest. Several large publishers now
answer a scripted request with a JavaScript challenge page rather than the file,
so a 200 response is not evidence of a PDF and every download has to be checked
for the magic bytes. And OpenAlex reports several open-access locations per work,
which is the way around the first problem: when the publisher blocks, a preprint
server or an institutional repository usually holds the same text.

So each work is tried at every location it has, publisher last. Whatever still
fails is written to an acquisition list, since those need the Harvard proxy and
are a library request rather than a bug.
"""
import csv, re, json, pathlib, subprocess, sys, time

ROOT = pathlib.Path(__file__).resolve().parents[2]
DEST = ROOT / "library" / "oa-harvest"
D = pathlib.Path(__file__).resolve().parents[1] / "data" / "processed"

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")

# Hosts that serve a challenge page instead of the file. Tried last rather than
# skipped, because the block is not applied uniformly.
HOSTILE = ("link.springer.com", "sciencedirect.com", "mdpi.com",
           "pubs.geoscienceworld.org", "onlinelibrary.wiley.com",
           "tandfonline.com", "nature.com", "academic.oup.com")


def rank(url):
    return 1 if any(h in url for h in HOSTILE) else 0


def slug(gap, r):
    a = re.sub(r"[^A-Za-z]", "", (r["authors"].split(";")[0] or "anon").split()[-1] or "anon")
    t = re.sub(r"[^A-Za-z0-9]+", "-", r["title"])[:62].strip("-")
    return f"{gap}_{a}{r['year']}_{t}.pdf"[:140]


def fetch(url, path):
    """True if the bytes that came back are actually a PDF."""
    try:
        subprocess.run(
            ["curl", "-sL", "-A", UA, "-H", "Accept: application/pdf,*/*",
             "-e", "https://scholar.google.com/", "--max-time", "150",
             "-o", str(path), url],
            check=True, capture_output=True)
    except Exception:
        return False
    if not path.exists() or path.stat().st_size < 20000:
        path.unlink(missing_ok=True)
        return False
    with open(path, "rb") as fh:
        if fh.read(5) != b"%PDF-":
            path.unlink()
            return False
    return True


def main(wanted=None):
    DEST.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(open(D / "geo_literature_candidates.csv")))
    if wanted:
        keep = {w.strip().lower() for w in wanted}
        rows = [r for r in rows if r["doi"].lower() in keep]
    else:
        rows = [r for r in rows if r.get("keep") == "Y"]

    print(f"{len(rows)} works to try\n")
    ok = skip = 0
    missing = []
    for r in rows:
        p = DEST / slug(r["gap"], r)
        if p.exists() and p.stat().st_size > 20000:
            skip += 1
            continue
        urls = sorted([u for u in r["oa_urls"].split(" | ") if u], key=rank)
        got = next((u for u in urls if fetch(u, p)), None)
        if got:
            ok += 1
            print(f"  OK {p.stat().st_size//1024:>6}KB  {p.name[:84]}", flush=True)
        else:
            missing.append(r)
            print(f"  -- blocked      {r['title'][:70]}", flush=True)
        time.sleep(0.4)

    print(f"\ndownloaded {ok}, already held {skip}, blocked {len(missing)}")
    if missing:
        with open(D / "geo_acquisition_list.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["gap", "year", "authors", "title", "venue", "doi"])
            w.writeheader()
            for r in missing:
                w.writerow({k: r[k] for k in w.fieldnames})
        print(f"blocked titles -> geo_acquisition_list.csv (needs the Harvard proxy)")


if __name__ == "__main__":
    main(sys.argv[1:] or None)

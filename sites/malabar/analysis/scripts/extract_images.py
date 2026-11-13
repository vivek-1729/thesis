"""Pull every embedded image out of the Malabar readings, with an index.

Each image is saved as material/images/<source>/p<page>_<n>.<ext>. The index
records source, PDF page, size, and any caption-like line on the same page
(starting Fig., Figure, Pl., Plate or Abb.), so an image can be found by what
the publication says it is. Images under 120 px on either side are skipped as
icons and rules.
"""
import csv, pathlib, re, sys
import fitz

HERE = pathlib.Path(__file__).resolve().parents[1]
READ = HERE.parent / "readings"
OUT = HERE.parent / "material" / "images"
CAP = re.compile(r"^\s*(fig(ure)?s?\.?|pl(ate)?s?\.?|abb\.?|tab(le)?\.?)\s*\d", re.I)

rows = []
for pdf in sorted(READ.rglob("*.pdf")):
    key = re.sub(r"[^A-Za-z0-9]+", "_", pdf.stem)[:50].strip("_")
    supplied = "supplementary" not in pdf.parts
    doc = fitz.open(pdf)
    (OUT / key).mkdir(parents=True, exist_ok=True)
    for i, page in enumerate(doc):
        caps = [l.strip() for l in page.get_text().splitlines() if CAP.match(l)]
        for j, im in enumerate(page.get_images(full=True)):
            info = doc.extract_image(im[0])
            if min(info["width"], info["height"]) < 120:
                continue
            fn = OUT / key / f"p{i+1:03d}_{j}.{info['ext']}"
            fn.write_bytes(info["image"])
            rows.append(dict(source=key, supplied_reading=supplied, pdf_page=i + 1,
                             file=str(fn.relative_to(OUT)), width=info["width"],
                             height=info["height"], captions_on_page=" | ".join(caps)[:400]))
    print(f"{key}: {sum(r['source']==key for r in rows)} images", file=sys.stderr)

with open(OUT / "index.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
print(len(rows), "images indexed")

# A browsable gallery, one section per source, each image labelled with its page
# and the caption-like lines found on that page.
import html
by = {}
for r in rows:
    by.setdefault(r["source"], []).append(r)
parts = ["<!doctype html><meta charset=utf-8><title>Malabar reading images</title>",
         "<style>body{font:14px system-ui;margin:16px;background:#fafafa;color:#222}"
         "h2{margin-top:2em;border-bottom:1px solid #ccc}figure{display:inline-block;width:260px;"
         "vertical-align:top;margin:6px;background:#fff;padding:6px;border:1px solid #ddd}"
         "img{max-width:100%;max-height:260px}figcaption{font-size:11px;color:#555}"
         "nav a{margin-right:10px}</style>",
         "<h1>Images from the Malabar readings</h1><nav>"]
parts += [f'<a href="#{k}">{html.escape(k[:40])}</a>' for k in by]
parts.append("</nav>")
for k, rs in by.items():
    tag = "supplied" if rs[0]["supplied_reading"] else "supplementary"
    parts.append(f'<h2 id="{k}">{html.escape(k)} <small>({tag}, {len(rs)})</small></h2>')
    for r in rs:
        parts.append(f'<figure><a href="{r["file"]}"><img loading=lazy src="{r["file"]}"></a>'
                     f'<figcaption><b>PDF p. {r["pdf_page"]}</b> · {r["width"]}×{r["height"]}<br>'
                     f'{html.escape(r["captions_on_page"][:200])}</figcaption></figure>')
(OUT / "gallery.html").write_text("\n".join(parts))
print("wrote gallery.html")

"""Pre-British charts of our four coasts, from Gallica.

The Admiralty sheets we already hold are 1857 to 1897. Gallica holds French and
Dutch charts from the seventeenth and eighteenth centuries, which is 150 to 250
years earlier and before any modern river engineering. Public domain, served
over IIIF at 50 to 95 megapixels.

Still nowhere near the Periplus, but each earlier survey tightens the bound on
how much the coast has moved, and the Dutch held Cochin from 1663 to 1795 so
their charts are the best pre-British record of the Malabar backwaters.
"""
import json, pathlib, time, urllib.request

OUT = pathlib.Path(__file__).resolve().parents[2] / "library" / "charts-gallica"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

CHARTS = {
    # Malabar. The first carries soundings and predates 1700.
    "malabar-canara-soundings-c1700": ("btv1b53257153h", "Carte particuliere des costes de Canara et de Malabar, avec les sondes, 16..-17.."),
    "malabar-dutch-1694":             ("btv1b59057278", "Carte hollandaise des cotes de Malabar et de Coromandel, 1694-1696"),
    "malabar-decust-17c":             ("btv1b532571416", "De cust Mallabaar, 17th century Dutch"),
    "malabar-ms-1799-rajapour-cochin":("btv1b530531363", "Carte manuscrite de la cote de Malabar depuis Rajapour jusqu'a Cochin, 1799"),
    "malabar-mccluer-1791":           ("btv1b532562290", "A chart of part of the Malabar coast, John McCluer, 1791"),
    "malabar-hydrographical-1780":    ("btv1b53256197m", "Malabar coast, Hydrographical Office, 1780"),
    "malabar-comorin-mangalore-18c":  ("btv1b532562273", "Cote de Malabar depuis le cap Comorin jusqu'a Mangalore, 17.."),
    # Indus
    "indus-gulf-guadar-kutch":        ("btv1b532624141", "Carte du Golfe de l'Indus depuis Guadar jusqu'au Golfe de Kutch"),
    # Red Sea
    "redsea-west-coast-1787":         ("btv1b53262700z", "Carte de la cote occidentale de la Mer Rouge, 17 to 24 N, 1787"),
    "redsea-ports-banks-c1700":       ("btv1b8459520q", "Carte des principaux Ports de Mer, Bancs de Sable etc, Mer Rouge, 1693-1703"),
    # East Africa
    "zanzibar-1784":                  ("btv1b8595694g", "Plan of the island of Zanzibar, from a French ms., 1784"),
    "zanzibar-1846":                  ("btv1b8440031q", "Plan de Zanzibar, 1846"),
}


def info(ark):
    u = f"https://gallica.bnf.fr/iiif/ark:/12148/{ark}/f1/info.json"
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60))


def full(ark, dest):
    u = f"https://gallica.bnf.fr/iiif/ark:/12148/{ark}/f1/full/full/0/native.jpg"
    with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=900) as r:
        dest.write_bytes(r.read())


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    index = []
    for key, (ark, title) in CHARTS.items():
        dest = OUT / f"{key}.jpg"
        try:
            meta = info(ark)
            if not dest.exists():
                full(ark, dest)
            mp = meta["width"] * meta["height"] / 1e6
            index.append({"key": key, "ark": ark, "title": title,
                          "width": meta["width"], "height": meta["height"],
                          "bytes": dest.stat().st_size,
                          "source": f"https://gallica.bnf.fr/ark:/12148/{ark}"})
            print(f"{key:34s} {meta['width']:6d}x{meta['height']:<6d} {mp:5.0f} MP  {dest.stat().st_size/1e6:6.1f} MB")
        except Exception as e:
            print(f"{key:34s} FAILED {type(e).__name__}: {str(e)[:70]}")
        time.sleep(1.5)
    (OUT / "index.json").write_text(json.dumps(index, indent=1))
    print(f"\n{len(index)} charts in {OUT}")

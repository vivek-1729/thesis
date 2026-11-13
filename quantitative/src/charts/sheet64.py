"""Georeference Admiralty chart 64, Sacrifice Rock to Beipur (survey 1887, published 1888).

Unlike sheets 749 and 750, this chart has no graticule on its border. It states one position in its
title, "Beipur Flagstaff: Lat. 11 9' 37" N, Long. 75 48' 26" E (depending upon Bombay Observatory being
in 72 48' 58" E)", and it carries a "Scale of Latitude and Distance" in sea miles. The transform uses:

  anchor  the flagstaff symbol (F.S.), just south of the Beypore river mouth, read at chart pixel
          (10306, 13378), to about +/- 5 px (about 15 m);
  scale   the bar's 0, 1 and 4 sea-mile ticks at x = 1201, 1797 and 3588 (one minute of latitude =
          596.75 px; the 1-mile and 4-mile ticks agree with a single scale to within 3 px). At the
          stated natural scale of 1:48,380 this implies a scan of about 400 dpi, which is consistent;
  north   taken as the sheet's vertical, as on all Admiralty Mercator charts. Not yet checked against
          an independent control point; a rotation error would grow with distance from the flagstaff.

Longitude pixels per minute come from the latitude scale through the cosine of the latitude
(Mercator). Over the 20 minutes of latitude the chart spans, the Mercator stretch is about 0.1 per
cent and is ignored.

The longitude depends on the 1887 value for Bombay Observatory. Any difference between that value and
the modern one shifts the whole chart east or west by the same amount; it does not distort it.

Datum (from the chart): "the level of the lowest low water spring tides", 17.2 ft below a bench mark at
the Beypore custom house. Spring rise 5 ft at Kadalur, Calicut and Beypore.
"""
import json, math, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "data" / "processed" / "charts" / "admiralty_georef.json"

ANCHOR_PX = (10306.0, 13378.0)
ANCHOR_LAT = 11 + 9 / 60 + 37 / 3600
ANCHOR_LON = 75 + 48 / 60 + 26 / 3600
PX_PER_ARCMIN_LAT = (3588 - 1201) / 4


def entry():
    px_lon = PX_PER_ARCMIN_LAT * math.cos(math.radians(ANCHOR_LAT))
    lat_a = -1 / (PX_PER_ARCMIN_LAT * 60)
    return dict(
        file="malabar-64-1888.jpg",
        title="India, West Coast, Sacrifice Rock to Beipur",
        surveyor="Lieuts. E. C. H. Helby and B. Whitehouse R.N., G. L. E. Mathias I.M., Bulwant Rajaram",
        surveyed="1887", scale="1:48,380",
        tide="Datum: lowest low water springs; spring rise 5 ft (Kadalur, Calicut, Beipur)",
        method="anchor (Beipur flagstaff, title) + scale bar; north = sheet vertical",
        lon_anchor_px=ANCHOR_PX[0], lon_anchor_deg=ANCHOR_LON,
        lat_a=lat_a, lat_b=ANCHOR_LAT - lat_a * ANCHOR_PX[1],
        px_per_arcmin_lat=PX_PER_ARCMIN_LAT, px_per_arcmin_lon=px_lon,
    )


if __name__ == "__main__":
    g = json.loads(OUT.read_text())
    g["BA64"] = entry()
    OUT.write_text(json.dumps(g, indent=1))
    e = g["BA64"]
    for name, (x, y) in {"top-left of frame": (430, 330), "bottom-right of frame": (11050, 15600)}.items():
        print(name, round(e["lat_a"] * y + e["lat_b"], 4), round(e["lon_anchor_deg"] + (x - e["lon_anchor_px"]) / e["px_per_arcmin_lon"] / 60, 4))

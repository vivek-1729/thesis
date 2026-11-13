"""Sounding windows on the georeferenced Admiralty sheets, one per candidate mouth.

Kodungallur, the first window, keeps its own scripts (detect_soundings.py, transcription_1857.py,
build_soundings_1857.py) and data folder. The windows here use the generic pipeline in soundings.py,
with data in data/soundings/<site>/ and hand readings in scripts/transcriptions/<site>.py.

Chart 64 is printed in lighter ink than Selby's sheets, so its glyph threshold is 170 rather than 125.

Windows are chart pixels (x0, y0, x1, y1). Each runs from the shore out to roughly the 10-fathom line,
about 1,600 px (16 km at 1:146,000) on a side, like the Kodungallur window.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
CHARTS = ROOT.parent / "library" / "charts"

SITES = {
    # port, candidate(s), sheet, window
    "ponnani": dict(port="Tyndis", candidates="Ponnani", sheet="BA749", file="malabar-749-1857.jpg",
                    surveyed="1851-3", window=(3300, 2200, 4900, 3800)),
    "tanur": dict(port="Tyndis", candidates="Tanur", sheet="BA749", file="malabar-749-1857.jpg",
                  surveyed="1851-3", window=(3000, 450, 4600, 2050)),
    "kollam": dict(port="Nelkynda / Bakare", candidates="Kollam, Neendakara, Thangassery", sheet="BA750",
                   file="malabar-750-1857.jpg", surveyed="1850-2", window=(4700, 8500, 6400, 10100)),
    "purakkad": dict(port="Nelkynda / Bakare", candidates="Purakkad, Nirkunnam", sheet="BA750",
                     file="malabar-750-1857.jpg", surveyed="1850-2 (with soundings added 'in 1901')",
                     window=(3200, 4500, 4800, 6200)),
    # chart 64 (survey 1887, 1:48,380, about three times Selby's scale; datum lowest low water springs)
    "beypore": dict(port="Tyndis", candidates="Beypore, Chaliyam (Kadalundi is off the chart's eastern edge)",
                    sheet="BA64", file="malabar-64-1888.jpg", surveyed="1887", window=(8300, 11900, 10740, 14400), ink=170),
    "koyilandy": dict(port="Tyndis", candidates="Koyilandy (Panthalayani Kollam, charted as 'Kollam' beside 'Quilandi')",
                      sheet="BA64", file="malabar-64-1888.jpg", surveyed="1887", window=(4400, 2300, 7000, 4900), ink=170),
}
UTM_EPSG = 32643

# ---- seabed-model geometry, in window pixels -------------------------------------------------------
# coast  the charted shoreline (the drawn coastline at the seaward edge of the beach and palms), north to
#        south. Taken from an automatic trace where it followed the line, and traced by hand from a gridded
#        overview elsewhere (river mouths, Quilon town, Beypore, the Koyilandy shoal). About +/- 20 px:
#        200 m on Selby's sheets, 60 m on chart 64. Everything east of it is treated as land or unsounded
#        backwater, as at Kodungallur.
# mouth  a river or lagoon entrance, or None. A circle of mouth_r_km round it is cut out of the land, so the
#        entrance channel and its soundings stay in the model, and model F's mouth term is centred on it.
# ref    the reference point on the shore from which anchorage distance and the controlling depth are
#        measured: the mouth where there is one, otherwise the shore opposite the candidate town.
GEOMETRY = {
    "ponnani": dict(coast=[(845, 0), (850, 100), (858, 200), (875, 300), (883, 400), (898, 500), (905, 600),
                           (931, 662), (995, 712), (1030, 760), (1056, 800), (1104, 900), (1125, 1000), (1161, 1100),
                           (1208, 1200), (1254, 1300), (1283, 1400), (1350, 1500), (1395, 1600)],
                    mouth=(962, 688), mouth_r_km=0.3, ref=(962, 688)),
    "tanur": dict(coast=[(780, 60), (782, 100), (788, 200), (805, 300), (823, 400), (865, 500), (876, 600), (912, 700),
                         (944, 800), (968, 900), (998, 1000), (1015, 1100), (1036, 1200), (1054, 1300), (1076, 1400),
                         (1088, 1500), (1100, 1600)],
                  mouth=None, mouth_r_km=0, ref=(876, 600)),
    "kollam": dict(coast=[(788, 0), (795, 100), (808, 200), (840, 300), (867, 400), (880, 500), (912, 600), (955, 670),
                          (1010, 775), (1020, 850), (1045, 930), (1082, 990), (1130, 1060), (1190, 1130), (1235, 1185),
                          (1300, 1195), (1360, 1210), (1420, 1235), (1470, 1260), (1530, 1290), (1580, 1330), (1650, 1360), (1700, 1380)],
                   mouth=(985, 720), mouth_r_km=0.3, ref=(985, 720)),
    "purakkad": dict(coast=[(720, 0), (726, 100), (734, 200), (766, 300), (820, 400), (838, 500), (876, 600), (934, 700),
                            (955, 800), (979, 900), (1028, 1000), (1062, 1100), (1101, 1200), (1144, 1300), (1187, 1400),
                            (1233, 1500), (1279, 1600), (1300, 1700)],
                     mouth=None, mouth_r_km=0, ref=(1030, 1000)),
    "beypore": dict(coast=[(1340, 0), (1398, 200), (1489, 400), (1568, 600), (1625, 800), (1739, 1000), (1795, 1100),
                           (1818, 1200), (1864, 1350), (1909, 1432), (2000, 1432), (1989, 1591), (2045, 1773),
                           (2182, 1909), (2295, 2023), (2386, 2136), (2440, 2250)],
                    mouth=(1950, 1430), mouth_r_km=0.15, ref=(1950, 1430)),
    "koyilandy": dict(coast=[(0, 106), (236, 71), (402, 95), (709, 165), (946, 284), (1135, 449), (1277, 591), (1324, 662),
                             (1418, 709), (1537, 804), (1655, 946), (1749, 1087), (1868, 1229), (1986, 1418), (2080, 1608),
                             (2175, 1797), (2293, 1986), (2411, 2128), (2506, 2317), (2577, 2506)],
                      mouth=None, mouth_r_km=0, ref=(1868, 1229)),
}
# Kodungallur already has model inputs from bathymetry_1857.ipynb (data/pilot_1857/local/); it enters the
# comparison through them, not through this table.

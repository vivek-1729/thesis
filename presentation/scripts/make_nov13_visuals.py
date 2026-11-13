"""Visuals for the 13 November 2026 presentation (Malabar case study, quantitative and qualitative).

Every image is one of three kinds, recorded in presentation/nov_13th/MANIFEST.md:
  archival   a real chart, map or manuscript, cropped or annotated (rings, outlines), never redrawn
  published  a figure from a cited publication, extracted from the PDF
  data       a plot made directly from the project's transcriptions, model outputs or dated evidence

Morph sequences (files ending a, b, c ...) share one canvas size and framing, so PowerPoint's Morph or Fade
moves between them without a jump.

  python make_nov13_visuals.py            all slides
  python make_nov13_visuals.py s04 s05    some slides
"""
import sys, json, pathlib, textwrap
import numpy as np, pandas as pd, geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from PIL import Image, ImageDraw, ImageFont

Image.MAX_IMAGE_PIXELS = None
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "presentation" / "nov_13th"; OUT.mkdir(parents=True, exist_ok=True)
SRC = ROOT / "presentation" / "sources"
CHARTS = ROOT.parent / "library" / "charts"
COAST = ROOT / "quantitative" / "coastline"
MAL = ROOT / "sites" / "malabar"
FATHOM = 1.8288

# ---- style -------------------------------------------------------------------------------------------
PAPER = "#F4EFE6"        # chart paper
INK = "#2B2B2B"
LAND = "#D9CFBC"
DEEP = "#1F5F7A"         # water deep enough for a loaded ship
SHALLOW = "#E8D9A8"      # too shallow
ACCENT = "#B5432F"       # highlights
DEPTH_CMAP = LinearSegmentedColormap.from_list("depth", ["#F1E7C9", "#BFD9D6", "#6FA8B8", "#2F6F8F", "#163F5C"])
W169 = (19.2, 10.8)      # inches at 100 dpi -> 1920 x 1080
plt.rcParams.update({"font.family": "serif", "font.serif": ["Georgia", "Times New Roman", "DejaVu Serif"],
                     "axes.edgecolor": INK, "text.color": INK, "axes.labelcolor": INK,
                     "xtick.color": INK, "ytick.color": INK, "savefig.facecolor": PAPER, "figure.facecolor": PAPER})
MANIFEST = []


def note(fname, slide, kind, what, source):
    MANIFEST.append(dict(file=fname, slide=slide, kind=kind, what=what, source=source))


def save(fig, name, transparent=False):
    fig.savefig(OUT / name, dpi=100, facecolor="none" if transparent else PAPER, transparent=transparent)
    plt.close(fig)


def canvas_fit(img, size=(1920, 1080), bg=PAPER):
    """Place an image on a 16:9 canvas, scaled to fit, centred."""
    c = Image.new("RGB", size, bg); im = img.copy(); im.thumbnail(size, Image.LANCZOS)
    c.paste(im, ((size[0] - im.width) // 2, (size[1] - im.height) // 2)); return c


# ---- slide 1: title backdrop ---------------------------------------------------------------------------
def s00_dividers():
    im = Image.open(CHARTS / "malabar-750-1857.jpg").convert("RGB")
    cx, cy, h = 4300, 5350, 1500; w = h * 16 / 9
    im.crop((int(cx - w / 2), int(cy - h / 2), int(cx + w / 2), int(cy + h / 2))).resize((1920, 1080), Image.LANCZOS).save(OUT / "s00_divider_ports.jpg", quality=90)
    note("s00_divider_ports.jpg", 0, "archival", "sheet 750 off Porakad (Purakkad), with its mud-bank anchorage, for the Part II divider",
         "Admiralty Chart No 750 (Selby, surveyed 1850-2, published 1857; this scan carries later additions), Wikimedia Commons, public domain")


def s01():
    im = Image.open(CHARTS / "malabar-749-1857.jpg").crop((4600, 7000, 7800, 8800))     # Kodungallur reach
    im = im.resize((1920, 1080), Image.LANCZOS); im.save(OUT / "s01_title_backdrop.jpg", quality=90)
    strip = Image.open(CHARTS / "malabar-749-1857.jpg").crop((4480, 7700, 8380, 8820))        # ~3.5:1, below the title
    strip.resize((2400, int(2400 * strip.height / strip.width)), Image.LANCZOS).save(OUT / "s01b_title_strip.jpg", quality=90)
    note("s01b_title_strip.jpg", 1, "archival", "a wide strip of sheet 749 round Kodungallur, placed under the title",
         "Admiralty Chart No 749 (Selby, surveyed 1851-3, published 1857), Wikimedia Commons, public domain")
    note("s01_title_backdrop.jpg", 1, "archival", "Admiralty sheet 749, the coast at Kodungallur",
         "Admiralty Chart No 749, Malabar Coast of India, surveyed by W. B. Selby 1851-3, published 1857 (Wikimedia Commons, public domain)")


# ---- slide 2: the Periplus map, with the two clusters ringed --------------------------------------------
def s02():
    m = Image.open(SRC / "periplus_map.jpg").convert("RGB"); W, H = m.size; k = W / 1400
    cred = "Map: PHGCOM, 'Map of the Periplus of the Erythraean Sea', Wikimedia Commons, CC BY-SA 4.0"
    canvas_fit(m).save(OUT / "s02a_periplus_map.jpg", quality=92)
    # Ed-Dur: the Musandam tip is at map pixel (1477, 580) at ~30 px per degree; Umm al-Quwain lies ~0.75 deg W
    # and ~0.85 deg S of it, on the Gulf-side coast, at about (1452, 606)
    # Malabar: the map's Tyndis, Muziris and Nelcynda dots, at about (812, 416) to (830, 437) on a 1400-px-wide copy
    rings = {"Malabar ports": (822 * k, 426 * k, 22 * k, 26 * k), "Ed-Dur": (1452, 606, 34, 34)}
    a = m.copy(); d = ImageDraw.Draw(a)
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Bold.ttf", int(30 * k / 1.6))
    for label, (x, y, rx, ry) in rings.items():
        for t in range(6):
            d.ellipse([x - rx - t, y - ry - t, x + rx + t, y + ry + t], outline=ACCENT)
        tx, ty = (x - rx - 150, y + ry + 4) if label == "Ed-Dur" else (x - rx - 330, y + ry - 10)
        d.text((tx, ty), label, fill=ACCENT, font=font, stroke_width=4, stroke_fill="white")
    canvas_fit(a).save(OUT / "s02b_periplus_map_ringed.jpg", quality=92)
    a.save(OUT / "s02d_periplus_map_ringed_fullres.jpg", quality=90)                # one picture for the zoom morph
    note("s02d_periplus_map_ringed_fullres.jpg", 2, "archival", "the ringed map at full resolution (3507 x 1921), used for the zoom morph in the deck", cred)
    # zoom on the Arabian Sea, same aspect, for a morph from the full map
    x0, y0, x1 = 450 * k, 205 * k, 980 * k; y1 = y0 + (x1 - x0) * 9 / 16
    a.crop((int(x0), int(y0), int(x1), int(y1))).resize((1920, 1080), Image.LANCZOS).save(OUT / "s02c_periplus_map_zoom.jpg", quality=92)
    for f, w in [("s02a_periplus_map.jpg", "the full map"), ("s02b_periplus_map_ringed.jpg", "Malabar cluster and Ed-Dur ringed"),
                 ("s02c_periplus_map_zoom.jpg", "zoom to the Arabian Sea, rings kept")]:
        note(f, 2, "archival", w + ". Ed-Dur is not on the map; its ring is placed at 25.55 N 55.6 E relative to the map's own Musandam peninsula, to about half a degree", cred)


# ---- slide 4: sheet 749, full and the Kodungallur window ------------------------------------------------
KWIN = dict(x0=5600, y0=7600, x1=7300, y1=9300)


def s04():
    full = Image.open(CHARTS / "malabar-749-1857.jpg").convert("RGB")
    a = canvas_fit(full); a.save(OUT / "s04a_sheet749_full.jpg", quality=90)
    b = full.copy(); d = ImageDraw.Draw(b)
    zx, zy = (KWIN["x0"] + KWIN["x1"]) / 2, (KWIN["y0"] + KWIN["y1"]) / 2; zh = KWIN["y1"] - KWIN["y0"]; zw = zh * 16 / 9
    for t in range(18):                                             # the 16:9 box the deck zooms to
        d.rectangle([zx - zw / 2 + t, zy - zh / 2 + t, zx + zw / 2 - t, zy + zh / 2 - t], outline=ACCENT)
    canvas_fit(b).save(OUT / "s04b_sheet749_window.jpg", quality=90)
    b.save(OUT / "s04d_sheet749_window_fullres.jpg", quality=85)                     # one picture for the zoom morph
    note("s04d_sheet749_window_fullres.jpg", 4, "archival", "the whole sheet with the window outlined, at full resolution, used for the zoom morph in the deck",
         "Admiralty Chart No 749 (Selby, surveyed 1851-3, published 1857), Wikimedia Commons, public domain")
    cx, cy = (KWIN["x0"] + KWIN["x1"]) / 2, (KWIN["y0"] + KWIN["y1"]) / 2; h = KWIN["y1"] - KWIN["y0"]; w = h * 16 / 9
    full.crop((int(cx - w / 2), int(cy - h / 2), int(cx + w / 2), int(cy + h / 2))).resize((1920, 1080), Image.LANCZOS).save(OUT / "s04c_kodungallur_mouth.jpg", quality=92)
    src = "Admiralty Chart No 749 (Selby, surveyed 1851-3, published 1857; scan of the 1914 edition), Wikimedia Commons, public domain"
    note("s04a_sheet749_full.jpg", 4, "archival", "the whole sheet", src)
    note("s04b_sheet749_window.jpg", 4, "archival", "the sheet with the zoom target (16:9, centred on the Kodungallur window) outlined", src)
    note("s04c_kodungallur_mouth.jpg", 4, "archival", "the Kodungallur mouth, the window at full resolution (16:9)", src)
    return (cx, cy, w, h)


# ---- slide 5: chart -> points (same framing) ------------------------------------------------------------
def s05():
    full = Image.open(CHARTS / "malabar-749-1857.jpg").convert("RGB")
    cx, cy = (KWIN["x0"] + KWIN["x1"]) / 2, (KWIN["y0"] + KWIN["y1"]) / 2; h = KWIN["y1"] - KWIN["y0"]; w = h * 16 / 9
    box = (int(cx - w / 2), int(cy - h / 2), int(cx + w / 2), int(cy + h / 2))
    crop = full.crop(box).resize((1920, 1080), Image.LANCZOS); sc = 1920 / (box[2] - box[0])
    s = pd.read_csv(COAST / "data/soundings_1857/soundings_1857.csv"); s = s[s.status.isin(["ok", "unsure"])]
    px = (s.chart_x - box[0]) * sc; py = (s.chart_y - box[1]) * sc
    crop.save(OUT / "s05a_chart.jpg", quality=92)
    for name, base_alpha in [("s05b_chart_with_points.png", 1.0), ("s05c_points_only.png", 0.0)]:
        fig = plt.figure(figsize=W169); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1920); ax.set_ylim(1080, 0); ax.axis("off")
        bg = np.asarray(crop).astype(float) / 255
        if base_alpha < 1:
            bg = bg * 0.12 + np.array(Image.new("RGB", (1, 1), PAPER).getpixel((0, 0))) / 255 * 0.88
        ax.imshow(bg, extent=[0, 1920, 1080, 0])
        sc_ = ax.scatter(px, py, c=s.depth_m, cmap=DEPTH_CMAP, vmin=0, vmax=22, s=70, edgecolors=INK, linewidths=.6, zorder=3)
        save(fig, name)
    note("s05a_chart.jpg", 5, "archival", "chart crop at the Kodungallur mouth (same framing as s04c)", "Admiralty Chart No 749")
    note("s05b_chart_with_points.png", 5, "data", "the 428 usable soundings (ok + unsure) over the chart, coloured by depth (0-22 m)",
         "transcription: quantitative/coastline/data/soundings_1857/soundings_1857.csv")
    note("s05c_points_only.png", 5, "data", "the same points with the chart faded out (same framing)", "as s05b")


# ---- slides 6, 7, 9: the Kodungallur mouth in 3D (one camera for all, so they morph) ---------------------
def mouth3d_data():
    import matplotlib.tri as mtri
    L = COAST / "data/pilot_1857/local"
    verts = pd.read_csv(L / "verts.csv")
    SV = np.fromfile(L / "samples_verts.bin", dtype=np.float32).reshape(-1, len(verts)).T       # model F draws
    land = gpd.read_file(L / "land.geojson").geometry[0]
    vx, vy, kind = verts.x_km.values, verts.y_km.values, verts.kind.values
    tri = mtri.Triangulation(vx, vy); t = tri.triangles
    cent = gpd.GeoSeries(gpd.points_from_xy(vx[t].mean(1), vy[t].mean(1)))
    on_land = cent.within(land).values
    uns = np.isin(kind, ["unsounded"])[t].any(1)
    long_edge = np.max(np.hypot(np.diff(vx[t][:, [0, 1, 2, 0]], axis=1), np.diff(vy[t][:, [0, 1, 2, 0]], axis=1)), axis=1) > 0.25
    wet = np.isin(kind, ["water", "shore"])
    return dict(vx=vx, vy=vy, wet=wet, SV=SV, water_tri=t[~on_land & ~uns & ~long_edge], land_tri=t[on_land],
                uns_tri=t[uns & ~on_land & ~long_edge],
                snd=pd.read_csv(L / "soundings.csv"), mouth=pd.read_csv(L / "mouth.csv").iloc[0])


def mouth3d_fig(d, mode, domain_x=(0, 1), zoom=1.0):
    import plotly.graph_objects as go
    vx, vy = d["vx"], d["vy"]; mean = d["SV"].mean(1)
    z = np.where(d["wet"], -mean, 0.0)
    fig = go.Figure()
    mk = lambda tris, **kw: go.Mesh3d(x=vx, y=vy, z=kw.pop("zz", z), i=tris[:, 0], j=tris[:, 1], k=tris[:, 2], flatshading=False,
                                      lighting=dict(ambient=.55, diffuse=.7, specular=.15, roughness=.8), **kw)
    fig.add_trace(mk(d["land_tri"], zz=np.full(len(vx), 1.0), color=LAND, opacity=1))
    fig.add_trace(mk(d["uns_tri"], zz=np.full(len(vx), -0.3), color="#C9D6DA", opacity=1))
    if mode == "points":
        pass                                                               # points only, no surface
    elif mode in ("surface", "surface_nodots"):
        fig.add_trace(mk(d["water_tri"], intensity=z, colorscale=[[0, "#163F5C"], [.35, "#2F6F8F"], [.65, "#6FA8B8"], [.85, "#BFD9D6"], [1, "#F1E7C9"]],
                         cmin=-14, cmax=0.5, showscale=False))
    elif mode == "ship":
        need = 3.5                                                         # 3 m draught + 0.5 m clearance
        ok = (d["SV"] > need).mean(1) >= 0.9
        fig.add_trace(mk(d["water_tri"], vertexcolor=np.where(ok & d["wet"], DEEP, SHALLOW)))
    s = d["snd"]
    if mode in ("points", "surface"):
        fig.add_trace(go.Scatter3d(x=s.x_km, y=s.y_km, z=-s.depth_m, mode="markers",
                                   marker=dict(size=6 if mode == "points" else 4, color=-s.depth_m if mode == "points" else INK,
                                               colorscale=[[0, "#163F5C"], [.5, "#6FA8B8"], [1, "#E9C46A"]], cmin=-14, cmax=0,
                                               line=dict(width=0))))
    if mode == "ship":
        m = d["mouth"]; fig.add_trace(go.Scatter3d(x=[m.x_km], y=[m.y_km], z=[0.6], mode="markers", marker=dict(size=7, color=ACCENT)))
    ax = dict(visible=False, showbackground=False)
    fig.update_layout(width=1920, height=1080, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor=PAPER, showlegend=False,
                      scene=dict(domain=dict(x=list(domain_x), y=[0, 1]), xaxis=ax, yaxis=ax, zaxis=dict(ax, range=[-16, 3]), aspectmode="manual",
                                 aspectratio=dict(x=.75, y=1, z=.32), camera=dict(eye=dict(x=-.86 * zoom, y=-.70 * zoom, z=.52 * zoom), center=dict(x=0, y=.03, z=-.12))))
    return fig


def ship_legend(path, x, y):
    from PIL import ImageFont
    im = Image.open(path).convert("RGB"); d = ImageDraw.Draw(im)
    f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 24)
    for col, lab, k in [(DEEP, "deep enough for a ship drawing 3 m", 0), (SHALLOW, "too shallow", 1)]:
        yy = y + k * 40; d.rectangle([x, yy, x + 34, yy + 24], fill=col, outline=(150, 140, 122)); d.text((x + 48, yy - 2), lab, font=f, fill=INK)
    d.ellipse([x + 4, y + 86, x + 28, y + 110], fill=ACCENT, outline="white", width=3); d.text((x + 48, y + 82), "the Kodungallur mouth", font=f, fill=INK)
    im.save(path)


def depth_legend(path, x, y):
    from PIL import ImageFont
    im = Image.open(path).convert("RGB"); d = ImageDraw.Draw(im)
    f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 22)
    stops = [(0, "#163F5C"), (.35, "#2F6F8F"), (.65, "#6FA8B8"), (.85, "#BFD9D6"), (1, "#F1E7C9")]   # as the 3D colourscale
    hexrgb = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
    W_, H_ = 360, 22
    for i in range(W_):
        depth = 14 * i / (W_ - 1); t = (-depth + 14) / 14.5
        for (t0, c0), (t1, c1) in zip(stops[:-1], stops[1:]):
            if t0 <= t <= t1:
                c0, c1 = hexrgb(c0), hexrgb(c1); u = (t - t0) / (t1 - t0)
                col = tuple(int(c0[j] + (c1[j] - c0[j]) * u) for j in range(3)); break
        d.line([(x + i, y + 36), (x + i, y + 36 + H_)], fill=col)
    d.rectangle([x, y + 36, x + W_, y + 36 + H_], outline=(150, 140, 122))
    d.text((x, y), "Depth below low water", font=f, fill=INK)
    for dv in (0, 2, 5, 10, 14):
        xx = x + dv / 14 * (W_ - 1); d.line([(xx, y + 36 + H_), (xx, y + 36 + H_ + 6)], fill=(110, 104, 92), width=2)
        d.text((xx, y + 36 + H_ + 10), f"{dv} m", font=f, fill="#5E574C", anchor="ma")
    im.save(path)


def s06_07_09_3d():
    d = mouth3d_data()
    for mode, name, slide, kind, what in [
            ("points", "s06_soundings_3d.png", 6, "data", "the 157 soundings of the near-shore box at their depths, over a flat sea surface"),
            ("surface", "s07_seabed_3d.png", 7, "data", "model F posterior mean seabed with the soundings on it (Gaussian-process field, R-INLA)"),
            ("surface_nodots", "s09a0_seabed_3d_nodots.png", 9, "data", "the s07 seabed without the sounding dots, the first frame of slide 9 (same camera as s09a, so it recolours in place)"),
            ("ship", "s09a_ship_water_3d.png", 9, "data", "the same seabed in two tones: water at least 3.5 m deep with probability >= 0.9 (a 3 m draught plus 0.5 m) in blue, shallower in sand; red dot the mouth; legend lower right")]:
        mouth3d_fig(d, mode).write_image(str(OUT / name), scale=1)
        if mode == "ship":
            ship_legend(OUT / name, x=1380, y=860)
        if mode == "surface_nodots":
            depth_legend(OUT / name, x=1380, y=860)
        note(name, slide, kind, what + ". Same camera as the other 3D views, for Morph",
             "model F (bathymetry_1857.ipynb section 8b): quantitative/coastline/data/pilot_1857/local/samples_verts.bin; soundings from Admiralty Chart 749")


# ---- slide 8: does it work? ----------------------------------------------------------------------------
def s08():
    V = ROOT / "data/cache/validation/slp"
    ev = pd.read_csv(V / "eval.csv"); o = ev[ev.lagoon == 0].reset_index(drop=True)
    S = np.fromfile(V / "samples/rep_F_0.bin", dtype=np.float32).reshape(-1, len(o)).T
    survey = pd.read_csv(V / "rep_0.csv"); land = gpd.read_file(V / "land.geojson").geometry[0]
    step = 0.1
    def grid(vals, frame):
        i = np.round((frame.x_km - ev.x_km.min()) / step).astype(int); j = np.round((frame.y_km - ev.y_km.min()) / step).astype(int)
        A = np.full((int(round((ev.y_km.max() - ev.y_km.min()) / step)) + 1, int(round((ev.x_km.max() - ev.x_km.min()) / step)) + 1), np.nan)
        A[j, i] = vals; return A
    ext = [ev.x_km.min() - step / 2, ev.x_km.max() + step / 2, ev.y_km.min() - step / 2, ev.y_km.max() + step / 2]
    lag = grid(np.ones(ev.lagoon.sum()), ev[ev.lagoon == 1])
    panels = [("s08a_texas_real_seabed.png", grid(o.depth_true.values, o), False, "The real seabed"),
              ("s08b_texas_rebuilt.png", grid(S.mean(1), o), True, "Rebuilt from %d soundings" % len(survey))]
    for name, A, pts, title in panels:
        fig = plt.figure(figsize=(9.6, 10.8)); ax = fig.add_axes([0.04, 0.04, 0.92, 0.86])
        ax.imshow(np.where(np.isnan(lag), np.nan, 1), origin="lower", extent=ext, cmap=ListedColormap(["#DCE4E4"]))
        im = ax.imshow(A, origin="lower", extent=ext, cmap=DEPTH_CMAP, vmin=0, vmax=10)
        gpd.GeoSeries([land]).plot(ax=ax, color=LAND, edgecolor="#A89F8C", linewidth=.6)
        if pts:
            ax.scatter(survey.x_km, survey.y_km, s=18, c=INK, edgecolors="white", linewidths=.5, zorder=4)
        ax.set_xlim(ext[0], ext[1]); ax.set_ylim(ext[2], ext[3]); ax.set_aspect("equal"); ax.axis("off")
        fig.text(0.5, 0.94, title, ha="center", fontsize=30)
        save(fig, name)
    note("s08a_texas_real_seabed.png", 8, "data", "San Luis Pass, Texas: the true seabed (NOAA CUDEM 1/9 arc-second, averaged to 100 m), depth 0-10 m; grey: lagoon, left unsounded as at Kodungallur",
         "NOAA NCEI Continuously Updated DEM (CUDEM), tiles ncei19_n29x25_w095x25 and ncei19_n29x00_w095x25; validation_bathymetry.ipynb")
    note("s08b_texas_rebuilt.png", 8, "data", "the same frame: the seabed reconstructed by model F from one simulated 1850s-style survey (black dots), same colour scale",
         "validation_bathymetry.ipynb, survey rep_0, model F posterior mean")
    # the pair, with the fit for exactly this survey, in words
    e = S.mean(1) - o.depth_true.values
    zones = {"open": (o.dist_km >= 1) & (o.d_mouth >= 2), "shore": (o.dist_km < 1) & (o.d_mouth >= 2), "inlet": o.d_mouth < 1}
    rmse = {k: float(np.sqrt(np.mean(e[m.values] ** 2))) for k, m in zones.items()}
    cm = lambda v: f"{int(round(v * 10)) * 10} cm" if v < 0.95 else ("a metre" if v < 1.05 else f"{v:.1f} m")
    caption = (f"Rebuilt from {len(survey)} soundings, the seabed comes back to within about {cm(rmse['open'])} in open water\n"
               f"and {cm(rmse['shore'])} along the shore. In the inlet itself, about {cm(rmse['inlet'])}.")
    fig = plt.figure(figsize=W169)
    for k, (A, pts, title) in enumerate([(grid(o.depth_true.values, o), False, "The real seabed"), (grid(S.mean(1), o), True, "Rebuilt")]):
        ax = fig.add_axes([0.06 + k * 0.46, 0.13, 0.42, 0.74])
        ax.imshow(np.where(np.isnan(lag), np.nan, 1), origin="lower", extent=ext, cmap=ListedColormap(["#DCE4E4"]))
        ax.imshow(A, origin="lower", extent=ext, cmap=DEPTH_CMAP, vmin=0, vmax=10)
        gpd.GeoSeries([land]).plot(ax=ax, color=LAND, edgecolor="#A89F8C", linewidth=.6)
        if pts:
            ax.scatter(survey.x_km, survey.y_km, s=14, c=INK, edgecolors="white", linewidths=.5, zorder=4)
        ax.set_xlim(ext[0], ext[1]); ax.set_ylim(ext[2], ext[3]); ax.set_aspect("equal"); ax.axis("off")
        ax.set_title(title, fontsize=28, pad=14)
    fig.text(0.5, 0.045, caption, ha="center", fontsize=22, color="#3E3A33", linespacing=1.5)
    save(fig, "s08_texas_pair.png")
    # layers for the deck's animation: identical frame and extent, so pictures can sit on top of each other
    asp = (ext[1] - ext[0]) / (ext[3] - ext[2])
    for nm, A, kind in [("s08_layer_real.png", grid(o.depth_true.values, o), "real"), ("s08_layer_empty.png", None, "empty"),
                        ("s08_layer_rebuilt.png", grid(S.mean(1), o), "rebuilt"), ("s08_layer_dots.png", None, "dots")]:
        fig = plt.figure(figsize=(8 * asp, 8)); ax = fig.add_axes([0, 0, 1, 1])
        if kind != "dots":
            ax.imshow(np.where(np.isnan(lag), np.nan, 1), origin="lower", extent=ext, cmap=ListedColormap(["#DCE4E4"]))
            if A is not None:
                ax.imshow(A, origin="lower", extent=ext, cmap=DEPTH_CMAP, vmin=0, vmax=10)
            else:
                ax.add_patch(plt.Rectangle((ext[0], ext[2]), ext[1] - ext[0], ext[3] - ext[2], color="#E9E6DE", zorder=0))
            gpd.GeoSeries([land]).plot(ax=ax, color=LAND, edgecolor="#A89F8C", linewidth=.6)
        else:
            ax.scatter(survey.x_km, survey.y_km, s=34, c=INK, edgecolors="white", linewidths=.8, zorder=4)
        ax.set_xlim(ext[0], ext[1]); ax.set_ylim(ext[2], ext[3]); ax.axis("off")
        fig.savefig(OUT / nm, dpi=100, transparent=(kind == "dots"), facecolor="none" if kind == "dots" else PAPER); plt.close(fig)
        note(nm, 8, "data", f"animation layer ({kind}): same frame for all four layers", "validation_bathymetry.ipynb, survey rep_0, model F; NOAA CUDEM")
    (OUT / "s08_caption.txt").write_text(caption.replace("\n", " "))
    note("s08_texas_pair.png", 8, "data",
         f"the real and rebuilt seabeds side by side, same scale, with the fit for this survey in words (RMSE: open water {rmse['open']:.2f} m, "
         f"along the shore {rmse['shore']:.2f} m, inlet {rmse['inlet']:.2f} m)", "validation_bathymetry.ipynb, survey rep_0, model F; NOAA CUDEM")


# ---- slide 9b: the Kodungallur mouth, top down, ship water and distance ----------------------------------
NEED = 3.5     # 3 m draught + 0.5 m clearance
from matplotlib.colors import BoundaryNorm
TWO_TONE = ListedColormap([SHALLOW, DEEP]); TWO_NORM = BoundaryNorm([0, 0.9, 1.0001], 2)


def site_twotone(site):
    D = COAST / "data/soundings" / site / "model"; g = pd.read_csv(D / "grid.csv")
    S = np.fromfile(D / "samples.bin", dtype=np.float32).reshape(len(g), -1)
    ok = (S > NEED).mean(1); step = 0.1                                   # probability; drawn with a threshold at 0.9
    i = np.round((g.x_km - g.x_km.min()) / step).astype(int); j = np.round((g.y_km - g.y_km.min()) / step).astype(int)
    A = np.full((j.max() + 1, i.max() + 1), np.nan); A[j, i] = ok.astype(float)
    ext = [g.x_km.min() - step / 2, g.x_km.max() + step / 2, g.y_km.min() - step / 2, g.y_km.max() + step / 2]
    meta = json.loads((D / "site.json").read_text()); land = gpd.read_file(D / "land.geojson").geometry[0]
    # the seaward corridor used in seabed_mouths.ipynb, to draw the distance
    ref = np.array(meta["ref"]); xy = g[["x_km", "y_km"]].values; mean = S.mean(1)
    ring = np.where((g.d_ref_km > 3.5) & (g.d_ref_km < 4.5))[0]; tgt = xy[ring[np.argmax(mean[ring])]]
    u = (tgt - ref) / np.hypot(*(tgt - ref))
    return A, ext, land, meta, ref, u


def s09b():
    A, ext, land, meta, ref, u = site_twotone("kodungallur")
    dist = pd.read_csv(COAST / "data/soundings/mouths_comparison.csv", index_col=0).loc["kodungallur", "anchorage, 3 m draught: P>=0.9 (km)"]
    fig = plt.figure(figsize=(10.8, 10.8)); ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(A, origin="lower", extent=ext, cmap=TWO_TONE, norm=TWO_NORM, interpolation="bilinear", interpolation_stage="data")
    gpd.GeoSeries([land]).plot(ax=ax, color=LAND, edgecolor="#A89F8C", linewidth=.8)
    p1 = ref + u * dist
    ax.annotate("", xy=p1, xytext=ref, arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=3, mutation_scale=28))
    ax.plot(*ref, "o", color=ACCENT, ms=14, mec="white", mew=2)
    ax.text(*(ref + u * dist / 2 + np.array([0.15, 0.35])), f"{dist:.1f} km", color=ACCENT, fontsize=34, fontweight="bold",
            path_effects=[__import__("matplotlib.patheffects", fromlist=["x"]).withStroke(linewidth=5, foreground="white")])
    side = ext[1] - ext[0]                                                # square: the box's full width, centred below the mouth
    ax.set_xlim(ext[0], ext[1]); ax.set_ylim(ref[1] - side * 0.62, ref[1] + side * 0.38); ax.set_aspect("equal"); ax.axis("off")
    save(fig, "s09b_ship_water_map.png")
    note("s09b_ship_water_map.png", 9, "data",
         f"Kodungallur mouth from above: blue where water is at least 3.5 m deep with probability >= 0.9 (3 m draught + 0.5 m), sand where not; arrow {dist:.1f} km from the mouth to that water along the seaward corridor",
         "seabed_mouths.ipynb (model F); data/soundings/mouths_comparison.csv")


# ---- slide 10: the whole coast ----------------------------------------------------------------------------
SITE_LABEL = {"kodungallur": ("Kodungallur", "Muziris"), "ponnani": ("Ponnani", "Tyndis"), "tanur": ("Tanur", "Tyndis"),
              "beypore": ("Beypore", "Tyndis"), "koyilandy": ("Koyilandy", "Tyndis"), "kollam": ("Kollam", "Nelkynda / Bakarē"),
              "purakkad": ("Purakkad", "Nelkynda / Bakarē")}


def s10():
    from pyproj import Transformer
    from matplotlib.patches import ConnectionPatch
    ocean = gpd.read_file(ROOT / "data/raw/ne10m/ne_10m_ocean.shp").clip((74.6, 8.3, 77.6, 11.9))
    inv = Transformer.from_crs("EPSG:32643", "EPSG:4326", always_xy=True)
    cmp_ = pd.read_csv(COAST / "data/soundings/mouths_comparison.csv", index_col=0)
    order = ["koyilandy", "beypore", "tanur", "ponnani", "kodungallur", "purakkad", "kollam"]      # north to south
    pos = {}
    for sname in order:
        meta = json.loads((COAST / "data/soundings" / sname / "model/site.json").read_text())
        pos[sname] = inv.transform(meta["ref"][0] * 1000, meta["ref"][1] * 1000)
    layout = {}
    for name, with_insets in [("s10a_coast_map.png", False), ("s10b_coast_map_insets.png", True), ("s10c_coast_map_dots.png", None)]:
        fig = plt.figure(figsize=W169)
        axm = fig.add_axes([0.40, 0.03, 0.30, 0.94])
        axm.add_patch(plt.Rectangle((75.2, 8.6), 1.7, 3.1, color=LAND, zorder=0))
        ocean.plot(ax=axm, color="#CFE0E3", edgecolor="#8FA9AE", linewidth=.8, zorder=1)
        axm.text(75.45, 9.6, "Arabian Sea", fontsize=20, color="#6F8F95", style="italic", rotation=90, zorder=2)
        for sname in order:
            x, y = pos[sname]; axm.plot(x, y, "o", color=ACCENT, ms=11, mec="white", mew=2, zorder=5)
            if with_insets is False:
                axm.text(x + .06, y, f"{SITE_LABEL[sname][0]}", fontsize=17, va="center", zorder=6)
        axm.set_xlim(75.2, 76.9); axm.set_ylim(8.6, 11.7); axm.set_aspect(1 / np.cos(np.radians(10.2))); axm.axis("off")
        if with_insets:
            slots = [(0.04, 0.80), (0.04, 0.55), (0.04, 0.30), (0.04, 0.05), (0.73, 0.62), (0.73, 0.35), (0.73, 0.08)]
            for (sx, sy), sname in zip(slots, order):
                A, ext, land, meta, ref, u = site_twotone(sname)
                ai = fig.add_axes([sx, sy, 0.23, 0.18])
                ai.imshow(A, origin="lower", extent=ext, cmap=TWO_TONE, norm=TWO_NORM, interpolation="bilinear", interpolation_stage="data")
                gpd.GeoSeries([land]).plot(ax=ai, color=LAND, edgecolor="#A89F8C", linewidth=.5)
                ai.plot(*ref, "o", color=ACCENT, ms=7, mec="white", mew=1.5)
                half = 3.0; ai.set_xlim(ref[0] - 2 * half, ref[0] + half * 0.8); ai.set_ylim(ref[1] - half, ref[1] + half)
                ai.set_aspect("equal"); ai.set_xticks([]); ai.set_yticks([]); ai.set_xlabel(""); ai.set_ylabel(""); ai.set_facecolor(PAPER)
                for sp in ai.spines.values(): sp.set_color("#A89F8C")
                d3 = cmp_.loc[sname, "anchorage, 3 m draught: P>=0.9 (km)"]
                ai.set_title(f"{SITE_LABEL[sname][0]}  ({SITE_LABEL[sname][1]})   {d3:.1f} km", fontsize=14, loc="left", pad=4)
                side = "right" if sx < 0.4 else "left"
                xa = (1.0 if sx < 0.4 else 0.0, 0.5)
                fig.add_artist(ConnectionPatch(xyA=xa, coordsA=ai.transAxes, xyB=pos[sname], coordsB=axm.transData, color="#B9B0A0", lw=.8, alpha=.8))
                layout[sname] = dict(slot=[sx, sy, 0.23, 0.18])
        if with_insets is None:                                   # record the dots in figure fractions for the deck
            fig.canvas.draw(); tr = axm.transData + fig.transFigure.inverted()
            for sname in order:
                layout.setdefault(sname, {})["dot"] = [float(v) for v in tr.transform(pos[sname])]
        save(fig, name)
    # each inset on its own, for the deck to animate (title band 0.36 in above the 1.944 in map)
    for (sx, sy), sname in zip([(0.04, 0.80), (0.04, 0.55), (0.04, 0.30), (0.04, 0.05), (0.73, 0.62), (0.73, 0.35), (0.73, 0.08)], order):
        A, ext, land, meta, ref, u = site_twotone(sname)
        MH_IN = 0.18 * 10.8; MW_IN = MH_IN * 7.8 / 6.0; TB = 0.55                    # map 7.8 x 6 km at true scale; title band
        fig = plt.figure(figsize=(MW_IN, MH_IN + TB)); ai = fig.add_axes([0, 0, 1, MH_IN / (MH_IN + TB)])
        ai.imshow(A, origin="lower", extent=ext, cmap=TWO_TONE, norm=TWO_NORM, interpolation="bilinear", interpolation_stage="data")
        gpd.GeoSeries([land]).plot(ax=ai, color=LAND, edgecolor="#A89F8C", linewidth=.5)
        ai.plot(*ref, "o", color=ACCENT, ms=7, mec="white", mew=1.5)
        half = 3.0; ai.set_xlim(ref[0] - 2 * half, ref[0] + half * 0.8); ai.set_ylim(ref[1] - half, ref[1] + half)
        ai.set_aspect("equal", anchor="W"); ai.set_xticks([]); ai.set_yticks([]); ai.set_xlabel(""); ai.set_ylabel(""); ai.set_facecolor(PAPER)
        for sp in ai.spines.values(): sp.set_color("#A89F8C")
        d3 = cmp_.loc[sname, "anchorage, 3 m draught: P>=0.9 (km)"]
        fig.text(0.0, 0.98, SITE_LABEL[sname][0], fontsize=14, va="top")
        fig.text(0.0, 0.98 - 0.24 / (MH_IN + TB), f"{SITE_LABEL[sname][1]}  ·  {d3:.1f} km", fontsize=10.5, va="top", color="#6E665A", style="italic")
        save(fig, f"s10_inset_{sname}.png")
        layout[sname].update(w_in=MW_IN, map_h_in=MH_IN, title_in=TB)
        note(f"s10_inset_{sname}.png", 10, "data", f"{SITE_LABEL[sname][0]}: the two-tone seabed inset on its own, for the deck's Morph", "seabed_mouths.ipynb (model F)")
    (OUT / "s10_layout.json").write_text(json.dumps(dict(order=order, label={k: SITE_LABEL[k][0] for k in order}, sites=layout), indent=1))
    note("s10c_coast_map_dots.png", 10, "data", "the coast map with the seven mouths as dots and nothing else; the deck adds labels and insets as separate objects", "Natural Earth; data/soundings/<site>/model/site.json")
    note("s10a_coast_map.png", 10, "data", "the Malabar coast (Natural Earth 10 m ocean) with the seven surveyed mouths", "Natural Earth; site positions from data/soundings/<site>/model/site.json")
    note("s10b_coast_map_insets.png", 10, "data",
         "the same map with each mouth's two-tone seabed (blue: >= 3.5 m with probability >= 0.9; sand: shallower) and the distance from the mouth or shore to that water. Surveys: Selby 1850-3 (five sites), chart 64 1887 (Beypore, Koyilandy). Insets share one scale (9 x 6 km)",
         "seabed_mouths.ipynb (model F); data/soundings/mouths_comparison.csv")


# ---- slide 12: the turnaround timeline (three morph frames) ----------------------------------------------
def s12():
    import datetime as dt
    from matplotlib import patheffects as pe
    D = lambda m, d: (dt.date(2001 if m < 6 else 2000, m, d) - dt.date(2000, 7, 1)).days       # days from 1 July
    months = [("Jul", 7), ("Aug", 8), ("Sep", 9), ("Oct", 10), ("Nov", 11), ("Dec", 12), ("Jan", 1), ("Feb", 2)]

    def frame(stage, name):
        fig = plt.figure(figsize=W169); ax = fig.add_axes([0.05, 0.12, 0.90, 0.72]); ax.set_xlim(-5, D(2, 28) + 5); ax.set_ylim(0, 10); ax.axis("off")
        for lab, m in months:
            x = D(m, 1); ax.plot([x, x], [1.0, 1.4], color="#9A9184", lw=1.2); ax.text(x + 14, 0.5, lab, ha="center", fontsize=20, color="#6E665A")
        ax.plot([0, D(2, 28)], [1.2, 1.2], color="#9A9184", lw=1.5)
        lane = dict(sea=8.0, port=5.4)
        ax.plot([D(9, 28)] * 2, [1.4, 9.4], color="#9A9184", lw=1, ls=":")
        # voyage
        ax.add_patch(plt.Rectangle((D(7, 20), lane["sea"] - .45), D(9, 28) - D(7, 20), .9, color=DEEP, alpha=.85))
        ax.text(D(7, 20) + 2, lane["sea"] + .8, "Leave Egypt  ~20 July", fontsize=19, ha="left")
        ax.text((D(7, 20) + D(9, 28)) / 2, lane["sea"], "~70 days at sea", fontsize=19, ha="center", va="center", color="white")
        ax.text(D(9, 28) + 2, lane["sea"] + .8, "Arrive  ~28 Sept", fontsize=19, ha="left")
        ax.text(D(7, 20) + 2, lane["sea"] - 1.2, "Periplus 56;  Pliny NH 6.104", fontsize=13, color="#7A7266", style="italic")
        if stage >= 2:
            ax.add_patch(plt.Rectangle((0, lane["port"] - .45), D(9, 15), .9, color="#B9B0A0", alpha=.55, hatch="///", ec="#9A9184"))
            ax.text(D(9, 15) / 2, lane["port"], "coast closed to sailing ships", fontsize=17, ha="center", va="center", color="#5E574C")
            ax.text(2, lane["port"] - 1.2, "1909 Admiralty Pilot (Cochin: closed 15 May – 15 Sept)", fontsize=13, color="#7A7266", style="italic")
            ax.add_patch(plt.Rectangle((D(9, 28), lane["port"] - .45), D(1, 13) - D(9, 28), .9, color=SHALLOW, ec="#BFA968"))
            ax.text((D(9, 28) + D(1, 13)) / 2, lane["port"] + .8, "In port  70–107 days", fontsize=19, ha="center")
        if stage >= 3:
            ax.add_patch(plt.Rectangle((D(9, 28), lane["port"] - .45), 21, .9, color=ACCENT, alpha=.85))
            ax.text(D(9, 28) + 2, lane["port"] - 1.1, "loading: days to ~3 weeks", fontsize=16, color=ACCENT)
            ax.text((D(10, 25) + D(1, 13)) / 2, lane["port"], "waiting for the wind", fontsize=17, ha="center", va="center", color="#6E5E2E")
            ax.add_patch(plt.Rectangle((D(12, 8), lane["sea"] - .45), D(1, 13) - D(12, 8), .9, color=DEEP, alpha=.85))
            ax.text((D(12, 8) + D(1, 13)) / 2, lane["sea"] + .8, "Leave 8 Dec – 13 Jan", fontsize=19, ha="center")
            ax.text((D(12, 8) + D(1, 13)) / 2, lane["sea"] - 1.2, "Pliny NH 6.106", fontsize=13, color="#7A7266", style="italic", ha="center")
            ax.add_patch(plt.Rectangle((D(11, 1), 2.2), D(2, 28) - D(11, 1), .6, color="#6B8E4E", alpha=.55))
            ax.text(D(2, 28), 3.05, "pepper harvest (plains), Nov – Feb", fontsize=15, color="#4E6B37", ha="right")
        save(fig, name)
    frame(1, "s12a_turnaround_voyage.png"); frame(2, "s12b_turnaround_stay.png"); frame(3, "s12c_turnaround_full.png")
    src = ("Periplus 56 and Pliny NH 6.104 (departure, about 20 July, De Romanis 2014: 81); Pliny NH 6.104 (30 + 40 days, so arrival about 28 Sept); "
           "1909 Admiralty West Coast of India Pilot p. 128 (Cochin bar closed 15 May - 15 Sept); Pliny NH 6.106 (depart Tybi 1 - Mechir 6 = 8 Dec - 13 Jan, De Romanis 2014: 81-83); "
           "loading time: the project's estimate, sites/malabar/analysis/turnaround.md section 8b (1-21 days on most assumptions); pepper harvest Nov-Feb: turnaround.md section 6")
    note("s12a_turnaround_voyage.png", 12, "data", "timeline frame 1: the outward voyage", src)
    note("s12b_turnaround_stay.png", 12, "data", "frame 2: adds the closed coast and the stay", src)
    note("s12c_turnaround_full.png", 12, "data", "frame 3: adds loading, waiting, the departure window and the pepper harvest", src)
    # the wharf photographs (PAMA catalogue pp. 120-121)
    import pymupdf
    doc = pymupdf.open(MAL / "readings/supplementary/PAMA-Unearthing-Pattanam-Excavation-Catalogue.pdf")
    for xref, name, what in [(1333, "s12d_pattanam_wharf_canoe.jpg", "the dugout canoe in the waterlogged wharf deposit"),
                             (1335, "s12e_pattanam_wharf_lining.jpg", "the brick lining of the wharf")]:
        pix = pymupdf.Pixmap(doc, xref)
        if pix.n - pix.alpha > 3: pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
        pix.save(str(OUT / name.replace(".jpg", ".png")))
        Image.open(OUT / name.replace(".jpg", ".png")).convert("RGB").save(OUT / name, quality=92); (OUT / name.replace(".jpg", ".png")).unlink()
        note(name, 12, "published", f"Pattanam: {what}", "Cherian and Menon (eds), Unearthing Pattanam: Histories, Cultures, Crossings (PAMA catalogue, National Museum, New Delhi, 2014), pp. 120-121")


# ---- object images, copied onto matching canvases (published figures) ----------------------------------
OBJ = MAL / "analysis/figures/objects"
OBJ_SRC = {   # provenance from sites/malabar/analysis/scripts/crop_figures.py
    "13_red_sea_crsw_fig6": "Tomber, Indo-Roman Trade: From Pots to Pepper (2008), fig. 6 (book PDF p. 49): Indian coarse red-slipped cooking wares from the Egyptian Red Sea ports",
    "13b_myos_hormos_graffiti_fig13": "Tomber 2008, fig. 13 (PDF p. 77): Tamil-Brahmi graffiti from Myos Hormos",
    "07_pattanam_dressel24_fig5": "Shajan, Tomber, Selvakumar and Cherian 2004, 'Locating the ancient port of Muziris', JRA 17, fig. 5 (PDF p. 7): Dressel 2-4 amphora, Pattanam",
    "08b_pattanam_sigillata_stamp_closeup": "Cherian and Menon (eds), Unearthing Pattanam (2014), PDF p. 28: stamped terra sigillata, Pattanam",
    "14_pattanam_rw_pama": "Unearthing Pattanam (2014), PDF p. 50: Rouletted Ware, Pattanam",
    "01_sumhuram_rw_fig3": "Pavan and Schenk 2012, 'Crossing the Indian Ocean before the Periplus', AAE 23, fig. 3 (PDF p. 9): Rouletted Ware, Sumhuram",
    "01b_tissa_rw_early_late_fig6": "Pavan and Schenk 2012, fig. 6 (PDF p. 9): early and late Rouletted Ware, Tissamaharama",
    "11_pattanam_torpedo_lined": "Unearthing Pattanam (2014), PDF p. 32: torpedo jar sherd with bitumen lining, Pattanam",
    "10_pattanam_tgp_ringbase": "Unearthing Pattanam (2014), PDF p. 34: turquoise glazed ring base, Pattanam",
}


def object_card(src_key, name, slide, size=(1200, 900)):
    im = Image.open(OBJ / f"{src_key}.png").convert("RGB")
    c = Image.new("RGB", size, PAPER); im.thumbnail((size[0] - 60, size[1] - 60), Image.LANCZOS)
    c.paste(im, ((size[0] - im.width) // 2, (size[1] - im.height) // 2)); c.save(OUT / name, quality=94)
    note(name, slide, "published", OBJ_SRC[src_key].split(": ", 1)[-1], OBJ_SRC[src_key].split(": ")[0])


def s13():
    for k, (key, nm) in enumerate([("13_red_sea_crsw_fig6", "s13a_redsea_indian_cooking_ware.jpg"),
                                   ("13b_myos_hormos_graffiti_fig13", "s13b_myos_hormos_tamil_graffiti.jpg"),
                                   ("07_pattanam_dressel24_fig5", "s13c_pattanam_dressel24_amphora.jpg"),
                                   ("08b_pattanam_sigillata_stamp_closeup", "s13d_pattanam_sigillata_stamp.jpg")]):
        object_card(key, nm, 13)
    tamil_poems_map()


# ---- slide 13: where the Tamil poems put foreigners, on a real terrain map ------------------------------
TAMIL_FONT = "/System/Library/Fonts/Supplemental/Tamil Sangam MN.ttc"
SERIF = "/System/Library/Fonts/Supplemental/Georgia.ttf"
SERIF_B = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
SERIF_I = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
# Tamil from Vaidehi Herbert's editions (sangamtranslationsbyvaidehi.com, saved in sites/malabar/readings/tamil/web/);
# the PDF text layer dropped some vowel signs, which are restored here. Check against a printed edition.
POEMS = [
    dict(key="muciri", lon=76.20, lat=10.17, place="Muciṟi", gloss="Yavana ships arrive and leave",
         tamil=["யவனர் தந்த வினைமாண் நன்கலம்", "பொன்னொடு வந்து கறியொடு பெயரும்", "வளங்கெழு முசிறி"],
         english=["… the fine ships of the Yavanas", "come with gold and leave with pepper,", "the wealthy Musiri …"],
         cite="Akanāṉūṟu 149.9–11, trans. Vaidehi Herbert", card=(60, 330), note="location disputed"),
    dict(key="madurai", lon=78.12, lat=9.925, place="Madurai", gloss="the Pandya court: Yavana wine, guards, lamps",
         tamil=["யவனர் நன்கலம் தந்த தண் கமழ் தேறல்"],
         english=["fragrant wine brought in fine ships", "by the Yavanas"],
         cite="Puṟanāṉūṟu 56.18, trans. Vaidehi Herbert", card=(1010, 760), note=None),
    dict(key="puhar", lon=79.855, lat=11.14, place="Puhar", gloss="the only place foreigners are said to dwell",
         tamil=["மொழி பல பெருகிய பழி தீர் தேஎத்துப்", "புலம் பெயர் மாக்கள் கலந்து இனிது உறையும்"],
         english=["People from many nations with various", "languages living together sweetly"],
         cite="Paṭṭiṉappālai 216–17, trans. Vaidehi Herbert", card=(1300, 30), note=None),
]


def tamil_poems_map():
    from PIL import ImageFont, ImageFilter
    from scipy import ndimage
    W0, S0, E0, N0, PPD = 73.5, 7.5, 81.5, 13.6, 120
    dem = np.load(ROOT / "data/cache/presentation/south_india_dem_120ppd.npy")
    lon0, lon1, lat0, lat1 = 71.9, 82.6, 7.55, 13.45                       # 16:9 at this latitude
    Wpx, Hpx = 1920, 1080
    kx = Wpx / (lon1 - lon0); ky = Hpx / (lat1 - lat0)
    P = lambda lon, lat: ((lon - lon0) * kx, (lat1 - lat) * ky)
    # terrain: hillshade on muted hypsometric tints, sea flat
    z = np.nan_to_num(dem, nan=0.0); land = np.isfinite(dem) & (dem > 0.5)
    gy, gx = np.gradient(z, 1000 / PPD * 110 / 1000)                      # metres per pixel, roughly
    az, alt = np.radians(315), np.radians(40)
    slope = np.arctan(np.hypot(gx, gy) * 0.004); aspect = np.arctan2(-gx, gy)
    hs = np.clip(np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - aspect), 0, 1)
    tints = np.array([[0, (233, 226, 208)], [300, (222, 212, 186)], [900, (204, 190, 160)], [1800, (185, 168, 140)]], dtype=object)
    hz = [t[0] for t in tints]; rgb = np.zeros(z.shape + (3,))
    for c in range(3):
        rgb[..., c] = np.interp(z, hz, [t[1][c] for t in tints])
    rgb = rgb * (0.72 + 0.28 * hs[..., None])
    sea = np.array([214, 227, 230.]); rgb[~land] = sea
    terr = Image.fromarray(rgb.clip(0, 255).astype("uint8"))
    # place the DEM raster on the canvas
    canvas = Image.new("RGB", (Wpx, Hpx), tuple(int(v) for v in sea))
    x0, y0 = P(W0, N0); x1, y1 = P(E0, S0)
    canvas.paste(terr.resize((int(x1 - x0), int(y1 - y0)), Image.LANCZOS), (int(x0), int(y0)))
    d = ImageDraw.Draw(canvas)
    # rivers and coast
    riv = gpd.read_file(ROOT / "data/raw/hydrorivers/HydroRIVERS_v10_as_shp/HydroRIVERS_v10_as.shp", bbox=(W0, S0, E0, N0))
    riv = riv[riv.UPLAND_SKM > 1500]
    for g, up in zip(riv.geometry, riv.UPLAND_SKM):
        w = 1 if up < 6000 else (2 if up < 30000 else 3)
        for line in getattr(g, "geoms", [g]):
            d.line([P(*c) for c in line.coords], fill=(120, 158, 172), width=w)
    coast = gpd.read_file(ROOT / "data/raw/ne10m/ne_10m_coastline.shp", bbox=(lon0, lat0, lon1, lat1))
    for g in coast.geometry:
        for line in getattr(g, "geoms", [g]):
            d.line([P(*c) for c in line.coords], fill=(122, 140, 144), width=2)
    base = canvas.copy()
    f_place = ImageFont.truetype(SERIF_B, 34); f_gloss = ImageFont.truetype(SERIF_I, 22); f_note = ImageFont.truetype(SERIF_I, 18)
    f_ta = ImageFont.truetype(TAMIL_FONT, 27, layout_engine=ImageFont.Layout.RAQM)
    f_en = ImageFont.truetype(SERIF, 24); f_cite = ImageFont.truetype(SERIF_I, 18)
    f_src = ImageFont.truetype(SERIF, 14)
    sea_names = [("Arabian Sea", 73.2, 9.0), ("Bay of Bengal", 81.3, 10.6)]

    def draw(im, poems):
        d = ImageDraw.Draw(im, "RGBA")
        for name, lo, la in sea_names:
            d.text(P(lo, la), name, font=ImageFont.truetype(SERIF_I, 26), fill=(110, 136, 142), anchor="mm")
        for pm in poems:
            x, y = P(pm["lon"], pm["lat"])
            d.ellipse([x - 11, y - 11, x + 11, y + 11], fill=ACCENT, outline="white", width=3)
            cx, cy = pm["card"]
            lines = [(pm["place"], f_place, INK), (pm["gloss"], f_gloss, "#5E574C"), ("", f_note, INK)]
            lines += [(t, f_ta, INK) for t in pm["tamil"]] + [("", f_note, INK)]
            lines += [(t, f_en, INK) for t in pm["english"]] + [("", f_note, INK), (pm["cite"], f_cite, "#6E665A")]
            widths = [d.textlength(t, font=f) for t, f, _ in lines]
            heights = [f.size * 1.45 if t else 10 for t, f, _ in lines]
            bw, bh = max(widths) + 56, sum(heights) + 44
            d.rounded_rectangle([cx, cy, cx + bw, cy + bh], radius=6, fill=(250, 247, 240, 236), outline=(168, 158, 140, 255), width=2)
            yy = cy + 22
            for (t, f, col), h in zip(lines, heights):
                if t: d.text((cx + 28, yy), t, font=f, fill=col)
                yy += h
            # leader from the card edge to the dot
            ex = min(max(x, cx), cx + bw); ey = min(max(y, cy), cy + bh)          # nearest point on the card
            d.line([(ex, ey), (x, y)], fill=(150, 140, 122, 255), width=2)
            if pm["note"]:
                d.text((x + 16, y + 10), pm["note"], font=f_note, fill="#5E574C")
        d.text((Wpx - 16, Hpx - 14), "Terrain: Copernicus DEM GLO-90.  Rivers: HydroRIVERS.  Coast: Natural Earth.", font=f_src, fill=(110, 110, 110), anchor="rd")
        return im

    for k, nm in enumerate(["s13e_tamil_poems_muciri.png", "s13f_tamil_poems_madurai.png", "s13g_tamil_poems_puhar.png"]):
        draw(base.copy(), POEMS[:k + 1]).save(OUT / nm)
    srcs = "; ".join(f"{pm['cite']}" for pm in POEMS)
    note("s13e_tamil_poems_muciri.png", 13, "data", "Tamil poems frame 1: Muciri, with the Tamil, Herbert's translation and the line citation. Muciri's location is disputed; the dot marks the Periyar mouth region",
         "Tamil and translations: Vaidehi Herbert (saved in sites/malabar/readings/tamil/web/); some Tamil vowel signs restored where the PDF text dropped them, check against a printed edition; counts and readings: argument2_westerners_at_muziris.md section 1d (agent-read, to be hand-checked). " + srcs)
    note("s13f_tamil_poems_madurai.png", 13, "data", "frame 2: adds Madurai (Puṟanāṉūṟu 56, the Pandya court)", "as s13e")
    note("s13g_tamil_poems_puhar.png", 13, "data", "frame 3: adds Puhar, the only place foreigners are said to dwell (3 passages, all Puhar)", "as s13e")


# ---- time bars (arguments 1 and 3) ----------------------------------------------------------------------
def time_bar(rows, marks, xlim, ticks, name, show, title_left=None, fmt=lambda v: f"{-v} BC" if v < 0 else f"AD {v}"):
    from matplotlib import patheffects as pe
    fig = plt.figure(figsize=W169); ax = fig.add_axes([0.04, 0.06, 0.92, 0.86]); ax.set_xlim(*xlim); ax.set_ylim(-1.55, len(rows) + 0.3 + 0.4 * max(len(marks) - 1, 0)); ax.axis("off")
    for t in ticks:
        ax.plot([t, t], [-1.05, -0.85], color="#9A9184", lw=1.2); ax.text(t, -1.45, fmt(t), ha="center", fontsize=17, color="#6E665A")
    ax.plot(xlim, [-0.95, -0.95], color="#9A9184", lw=1.5)
    for i, (x, lab) in enumerate(marks):
        ax.plot([x, x], [-0.85, len(rows) - 0.2 + 0.4 * i], color="#9A9184", lw=1, ls=":")
        ax.text(x, len(rows) - 0.1 + 0.4 * i, lab, ha="center", fontsize=15, color="#6E665A", style="italic")
    for k, r in enumerate(rows):
        y = len(rows) - 1 - k
        if k not in show: continue
        a, b, col, label, cite = r["a"], r["b"], r["col"], r["label"], r["cite"]
        if b is None:
            ax.plot(a, y, "D", color=col, ms=14, mec="white", mew=1.5)
            x_text, ha = (a + (xlim[1] - xlim[0]) * 0.012, "left") if r.get("text_right", True) else (a - (xlim[1] - xlim[0]) * 0.012, "right")
        else:
            ax.add_patch(plt.Rectangle((a, y - 0.22), b - a, 0.44, color=col, alpha=r.get("alpha", .85), hatch=r.get("hatch"), ec=col))
            x_text, ha = (b + (xlim[1] - xlim[0]) * 0.008, "left") if r.get("text_right", True) else (a - (xlim[1] - xlim[0]) * 0.008, "right")
        ax.text(x_text, y + 0.05, label, fontsize=17, ha=ha, va="center")
        ax.text(x_text, y - 0.3, cite, fontsize=12, ha=ha, va="center", style="italic", color="#7A7266")
    save(fig, name)


NW, SOUTH, GREY = "#8A5A44", DEEP, "#A39C90"


def s14():
    rows = [dict(a=-300, b=-150, col=NW, label="Indian pottery at Mleiha, from Maharashtra and Gujarat", cite="Reddy 2013: 32"),
            dict(a=-200, b=-100, col=NW, label="Merchants from Patala (Indus) at Socotra", cite="Agatharchides, via Cobb 2023: 371"),
            dict(a=-116, b=None, col=GREY, label="Eudoxus guided to India by an Indian (origin not stated)", cite="Strabo 2.3.4; Casson 1989: 12"),
            dict(a=-50, b=200, col=GREY, label="Indian pottery at Qana, limited at first, rising later", cite="Avanzini 2014: 487; Reddy 2013: 134"),
            dict(a=-30, b=100, col=SOUTH, label="Indian fine wares at Berenike and Myos Hormos", cite="Tomber 2008: 74"),
            dict(a=-10, b=14, col=SOUTH, label="Myos Hormos Rouletted Ware: one late-Augustan deposit", cite="Tomber 2002, via Shoebridge 2017: 112–13"),
            dict(a=-30, b=200, col=SOUTH, label="Pattanam: no foreign ceramics before the late 1st c. BC", cite="Selvakumar, Shajan and Tomber 2010: 34; Tomber 2008: 142"),
            dict(a=50, b=200, col=GREY, label="Socotra: Indian graffiti from the 1st c. AD; none from Malabar", cite="Evers 2014–15: 31")]
    marks = [(-30, "Rome annexes Egypt, 30 BC"), (50, "Periplus, c. AD 50")]
    ticks = [-300, -200, -100, 1, 100, 200]
    fmt = lambda v: "AD 1" if v == 1 else (f"{-v} BC" if v < 0 else f"AD {v}")
    time_bar(rows, marks, (-340, 600), ticks, "s14a_crossing_axis.png", show=[], fmt=fmt)
    time_bar(rows, marks, (-340, 600), ticks, "s14b_crossing_northwest.png", show=[0, 1, 2], fmt=fmt)
    time_bar(rows, marks, (-340, 600), ticks, "s14c_crossing_south.png", show=list(range(8)), fmt=fmt)
    src = "sites/malabar/analysis/arabian_sea_crossing.md, tables A-D (each bar's citation is printed under it). Colours: brown, north-west India; blue, south India or the Red Sea finds; grey, India unspecified"
    for f, w in [("s14a_crossing_axis.png", "frame 1: axis and markers"), ("s14b_crossing_northwest.png", "frame 2: north-west India before Rome"),
                 ("s14c_crossing_south.png", "frame 3: south India and the Red Sea, from the late 1st c. BC")]:
        note(f, 14, "data", "argument 1 time bar, " + w, src)
    for key, nm in [("14_pattanam_rw_pama", "s14d_pattanam_rouletted_ware.jpg"), ("01_sumhuram_rw_fig3", "s14e_sumhuram_rouletted_ware.jpg"),
                    ("01b_tissa_rw_early_late_fig6", "s14f_tissamaharama_rouletted_ware.jpg")]:
        object_card(key, nm, 14)


def s15():
    ROM, GULF, MED, GAP = DEEP, "#8A5A44", "#6B8E4E", "#B9B0A0"
    rows = [dict(a=50, b=None, col=ROM, label="Periplus names Muziris", cite="c. AD 50"),
            dict(a=-90, b=125, col=ROM, label="Pattanam radiocarbon dates, Early Historic layer", cite="Cherian 2015: 747"),
            dict(a=150, b=None, col=ROM, label="Ptolemy: 'Mouziris, an emporium'", cite="Geography 7.1.8; McCrindle 1885: 48"),
            dict(a=224, b=800, col=GULF, alpha=.55, label="Gulf wares at Pattanam: torpedo jars, turquoise glaze", cite="Tomber 2007, 2010: 50; Cherian 2012: 27"),
            dict(a=550, b=None, col=GULF, label="Cosmas: five pepper marts of 'Male'; Muziris not among them", cite="McCrindle 1897: 365–7"),
            dict(a=849, b=None, col=MED, label="Kollam copper plates: Christian merchant guilds", cite="Narayanan, via secondary summaries"),
            dict(a=851, b=None, col=MED, label="Akhbār al-Ṣīn: Gulf ships sail to Kūlam (Kollam)", cite="Ferrand 1922: 39–40"),
            dict(a=844, b=1124, col=MED, label="Chera capital at Mahodayapuram (Kodungallur)", cite="Narayanan; Veluthat (secondary)", text_right=True),
            dict(a=1000, b=1500, col=GAP, hatch="//", label="Pattanam: signs of life 'even nil for five centuries'", cite="PAMA catalogue: 2–3, 16–17"),
            dict(a=1341, b=None, col=GAP, label="Periyar flood, traditional date; no contemporary record", cite="after_rome.md, landscape section"),
            dict(a=1435, b=None, col=MED, label="Ma Huan: Kochi the great pepper port", cite="Sastri 1939: 312"),
            dict(a=1516, b=None, col=MED, label="Barbosa: Cranganore, a mixed town under Cochin", cite="Dames 1921, vol. 2: 88–89")]
    for r in rows:
        if (r["b"] or r["a"]) > 1300: r["text_right"] = False
    marks = []
    ticks = [1, 250, 500, 750, 1000, 1250, 1500]
    fmt = lambda v: "AD 1" if v == 1 else f"{v}"
    for name, show, w in [("s15a_after_rome_roman.png", [0, 1, 2], "frame 1: the Roman horizon"),
                          ("s15b_after_rome_gulf.png", [0, 1, 2, 3, 4], "frame 2: adds the Gulf phase and Cosmas"),
                          ("s15c_after_rome_medieval.png", list(range(12)), "frame 3: adds the medieval shift north and south")]:
        time_bar(rows, marks, (-150, 1900), ticks, name, show=show, fmt=fmt)
        note(name, 15, "data", "argument 3 timeline, " + w,
             "sites/malabar/analysis/after_rome.md (each item's citation printed under it; the copper plates and the Chera dates are secondhand there)")
    object_card("11_pattanam_torpedo_lined", "s15d_pattanam_torpedo_jar.jpg", 15)
    object_card("10_pattanam_tgp_ringbase", "s15e_pattanam_turquoise_glaze.jpg", 15)


# ---- slide 17: Ed-Dur teaser (published figure) ---------------------------------------------------------
def s17():
    import pymupdf
    d = pymupdf.open(ROOT / "sites/ed-dur/readings/coastline/Forti-2024-CATENA-Umm-al-Quwain-lagoon.pdf")
    pg = d[3]; r = pg.rect
    clip = pymupdf.Rect(r.width * 0.11, r.height * 0.075, r.width * 0.885, r.height * 0.431)
    pg.get_pixmap(dpi=250, clip=clip).save(str(OUT / "s17_ed_dur_lagoon.png"))
    Image.open(OUT / "s17_ed_dur_lagoon.png").convert("RGB").save(OUT / "s17_ed_dur_lagoon.jpg", quality=93); (OUT / "s17_ed_dur_lagoon.png").unlink()
    note("s17_ed_dur_lagoon.jpg", 17, "published",
         "the Umm al-Quwain coastal-lagoon system (Google Earth 2023), Fig. 2A. Ed-Dur, about 4 km inland of the present coast (Forti et al. 2023, INQUA abstract), is not labelled in this figure",
         "Forti, Degli Esposti, Cremaschi, Borgi, Azzoni and Zerboni 2024, 'Geomorphological evolution of the Umm al-Quwain (UAE) coastal-lagoon system', Catena 247: 108517, Fig. 2A (p. 4)")


def write_manifest():
    rows = [r for r in json.loads((OUT / "manifest_rows.json").read_text()) if (OUT / r["file"]).exists()]
    rows.sort(key=lambda r: (r["slide"], r["file"]))
    titles = {1: "Title", 2: "Two port clusters on one sea", 4: "The 1857 survey of the Malabar coast", 5: "Reading the chart into data",
              6: "The soundings in 3D", 7: "The modelled seabed", 8: "Does it work?", 9: "Where an ancient ship could float",
              10: "The same pattern along the whole coast", 12: "Argument 2: the turnaround", 13: "Argument 2: who stayed",
              14: "Argument 1: when the crossing began", 15: "Argument 3: after Rome", 17: "Next: Ed-Dur"}
    out = ["# Visuals for 13 November 2026", "",
           "Generated by `presentation/scripts/make_nov13_visuals.py`. Every image is one of three kinds:", "",
           "- **archival**: a real chart, map or manuscript, cropped or annotated, never redrawn;",
           "- **published**: a figure from a cited publication, extracted from the PDF. Put the citation on the slide;",
           "- **data**: a plot made directly from the project's transcriptions, model outputs or dated evidence.", "",
           "Files ending a, b, c ... are morph sequences: same canvas and framing, meant for consecutive slides with",
           "PowerPoint's Morph or Fade. Slides 3, 11 and 16 are text only.", ""]
    for sl in sorted({r["slide"] for r in rows}):
        out += [f"## Slide {sl}. {titles.get(sl, '')}", "", "| File | Kind | What | Source |", "|---|---|---|---|"]
        for r in rows:
            if r["slide"] == sl:
                out.append(f"| `{r['file']}` | {r['kind']} | {r['what']} | {r['source']} |")
        out.append("")
    (OUT / "MANIFEST.md").write_text("\n".join(out))


def s09a_quote():
    from PIL import ImageFont
    mouth3d_fig(mouth3d_data(), "ship", domain_x=(0, 0.6), zoom=1.3).write_image(str(OUT / "_tmp_ship_left.png"), scale=1)
    base = Image.open(OUT / "_tmp_ship_left.png").convert("RGB"); (OUT / "_tmp_ship_left.png").unlink(); d = ImageDraw.Draw(base, "RGBA")
    f_la = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Italic.ttf", 38)
    f_en = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 30)
    f_ci = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Italic.ttf", 21)
    f_lg = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 24)
    x, y = 1170, 300
    latin = ["praeterea longe a terra", "abest navium statio,", "lintribusque adferuntur", "onera et egeruntur."]
    eng = ["“the roadstead for shipping is a long way", "from the land, and cargoes have to be", "brought in and carried out in boats.”"]
    d.line([(x - 26, y + 6), (x - 26, y + 410)], fill=ACCENT, width=4)
    for k, t in enumerate(latin): d.text((x, y + k * 50), t, font=f_la, fill=INK)
    for k, t in enumerate(eng): d.text((x, y + 230 + k * 42), t, font=f_en, fill="#3E3A33")
    d.text((x, y + 370), "Pliny, Natural History 6.104, on Muziris", font=f_ci, fill="#6E665A")
    d.text((x, y + 396), "Latin: Mayhoff 1906;  translation: H. Rackham", font=f_ci, fill="#6E665A")
    ly = y + 470
    for col, lab, k in [(DEEP, "deep enough for a 3 m draught (≥ 3.5 m, 90% sure)", 0), (SHALLOW, "too shallow", 1)]:
        yy = ly + k * 40; d.rectangle([x, yy, x + 34, yy + 24], fill=col, outline=(150, 140, 122)); d.text((x + 48, yy - 2), lab, font=f_lg, fill=INK)
    d.ellipse([x + 4, ly + 86, x + 28, ly + 110], fill=ACCENT, outline="white", width=3); d.text((x + 48, ly + 82), "the Kodungallur mouth", font=f_lg, fill=INK)
    base.save(OUT / "s09a2_ship_water_3d_pliny.png")
    note("s09a2_ship_water_3d_pliny.png", 9, "data", "s09a with Pliny's description of the Muziris roadstead and a legend; the next frame after s09a (same image underneath, so it fades in)",
         "Pliny, NH 6.104, Latin from Mayhoff's Teubner text (1906), translation H. Rackham (Loeb); quoted from sites/malabar/analysis/turnaround.md section 1; seabed as s09a")


# ---- slide 14: Rouletted Ware in its find contexts (three morph frames) --------------------------------------------
CONTEXTS = [
    dict(site="Tissamaharama", region="Sri Lanka", img="03_tissa_trench3b_fig6",
         layers=[("Phase c2  ·  1st c. BC", "single, worn sherds", False), ("Phase c1  ·  2nd c. BC", "mended vessels, joining pieces", True)],
         dated="its own layers, with radiocarbon", verdict="Early: used and broken where it lay",
         cite="Schenk 2014: 100–101, 113"),
    dict(site="Sumhuram", region="Oman", img="01_sumhuram_rw_fig3",
         layers=[("near the surface", "one sherd", None), ("a later stratum", "the decorated base", None),
                 ("oldest layers, mixed", "Indian pottery 'BC' with\namphorae of the 1st c. BC or AD", None)],
         dated="matching to Tissamaharama; no layer published", verdict="Borrowed date; the earliest layers hold Roman amphorae",
         cite="Pavan and Schenk 2012: 192–7; Avanzini 2014: 498"),
    dict(site="Myos Hormos", region="Egypt", img="16_myos_hormos_rw_fig5",
         layers=[("one deposit  ·  late Augustan", "16 sherds from 2 or 3 vessels", True)],
         dated="the deposit it lies in", verdict="Late: a late-Augustan deposit",
         cite="Tomber 2002: 28, via Shoebridge 2017: 112–13"),
    dict(site="Pattanam", region="Kerala", img="14_pattanam_rw_pama",
         layers=[("modern", "", None), ("medieval", "", None), ("Early Historic", "", None), ("Iron Age", "", None)],
         dated="nothing: found in every layer", verdict="No date of its own",
         cite="Sarathchandrababu 2022–23: 240; Selvakumar, Shajan and Tomber 2010: 34"),
]


def s14_contexts():
    from matplotlib.patches import FancyBboxPatch
    for stage, name in [(1, "s14g_contexts_objects.png"), (2, "s14h_contexts_layers.png"), (3, "s14i_contexts_dated.png")]:
        fig = plt.figure(figsize=W169)
        for k, c in enumerate(CONTEXTS):
            x0 = 0.03 + k * 0.243; w = 0.205
            wr = lambda t, n=36: "\n".join(textwrap.wrap(t, n))
            fig.text(x0, 0.955, c["site"], fontsize=24, va="top")
            fig.text(x0, 0.905, c["region"], fontsize=16, va="top", color="#6E665A", style="italic")
            ai = fig.add_axes([x0, 0.62, w, 0.25]); ai.axis("off")
            if c["img"]:
                ai.imshow(Image.open(MAL / "analysis/figures/objects" / f"{c['img']}.png").convert("RGB"))
            else:
                ai.set_xlim(0, 1); ai.set_ylim(0, 1)
                ai.add_patch(FancyBboxPatch((0.04, 0.08), 0.92, 0.84, boxstyle="round,pad=0.01", fc="#EEE8DC", ec="#CFC7B8"))
                ai.text(0.5, 0.5, "no image held", ha="center", va="center", fontsize=14, color="#9A9184", style="italic")
            if stage >= 2:                                      # the layer stack, top = latest
                al = fig.add_axes([x0, 0.25, w, 0.32]); al.set_xlim(0, 1); al.set_ylim(0, 1); al.axis("off")
                n = len(c["layers"]); hh = 0.92 / n
                for j, (lab, what, here) in enumerate(c["layers"]):
                    y = 0.96 - (j + 1) * hh
                    al.add_patch(plt.Rectangle((0, y), 1, hh - 0.02, fc="#E7DFCF" if j % 2 else "#EFE8DA", ec="#CFC7B8", lw=.8))
                    al.text(0.04, y + hh - 0.06, lab, fontsize=13, va="top")
                    if what: al.text(0.04, y + hh - 0.06 - 0.075 * (4 / max(n, 2)), what, fontsize=11, va="top", color="#5E574C", style="italic")
                    if c["site"] == "Pattanam":
                        al.plot(0.88, y + hh / 2 - 0.01, "o", ms=11, color=ACCENT, mec="white", mew=1.5)
                    elif here is True:
                        al.plot(0.88, y + hh / 2 - 0.01, "o", ms=13, color=ACCENT, mec="white", mew=1.5)
                    elif here is None and c["site"] == "Sumhuram" and j < 2:
                        al.text(0.88, y + hh / 2 - 0.01, "?", fontsize=22, color=ACCENT, ha="center", va="center", fontweight="bold")
                if c["site"] == "Pattanam":
                    al.text(0.5, -0.06, "in every layer: 'heavy disturbances'", fontsize=11, ha="center", va="top", color=ACCENT, style="italic")
            if stage >= 3:
                fig.text(x0, 0.175, "Dated by", fontsize=12, color="#6E665A", style="italic")
                fig.text(x0, 0.15, wr(c["dated"], 38), fontsize=13, va="top")
                fig.text(x0, 0.105, wr(c["verdict"], 30), fontsize=15, va="top", color=DEEP if "Early" in c["verdict"] else ACCENT, fontweight="bold", linespacing=1.15)
                fig.text(x0, 0.012, wr(c["cite"], 52), fontsize=9.5, color="#8A8275", style="italic")
        fig.text(0.985, 0.25 + 0.32 + 0.005, "", fontsize=1)
        if stage >= 2:
            fig.text(0.03, 0.592, "red: Rouletted Ware in that layer   ·   ?: layer not published", fontsize=11, color="#6E665A", style="italic")
        save(fig, name)
    src = ("sites/malabar/analysis/ceramics_and_ports.md (objects 1-3 and the dating-methods section) and arabian_sea_crossing.md, tables B-D; "
           "images: Schenk 2014 fig. 6; Pavan and Schenk 2012 fig. 3; Unearthing Pattanam (2014) p. 50. The layer stacks are schematic: only what the "
           "publications state is shown, and Sumhuram's unpublished layers are marked '?'")
    for f, w in [("s14g_contexts_objects.png", "frame 1: the Rouletted Ware at four sites"), ("s14h_contexts_layers.png", "frame 2: adds the layers each was found in"),
                 ("s14i_contexts_dated.png", "frame 3: adds what dates each, and the verdict")]:
        note(f, 14, "data", "argument 1 find contexts, " + w, src)


def s14_sherds():
    caps = {"Tissamaharama": "Rouletted Ware, Trench 3B\nSchenk 2014, fig. 6",
            "Sumhuram": "Rouletted Ware, three vessels\nPavan and Schenk 2012, fig. 3",
            "Myos Hormos": "Rouletted and related ware\nTomber 2008, fig. 5.1–2",
            "Pattanam": "Rouletted Ware\nUnearthing Pattanam (2014), p. 50"}
    fig = plt.figure(figsize=W169)
    for k, c in enumerate(CONTEXTS):
        x0 = 0.03 + k * 0.243; w = 0.215
        fig.text(x0, 0.93, c["site"], fontsize=28, va="top")
        fig.text(x0, 0.865, c["region"], fontsize=18, va="top", color="#6E665A", style="italic")
        ai = fig.add_axes([x0, 0.24, w, 0.56]); ai.axis("off")
        ai.imshow(Image.open(MAL / "analysis/figures/objects" / f"{c['img']}.png").convert("RGB"))
        fig.text(x0, 0.19, caps[c["site"]], fontsize=13, va="top", color="#5E574C", style="italic", linespacing=1.4)
    save(fig, "s14j_sherds.png")
    note("s14j_sherds.png", 14, "published", "argument 1: Rouletted Ware from the four sites, enlarged, one frame (the layers are spoken, not shown)",
         "Schenk 2014 fig. 6; Pavan and Schenk 2012 fig. 3; Tomber 2008 fig. 5 (nos 1-2 only); Unearthing Pattanam (2014) p. 50")


def s14_timeline():
    """Argument 1, the pottery on a date axis: north-west Indian pottery in Arabia before Rome, the south Indian
    route only from the late 1st c. BC. Each piece sits at the date of the deposit it was found in."""
    OBJ = MAL / "analysis/figures/objects"
    X0, X1, Y0, Y1 = -350, 170, 0.17, 0.97
    fx = lambda yr: Y0 + (yr - X0) / (X1 - X0) * (Y1 - Y0)
    NW, SO, MUTE = "#2F6F8F", ACCENT, "#6E665A"
    fig = plt.figure(figsize=W169)
    bg = fig.add_axes([0, 0, 1, 1]); bg.axis("off"); bg.set_xlim(0, 1); bg.set_ylim(0, 1)
    # axis
    ay = 0.10
    bg.plot([fx(X0), fx(X1)], [ay, ay], color=INK, lw=1.2)
    for yr, lab in [(-300, "300 BC"), (-200, "200 BC"), (-100, "100 BC"), (0, "BC | AD"), (100, "AD 100")]:
        bg.plot([fx(yr)] * 2, [ay, ay - 0.012], color=INK, lw=1.2)
        bg.text(fx(yr), ay - 0.025, lab, ha="center", va="top", fontsize=17, color=MUTE)
    # Rome in Egypt
    bg.plot([fx(-30)] * 2, [ay, 0.97], color=INK, lw=1.2, ls=(0, (4, 4)))
    bg.text(fx(-30) + 0.006, 0.965, "Egypt becomes Roman, 30 BC", fontsize=17, va="top", color=INK)
    bg.plot([0.02, 0.98], [0.565, 0.565], color="#CFC6B4", lw=1)
    bg.text(0.02, 0.93, "North-west India", fontsize=26, va="top", color=NW)
    bg.text(0.02, 0.52, "South India", fontsize=26, va="top", color=SO)

    def thumb(img, xc, ybot, w=None, h=None):
        im = Image.open(img).convert("RGB"); a = im.width / im.height
        if w is None: w = h * a * 1080 / 1920
        if h is None: h = w / a * 1920 / 1080
        ax = fig.add_axes([xc - w / 2, ybot, w, h]); ax.imshow(im); ax.axis("off")
        return xc - w / 2, xc + w / 2

    def mark(y, a, b, col):
        if b - a < 8: bg.plot([fx((a + b) / 2)], [y], "o", ms=13, color=col)
        else: bg.plot([fx(a), fx(b)], [y, y], color=col, lw=11, solid_capstyle="butt")

    # north-west: Mleiha, PIR.A
    mark(0.62, -300, -150, NW)
    l, r = thumb(OBJ / "17_mleiha_high_necked_fig213.png", fx(-225), 0.645, h=0.30)
    bg.text(r + 0.015, 0.80, "Mleiha, south-east Arabia", fontsize=19, va="bottom")
    bg.text(r + 0.015, 0.79, "Indian jars, clay from\nMaharashtra and Gujarat\n3rd – mid-2nd century BC",
            fontsize=15, va="top", color=MUTE, style="italic", linespacing=1.4)
    # south
    crop = lambda p, box: (Image.open(p).convert("RGB").crop(box))
    cp = SCRATCH_CROP = OUT / "_s14k_cooking.png"; crop(OUT / "s13a_redsea_indian_cooking_ware.jpg", (44, 130, 1166, 670)).save(cp)
    items = [(OBJ / "01_sumhuram_rw_fig3.png", -200, (-112, -108), 0.17, "Sumhuram, Oman", "Rouletted Ware\ndated late 2nd century BC"),
             (OBJ / "16_myos_hormos_rw_fig5.png", 22, (-10, 14), 0.19, "Myos Hormos, Egypt", "Rouletted Ware\nlate Augustan deposit"),
             (cp, 122, (-30, 100), 0.145, "Berenike and Myos Hormos", "Indian cooking pots\nlate 1st c. BC – 1st c. AD")]
    for img, slot, (a, b), ym, site, what in items:
        xc = fx(slot); thumb(img, xc, 0.36, w=0.14)
        bg.text(xc, 0.345, site, fontsize=17, ha="center", va="top")
        bg.text(xc, 0.31, what, fontsize=14, ha="center", va="top", color=MUTE, style="italic", linespacing=1.35)
        mark(ym, a, b, SO)
        bg.plot([xc, fx((a + b) / 2)], [0.245, ym + 0.015], color="#B9AE9A", lw=1)
    cp.unlink()
    save(fig, "s14k_crossing_pottery.png")
    note("s14k_crossing_pottery.png", 38, "published",
         "argument 1: Indian pottery on a date axis. North-west: Mleiha PIR.A high-necked jars (3rd - mid-2nd c. BC). South: "
         "Sumhuram Rouletted Ware (dated late 2nd c. BC by Tissamaharama), Myos Hormos Rouletted Ware (late Augustan deposit), "
         "Red Sea Indian cooking pots (Early Roman)",
         "Reddy 2013 fig. 213 after Mouton 2008 fig. 17, dates Reddy 2013: 32; Pavan and Schenk 2012 fig. 3, p. 196; "
         "Tomber 2008 fig. 5 and Shoebridge 2017: 112-113; Tomber 2008 fig. 6 and p. 74-75")


SLIDES = {"s00": s00_dividers, "s01": s01, "s02": s02, "s04": s04, "s05": s05, "s3d": s06_07_09_3d, "s08": s08, "s09b": s09b, "s10": s10, "s12": s12, "s13": s13, "s14": s14, "s15": s15, "s14x": s14_contexts, "s14s": s14_sherds, "s17": s17, "s09q": s09a_quote, "s14t": s14_timeline}

if __name__ == "__main__":
    for k in (sys.argv[1:] or SLIDES):
        SLIDES[k](); print("done", k)
    mf = OUT / "manifest_rows.json"
    old = json.loads(mf.read_text()) if mf.exists() else []
    files = {r["file"] for r in MANIFEST}
    mf.write_text(json.dumps([r for r in old if r["file"] not in files] + MANIFEST, indent=1))
    write_manifest()

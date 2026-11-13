"""Build presentation/nov_13th/nov13_malabar.pptx from the visuals in presentation/nov_13th/.

Layout. Every slide has the same grid: a Georgia headline top-left on the plain paper background (nothing behind
it), a short brick-red rule under it, every visual in the area below the headline, the source line bottom-left
and the slide number bottom-right. Speaker notes carry the talk track.

Transitions are chosen per slide:
  morph  only where an object carries on from the previous slide and its change means something: the zooms
         (one picture, re-cropped), chart -> soundings -> points, the 3D seabed recolouring, the build-ups of a
         single graphic (timelines, Tamil map, coast insets), and the agenda tree's highlight moving
  fade   between unrelated slides
Morph pairs objects whose names start with "!!" and match on consecutive slides.
python-pptx cannot write a slide master, so the theme is applied slide by slide in fixed positions.
"""
import pathlib
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
ROOT = pathlib.Path(__file__).resolve().parents[2]
V = ROOT / "presentation" / "nov_13th"
OUT = V / "nov13_malabar.pptx"

SW, SH = 13.333, 7.5
PAPER = RGBColor(0xF4, 0xEF, 0xE6); INK = RGBColor(0x2B, 0x2B, 0x2B); GREY = RGBColor(0x6E, 0x66, 0x5A)
PALE = RGBColor(0xA8, 0x9F, 0x8C); FAINT = RGBColor(0xCF, 0xC7, 0xB8); CARD = RGBColor(0xFA, 0xF7, 0xF0)
RED = RGBColor(0xB5, 0x43, 0x2F); FONT = "Georgia"
M = 0.55
BODY_TOP, BODY_H = 1.5, 5.5                         # the visual area below the headline
BODY_W = BODY_H * 16 / 9; BODY_X = (SW - BODY_W) / 2

prs = Presentation(); prs.slide_width = Inches(SW); prs.slide_height = Inches(SH)
BLANK = prs.slide_layouts[6]
N = [0]

# ---- transitions ----------------------------------------------------------------------------------------------
NS = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main"}
P_NS = 'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
MORPH_XML = ('<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" ' + P_NS + '>'
             '<mc:Choice xmlns:p159="http://schemas.microsoft.com/office/powerpoint/2015/09/main" Requires="p159">'
             '<p:transition xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" spd="slow" p14:dur="1400">'
             '<p159:morph option="byObject"/></p:transition></mc:Choice>'
             '<mc:Fallback><p:transition spd="slow"><p:fade/></p:transition></mc:Fallback></mc:AlternateContent>')
FADE_XML = '<p:transition ' + P_NS + ' spd="med"><p:fade/></p:transition>'


def transition(slide, kind):
    if kind is None: return
    el = etree.fromstring(MORPH_XML if kind == "morph" else FADE_XML)
    anchor = slide._element.find("p:clrMapOvr", NS)
    (anchor if anchor is not None else slide._element.find("p:cSld", NS)).addnext(el)


# ---- primitives -------------------------------------------------------------------------------------------------
def text(slide, x, y, w, h, runs, size=14, color=INK, italic=False, align=PP_ALIGN.LEFT, name=None,
         anchor=MSO_ANCHOR.TOP, spacing=1.1):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); tf = tb.text_frame
    tf.word_wrap = True; tf.vertical_anchor = anchor
    for a in ("margin_left", "margin_right", "margin_top", "margin_bottom"): setattr(tf, a, 0)
    for i, ptxt in enumerate(runs if isinstance(runs, list) else [runs]):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); p.alignment = align; p.line_spacing = spacing
        r = p.add_run(); r.text = ptxt; f = r.font; f.name = FONT; f.size = Pt(size); f.color.rgb = color; f.italic = italic
    if name: tb.name = name
    return tb


def rule(s, x, y, w=0.9, name="!!rule"):
    r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(0.035)); r.name = name
    r.fill.solid(); r.fill.fore_color.rgb = RED; r.line.fill.background(); return r


def new_slide(title, notes, source=None, trans="fade"):
    s = prs.slides.add_slide(BLANK); N[0] += 1
    s.background.fill.solid(); s.background.fill.fore_color.rgb = PAPER
    s.notes_slide.notes_text_frame.text = "\n".join(f"• {n}" for n in notes)
    if title:
        text(s, M, 0.34, SW - 2 * M, 0.8, title, size=24, name="!!title", spacing=1.0)
        rule(s, M, 1.24)
    if source:
        text(s, M, SH - 0.38, SW - 2 * M - 0.8, 0.25, source, size=9, color=GREY, italic=True, name="!!source")
    text(s, SW - M - 0.6, SH - 0.38, 0.6, 0.25, str(N[0]), size=10, color=GREY, align=PP_ALIGN.RIGHT, name="!!num")
    transition(s, trans)
    return s


def pic(s, fname, x, y, w=None, h=None, name="!!pic"):
    p = s.shapes.add_picture(str(V / fname), Inches(x), Inches(y), Inches(w) if w else None, Inches(h) if h else None)
    p.name = name; return p


def body(s, fname, name="!!pic"):
    """A 16:9 image filling the visual area."""
    return pic(s, fname, BODY_X, BODY_TOP, BODY_W, BODY_H, name)


def fit(s, fname, name="!!pic", box=(M, BODY_TOP, SW - 2 * M, BODY_H)):
    """Any image, scaled to fit inside box and centred in it."""
    W, H = Image.open(V / fname).size; bx, by, bw, bh = box
    w = bw; h = w * H / W
    if h > bh: h = bh; w = h * W / H
    return pic(s, fname, bx + (bw - w) / 2, by + (bh - h) / 2, w, h, name)


def view(s, fname, box_px, name="!!pic"):
    """Show the region box_px of an image, cropped, in a frame of the same aspect centred in the visual area.
    Re-cropping one picture across slides is what makes Morph zoom."""
    W, H = Image.open(V / fname).size; x0, y0, x1, y1 = box_px
    a = (x1 - x0) / (y1 - y0)
    fh = BODY_H; fw = fh * a
    if fw > SW - 2 * M: fw = SW - 2 * M; fh = fw / a
    p = pic(s, fname, (SW - fw) / 2, BODY_TOP + (BODY_H - fh) / 2, fw, fh, name)
    p.crop_left, p.crop_right = max(x0, 0) / W, max(W - x1, 0) / W
    p.crop_top, p.crop_bottom = max(y0, 0) / H, max(H - y1, 0) / H
    return p


DARK = RGBColor(0x17, 0x20, 0x26)


def _alpha(shape, pct):
    sf = shape.fill._xPr.find(".//{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr")
    a = etree.SubElement(sf, "{http://schemas.openxmlformats.org/drawingml/2006/main}alpha"); a.set("val", str(pct * 1000))


def chapter(kicker, title, image, notes, source, sub=None, trans="fade"):
    """Full-bleed chapter slide: the chart edge to edge under a dark wash, title in paper colour."""
    s = prs.slides.add_slide(BLANK); N[0] += 1
    s.background.fill.solid(); s.background.fill.fore_color.rgb = DARK
    s.notes_slide.notes_text_frame.text = "\n".join(f"• {n}" for n in notes)
    pic(s, image, 0, 0, SW, SH, name="!!chapter_img")
    w = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(SW), Inches(SH)); w.name = "!!wash"
    w.fill.solid(); w.fill.fore_color.rgb = DARK; w.line.fill.background(); _alpha(w, 50)
    if kicker: text(s, 0.9, 2.55, 10, 0.5, kicker, size=16, color=RGBColor(0xD9, 0xA5, 0x92), italic=True)
    text(s, 0.9, 3.0, 11.0, 1.6, title, size=40, color=PAPER, spacing=1.0)
    if sub: text(s, 0.9, 4.75, 11.0, 0.9, sub, size=17, color=RGBColor(0xD8, 0xD0, 0xC2), spacing=1.15)
    rule(s, 0.9, 2.95 if kicker else 2.85, w=1.1)
    text(s, M, SH - 0.38, SW - 2 * M - 0.8, 0.25, source, size=9, color=RGBColor(0xB9, 0xB0, 0xA0), italic=True)
    if N[0] > 1: text(s, SW - M - 0.6, SH - 0.38, 0.6, 0.25, str(N[0]), size=10, color=RGBColor(0xB9, 0xB0, 0xA0), align=PP_ALIGN.RIGHT)
    transition(s, trans); return s


def argument_title(kicker, title, notes):
    """A short, quiet title slide before each argument."""
    s = new_slide(None, notes)
    text(s, 1.4, 2.7, 10, 0.5, kicker, size=16, color=RED, italic=True)
    text(s, 1.4, 3.15, 10.5, 1.4, title, size=36, spacing=1.0)
    rule(s, 1.4, 4.45, w=1.1)
    return s


def caption(s, x, y, w, line, size=12):
    return text(s, x, y, w, 0.5, line, size=size, color=GREY, italic=True, spacing=1.05)


# ---- the agenda tree (left to right) ----------------------------------------------------------------------------------
# id: (label, subtitle, column, y-centre). Columns: 0 question, 1 strands, 2 halves, 3 questions and arguments
TREE = {
    "root": ("Where were the\nPeriplus ports, and\nhow did they work?", None, 0, 4.2),
    "frame": ("Statistical framework", "locating a place from noisy, partial evidence", 1, 1.95),
    "mal": ("Malabar coast", "Tyndis, Muziris, Nelkynda, Bakarē", 1, 3.95),
    "edd": ("Ed-Dur", "the Gulf", 1, 5.95),
    "conc": ("Conclusion", "blending the evidence", 1, 6.75),
    "mq": ("Quantitative", None, 2, 2.85),
    "ml": ("Qualitative", None, 2, 5.05),
    "eq": ("Quantitative", None, 2, 5.85),
    "el": ("Qualitative", None, 2, 6.4),
    "q1": ("Where was the coastline?", None, 3, 1.85),
    "q2": ("How deep was the water?", None, 3, 2.5),
    "q3": ("Where did the rivers run?", None, 3, 3.15),
    "q4": ("How fast did ships sail?", None, 3, 3.8),
    "a1": ("When the crossing began", None, 3, 4.6),
    "a2": ("How the port worked", None, 3, 5.25),
    "a3": ("After Rome", None, 3, 5.9),
}
EDGES = [("root", "frame"), ("root", "mal"), ("root", "edd"), ("root", "conc"), ("mal", "mq"), ("mal", "ml"),
         ("edd", "eq"), ("edd", "el"), ("mq", "q1"), ("mq", "q2"), ("mq", "q3"), ("mq", "q4"),
         ("ml", "a1"), ("ml", "a2"), ("ml", "a3")]
COLX = [0.55, 3.45, 6.35, 8.6]; COLW = [2.65, 2.6, 1.75, 3.25]


def tree(s, lit, tag=None):
    """Draw the tree; nodes in `lit` (and the edges between them) in ink and red, the rest pale."""
    for a, b in EDGES:
        la, lb = TREE[a], TREE[b]
        x1 = COLX[la[2]] + COLW[la[2]]; y1 = la[3]; x2 = COLX[lb[2]]; y2 = lb[3]
        c = s.shapes.add_connector(MSO_CONNECTOR.ELBOW, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
        on = a in lit and b in lit
        c.line.color.rgb = RED if on else FAINT; c.line.width = Pt(2 if on else 1); c.name = f"!!edge_{a}_{b}"
    for k, (lab, sub, col, yc) in TREE.items():
        on = k in lit; h = 0.62 if sub or "\n" in lab else 0.44
        if k == "root": h = 1.0
        b = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(COLX[col]), Inches(yc - h / 2), Inches(COLW[col]), Inches(h))
        b.name = f"!!node_{k}"; b.fill.solid(); b.fill.fore_color.rgb = CARD
        b.line.color.rgb = RED if on and k != "root" else (INK if k == "root" else FAINT); b.line.width = Pt(1.75 if on else 0.75)
        tf = b.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        for a_ in ("margin_left", "margin_right"): setattr(tf, a_, Inches(0.12))
        lines = lab.split("\n") + ([sub] if sub else [])
        for i, ln in enumerate(lines):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); p.alignment = PP_ALIGN.LEFT
            r = p.add_run(); r.text = ln; f = r.font; f.name = FONT
            is_sub = sub is not None and i == len(lines) - 1
            f.size = Pt(11 if is_sub else (15 if k == "root" else 13)); f.italic = is_sub
            f.color.rgb = (GREY if is_sub else INK) if (on or k == "root") else PALE
    if tag:
        text(s, COLX[3] + COLW[3] + 0.15, tag[1] - 0.15, 1.2, 0.3, tag[0], size=13, color=RED, italic=True, name="!!tag")


# ---- sources --------------------------------------------------------------------------------------------------------------
SRC_749 = "Admiralty Chart 749, Malabar Coast, surveyed by W. B. Selby 1851–53, published 1857 (Wikimedia Commons, public domain)"
SRC_MAP = "Map: PHGCOM, 'Map of the Periplus of the Erythraean Sea', Wikimedia Commons, CC BY-SA 4.0. Ed-Dur ring placed by the author"
SRC_MODEL = "Soundings from Admiralty Chart 749; seabed modelled with a Gaussian process (R-INLA)"
SRC_PAMA = "Cherian and Menon (eds), Unearthing Pattanam (National Museum, New Delhi, 2014)"

# ---- 1. title, full bleed -------------------------------------------------------------------------------------------------------------
chapter(None, "Where were the ports of the Periplus, and how did they work?", "s01_title_backdrop.jpg",
        ["Where were the Periplus ports, and how did they work?", "Today: the Malabar coast, the seabed and then the texts and objects."],
        "Chart: " + SRC_749, sub="The Malabar coast  ·  Vivek Shah  ·  13 November 2026", trans=None)

# ---- 2. the two clusters ----------------------------------------------------------------------------------------------------------
T2 = "The Periplus names two clusters of ports this thesis tests: the Malabar coast and Ed-Dur"
n2 = ["The Periplus, c. AD 50: a merchant's guide from Egypt to India.",
      "Two case studies: the Malabar ports (Tyndis, Muziris, Nelkynda, Bakarē) and Ed-Dur in the Gulf.", "Today: Malabar."]
MAPF = "s02d_periplus_map_ringed_fullres.jpg"; MW, MH = Image.open(V / MAPF).size; k = MW / 1400
s = new_slide(T2, n2, SRC_MAP); view(s, MAPF, (0, (MH - MW * 9 / 16) / 2, MW, (MH + MW * 9 / 16) / 2))
x0, y0, x1 = 450 * k, 205 * k, 980 * k
s = new_slide(T2, n2, SRC_MAP, trans="morph"); view(s, MAPF, (x0, y0, x1, y0 + (x1 - x0) * 9 / 16))

# ---- the thesis as a tree: the whole design, then today's path -------------------------------------------------------------------------
TT = "The thesis tests each port cluster twice: once with the seabed, once with texts and objects"
s = new_slide(TT, ["The whole thesis: a statistical framework, two case studies each with a quantitative and a qualitative half, and a conclusion."])
tree(s, set(TREE))
s = new_slide("Today: the Malabar coast, its seabed and three arguments from the texts and objects",
              ["Today: Malabar. On the quantitative side, the water depth; on the qualitative side, three arguments."], trans="morph")
tree(s, {"root", "mal", "mq", "ml", "q2", "a1", "a2", "a3"}, tag=("today", 3.95))

chapter("Part I", "How deep was the water at the mouths?", "s04c_kodungallur_mouth.jpg", ["Part one: the seabed."], "Chart: " + SRC_749)

# ---- 4. the 1857 survey -------------------------------------------------------------------------------------------------------------------
T4 = "An 1857 Admiralty survey is the oldest measured seabed on this coast"
n4 = ["A British Admiralty survey of 1851–53, measured with a lead line.", "The oldest measured depths for this coast.",
      "Zoom to the Kodungallur mouth, the traditional Muziris area."]
SHF = "s04d_sheet749_window_fullres.jpg"; SWp, SHp = Image.open(V / SHF).size
s = new_slide(T4, n4, SRC_749); view(s, SHF, (0, 0, SWp, SHp))
cx, cy, h = 6450, 8450, 1700; w = h * 16 / 9
s = new_slide(T4, n4, SRC_749, trans="morph"); view(s, SHF, (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2))

# ---- 5. chart -> points -------------------------------------------------------------------------------------------------------------------
T5 = "Every number on the chart is a depth: 428 soundings, each read and checked by hand"
n5 = ["Every number on the chart is a depth in fathoms.", "428 soundings read by hand and checked a second time."]
for i, f in enumerate(["s05a_chart.jpg", "s05b_chart_with_points.png", "s05c_points_only.png"]):
    s = new_slide(T5, n5, SRC_749 + ("; points: the author's transcription" if i else ""), trans="morph"); body(s, f)

# ---- 6, 7. 3D ---------------------------------------------------------------------------------------------------------------------------------
s = new_slide("Each sounding becomes a point in three dimensions", ["Each point is a measured depth."], SRC_MODEL, trans="morph"); body(s, "s06_soundings_3d.png")
s = new_slide("A Gaussian process fills in the seabed between the soundings",
              ["A Gaussian process fills in the seabed between the soundings, with uncertainty.",
               "It allows for a beach slope near shore and extra roughness at the river mouth."], SRC_MODEL, trans="morph"); body(s, "s07_seabed_3d.png")

# ---- 8. does it work: dots land on the real seabed, move across, and the rebuilt seabed fills in under them -------------------
T8 = "Tested on a fully mapped modern inlet, the method rebuilds the seabed to within half a metre"
n8 = ["Proof of concept: a modern Texas inlet whose whole seabed is known.",
      "We survey it as sparsely as Kodungallur was surveyed in 1853, then rebuild it.",
      "It comes back to within about 30 cm in open water and 40 cm along the shore. In the inlet itself, about 1.2 m.",
      "If asked: we also hid the mouth soundings at Kodungallur and predicted them. 8 of 9 fell inside the predicted range."]
src8 = "San Luis Pass, Texas: NOAA Continuously Updated DEM (CUDEM); survey simulated at the 1853 Kodungallur density"
CAP8 = (V / "s08_caption.txt").read_text().strip()
PS = 4.25; PY = 1.95; LX = SW / 2 - PS - 0.3; RX = SW / 2 + 0.3
def texas(stage, trans):
    s = new_slide(T8, n8, src8, trans=trans)
    pic(s, "s08_layer_real.png", LX, PY, PS, PS, name="!!real")
    text(s, LX, PY - 0.45, PS, 0.4, "The real seabed", size=18, align=PP_ALIGN.CENTER, name="!!lab_real")
    if stage >= 3:
        pic(s, "s08_layer_empty.png", RX, PY, PS, PS, name="!!empty")
        text(s, RX, PY - 0.45, PS, 0.4, "Rebuilt (130 soundings)", size=18, align=PP_ALIGN.CENTER, name="!!lab_rebuilt")
    if stage >= 4:
        pic(s, "s08_layer_rebuilt.png", RX, PY, PS, PS, name="!!rebuilt")
        text(s, 1.2, PY + PS + 0.2, SW - 2.4, 0.7, CAP8, size=15, color=GREY, align=PP_ALIGN.CENTER, name="!!cap8")
    if stage >= 2:
        pic(s, "s08_layer_dots.png", LX if stage == 2 else RX, PY, PS, PS, name="!!dots")
texas(1, "fade"); texas(2, "morph"); texas(3, "morph"); texas(4, "morph")

# ---- 9. where a ship could float -----------------------------------------------------------------------------------------------------------------
T9 = "A loaded ship could not come in: water deep enough starts 1.3 km offshore"
n9 = ["Blue is deep enough for a ship drawing 3 m; sand is too shallow.", "At Kodungallur, ship-worthy water starts about 1.3 km out."]
s = new_slide(T9, n9, SRC_MODEL); body(s, "s09a0_seabed_3d_nodots.png")
s = new_slide(T9, n9, SRC_MODEL, trans="morph"); body(s, "s09a_ship_water_3d.png")
s = new_slide("Pliny says the same of Muziris: ships lay far from land and boats carried the cargo",
              ["Pliny says the same of Muziris: ships anchored far from land, and boats carried the cargo.",
               "The 1866 Admiralty Pilot: the bar was 'only available for small coasting craft'."],
              "Pliny, Natural History 6.104: Latin, ed. Mayhoff (Teubner, 1906); translation H. Rackham (Loeb). " + SRC_MODEL, trans="morph")
body(s, "s09a2_ship_water_3d_pliny.png")
s = new_slide(T9, n9 + ["From above: the arrow runs from the mouth to the first water that is 90 per cent sure to be deep enough."], SRC_MODEL)
fit(s, "s09b_ship_water_map.png")

# ---- 10. the whole coast --------------------------------------------------------------------------------------------------------------------------
T10 = "Every candidate mouth worked as an offshore anchorage, so depth cannot pick the port"
n10 = ["Seven candidate mouths, all modelled the same way.", "At every one, ship water is 0.3 to 1.6 km out.",
       "Every mouth worked as an offshore anchorage, so depth does not pick the port."]
src10 = "Admiralty Charts 749, 750 (Selby, 1850–53) and 64 (1887); coast: Natural Earth; seabeds modelled by the author"
import json as _json
LAY = _json.loads((V / "s10_layout.json").read_text()); kf = BODY_W / 19.2
def coast(with_insets, trans):
    s = new_slide(T10, n10, src10, trans=trans); body(s, "s10c_coast_map_dots.png")
    for site in LAY["order"]:
        L = LAY["sites"][site]; fx, fy = L["dot"]; dx, dy = BODY_X + fx * BODY_W, BODY_TOP + (1 - fy) * BODY_H
        sx, sy = L["slot"][:2]; w, h = L["w_in"] * kf, (L["map_h_in"] + L["title_in"]) * kf
        ix, iy = BODY_X + sx * BODY_W, BODY_TOP + (1 - sy) * BODY_H - h
        left = sx < 0.4; ex = ix + w if left else ix; ey = iy + (L["title_in"] + L["map_h_in"] / 2) * kf
        if with_insets:
            pic(s, f"s10_inset_{site}.png", ix, iy, w, h, name=f"!!inset_{site}")
            c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(ex), Inches(ey), Inches(dx), Inches(dy))
        else:
            pic(s, f"s10_inset_{site}.png", dx - 0.01, dy - 0.01, 0.02, 0.02, name=f"!!inset_{site}")        # a speck on its dot
            c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(dx), Inches(dy), Inches(dx + 0.001), Inches(dy))
            text(s, dx + 0.12, dy - 0.13, 2.0, 0.3, LAY["label"][site], size=13, name=f"!!lab_{site}")
        c.line.color.rgb = FAINT; c.line.width = Pt(1); c.name = f"!!lead_{site}"
coast(False, "fade"); coast(True, "morph")

# ---- Part II -----------------------------------------------------------------------------------------------------------------------------------------------------
chapter("Part II", "How did the ports work, and what came after Rome?", "s00_divider_ports.jpg", ["Part two: the texts and the objects."],
        "Chart: Admiralty Chart 750, off Porakad (Purakkad), Selby 1850–52, published 1857 (Wikimedia Commons, public domain)")

argument_title("The turnaround", "How the port worked", ["If ships lay offshore, the question is the turnaround: how a ship was handled."])

# ---- 12. argument 2: the turnaround ------------------------------------------------------------------------------------------------------------------------
T12 = "Ships lay offshore for months waiting for the wind; loading took only weeks"
n12 = ["Leave Egypt about 20 July and arrive about 28 September, just as the coast reopens.",
       "Loading takes days to about three weeks, but ships must leave by 13 January.", "So most of the stay was waiting.",
       "The pepper harvest is not in until after the deadline, so cargoes came from store, held by locals."]
src12 = "Periplus 56; Pliny, Natural History 6.104, 6.106; Admiralty West Coast of India Pilot (1909); loading time: the author's estimate"
for i, f in enumerate(["s12a_turnaround_voyage.png", "s12b_turnaround_stay.png", "s12c_turnaround_full.png"]):
    s = new_slide(T12, n12, src12, trans="morph" if i else "fade"); body(s, f)
s = new_slide("At Pattanam, a dugout canoe and a wharf at the waterline", ["At Pattanam: a dugout canoe and a wharf."], SRC_PAMA + ", pp. 120–21")
pw = (SW - 2 * M - 0.3) / 2
p1 = pic(s, "s12d_pattanam_wharf_canoe.jpg", M, 1.6, w=pw); p2 = pic(s, "s12e_pattanam_wharf_lining.jpg", M + pw + 0.3, 1.6, w=pw, name="!!pic2")
cy_ = 1.6 + max(p1.height, p2.height) / 914400 + 0.12
caption(s, M, cy_, pw, "The dugout canoe in the waterlogged wharf deposit"); caption(s, M + pw + 0.3, cy_, pw, "The brick lining of the wharf")

# ---- 13. argument 2: who stayed --------------------------------------------------------------------------------------------------------------------------
s = new_slide("Indians lived in Roman ports; at Pattanam, Romans left only trade goods",
              ["Indians in Egyptian ports left cooking pots and their names.", "Romans at Pattanam left trade goods only."],
              "Tomber, Indo-Roman Trade (2008), figs 6 and 13; Shajan, Tomber, Selvakumar and Cherian, JRA 17 (2004), fig. 5; " + SRC_PAMA)
CW = (SW - 2 * M - 0.5) / 2
text(s, M, 1.55, CW, 0.4, "Indians in the Egyptian Red Sea ports: a household", size=17, color=GREY)
text(s, M + CW + 0.5, 1.55, CW, 0.4, "Romans at Pattanam: trade goods only", size=17, color=GREY)
ln = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(M + CW + 0.24), Inches(1.6), Inches(0.015), Inches(5.3))
ln.fill.solid(); ln.fill.fore_color.rgb = FAINT; ln.line.fill.background()
half = (CW - 0.3) / 2
for (f, col, kk, cap) in [("s13a_redsea_indian_cooking_ware.jpg", 0, 0, "Indian cooking pots, Berenike and Myos Hormos"),
                          ("s13b_myos_hormos_tamil_graffiti.jpg", 0, 1, "Tamil-Brahmi names scratched on jars, Myos Hormos"),
                          ("s13c_pattanam_dressel24_amphora.jpg", 1, 0, "Dressel 2-4 wine amphora from Campania"),
                          ("s13d_pattanam_sigillata_stamp.jpg", 1, 1, "Stamped Italian terra sigillata")]:
    x = M + col * (CW + 0.5) + kk * (half + 0.3)
    pic(s, f, x, 2.15, w=half, name=f"!!obj_{f[:4]}"); caption(s, x, 2.15 + half * 0.75 + 0.12, half, cap)
T13b = "In the Tamil poems, foreigners live only at Puhar; at Muciṟi their ships come and go"
n13 = ["Tamil poems: at Muciṟi, Yavana ships come and go.", "At Madurai, Yavanas are guards and wine suppliers.",
       "Only at Puhar do foreigners 'dwell'.", "A port run by locals for seasonal crews."]
src13 = "Translations: Vaidehi Herbert (sangamtranslationsbyvaidehi.com). Terrain: Copernicus DEM; rivers: HydroRIVERS; coast: Natural Earth"
for i, f in enumerate(["s13e_tamil_poems_muciri.png", "s13f_tamil_poems_madurai.png", "s13g_tamil_poems_puhar.png"]):
    s = new_slide(T13b, n13, src13, trans="morph" if i else "fade"); body(s, f)

argument_title("The crossing", "When south India began to cross the Arabian Sea", ["Next: when the crossing began."])

# ---- 14. argument 1 ------------------------------------------------------------------------------------------------------------------------------------------
T14 = "The early date for the crossing is borrowed from Sri Lanka; where the pottery was found, its neighbours are Roman"
n14 = ["Rouletted Ware is the pottery used to date the crossing. A sherd has no date of its own: it takes one from what it was found with.",
       "Tissamaharama: mended vessels in a 2nd-century BC layer. Used and broken where they lay. A real early date.",
       "Sumhuram: no layer published. Dated by matching to Tissamaharama, and the oldest layers mix 'BC' Indian pottery with Roman amphorae.",
       "Myos Hormos: one late-Augustan deposit.", "Pattanam: in every layer, because of heavy disturbance, so it dates nothing.",
       "So the early date is borrowed; the contexts on the Arabian Sea are Roman. North-west India crossed early; south India appears only from the late 1st c. BC."]
src14 = ("Schenk 2014; Pavan and Schenk, AAE 23 (2012), fig. 3; Avanzini 2014; Tomber 2002 via Shoebridge 2017; " + SRC_PAMA +
         ", p. 50; Sarathchandrababu 2022–23. Layer stacks schematic: only what the publications state")
for i, f in enumerate(["s14g_contexts_objects.png", "s14h_contexts_layers.png", "s14i_contexts_dated.png"]):
    s = new_slide(T14, n14, src14, trans="morph" if i else "fade"); body(s, f)

argument_title("After Rome", "What became of the port when Rome's trade faded", ["Next: after Rome."])

# ---- 15. argument 3 ------------------------------------------------------------------------------------------------------------------------------------------
T15 = "The port zone outlived Rome by shifting along the coast"
n15 = ["Roman contact peaks in the 1st century AD.", "Gulf pottery follows, 3rd to 8th centuries. By about 550, Cosmas no longer names Muziris.",
       "The trade moves: to Kollam (849), the Chera capital at Kodungallur, then Kochi.", "The harbour zone moved rather than died."]
src15 = "Each item's source is printed beneath it; the copper plates and the Chera dates rest on secondary summaries"
for i, f in enumerate(["s15a_after_rome_roman.png", "s15b_after_rome_gulf.png", "s15c_after_rome_medieval.png"]):
    s = new_slide(T15, n15, src15, trans="morph" if i else "fade"); body(s, f)
s = new_slide("After Rome, Pattanam's foreign pottery comes from the Gulf", ["Torpedo jars and turquoise-glazed ware: Gulf pottery, mostly after the Roman peak."], SRC_PAMA)
for (f, x, cap) in [("s15d_pattanam_torpedo_jar.jpg", 1.3, "Torpedo jar sherd with bitumen lining"),
                    ("s15e_pattanam_turquoise_glaze.jpg", 7.0, "Turquoise-glazed ring base")]:
    pic(s, f, x, 1.7, w=5.0, name=f"!!obj_{f[:4]}"); caption(s, x, 5.6, 5.0, cap, size=13)

# ---- 16. what we can say -------------------------------------------------------------------------------------------------------------------------------------
s = new_slide("Four claims, kept small", ["The seabed explains how ships were handled. It does not pick the port.",
              "Foreign crews came seasonally and locals ran the port.", "South India joined the crossing late.",
              "The port zone outlived Rome by shifting along the coast."])
claims = ["The seabed explains how ships were handled. It does not pick the port.",
          "Foreign crews came with the monsoon; local people ran the port.",
          "South India joined the Arabian Sea crossing late, from the late 1st century BC.",
          "The port zone outlived Rome by shifting along the coast."]
for i, c in enumerate(claims):
    text(s, 1.2, 1.75 + i * 1.22, 0.6, 0.6, str(i + 1), size=30, color=RED)
    text(s, 1.95, 1.85 + i * 1.22, 10.2, 0.9, c, size=22)

# ---- 17. next: Ed-Dur ---------------------------------------------------------------------------------------------------------------------------------------------
s = new_slide("Next: Ed-Dur, a lagoon port now about 4 km inland",
              ["A lagoon port, now about 4 km inland.", "The same methods: shoreline, depth, and the material record."],
              "Forti et al., 'Geomorphological evolution of the Umm al-Quwain (UAE) coastal-lagoon system', Catena 247 (2024), fig. 2A")
fit(s, "s17_ed_dur_lagoon.jpg")

prs.save(OUT)
print("wrote", OUT, len(prs.slides), "slides,", round(OUT.stat().st_size / 1e6, 1), "MB")

"""Edit the hand-edited deck in place: argument 1 as relay -> misread and misdated -> the four contexts.

Inserts, after the 'The crossing' title slide:
  A  the Periplus 26 relay, on the Wikimedia Periplus map (same picture as the opening slides)
  B1 the Pattanam Rouletted Ware sherd: misread as Roman
  B2 the same, adding: misdated as early (morphs from B1)
and relabels the existing four-sherd slide with early / late verdicts and a concluding headline.
Run once; it refuses to run twice.
"""
import pathlib, copy
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
V = ROOT / "presentation" / "nov_13th"; DECK = V / "nov13_malabar.pptx"
MAP = ROOT / "presentation" / "sources" / "periplus_map.jpg"
SHERD = ROOT / "sites/malabar/analysis/figures/objects/14_pattanam_rw_pama.png"
SW, SH, M = 13.333, 7.5, 0.55
PAPER = RGBColor(0xF4, 0xEF, 0xE6); INK = RGBColor(0x2B, 0x2B, 0x2B); GREY = RGBColor(0x6E, 0x66, 0x5A)
RED = RGBColor(0xB5, 0x43, 0x2F); DEEP = RGBColor(0x1F, 0x5F, 0x7A); BROWN = RGBColor(0x8A, 0x5A, 0x44)
NS = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main"}
A_NS = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
MORPH = ('<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
         'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
         '<mc:Choice xmlns:p159="http://schemas.microsoft.com/office/powerpoint/2015/09/main" Requires="p159">'
         '<p:transition xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" spd="slow" p14:dur="1400">'
         '<p159:morph option="byObject"/></p:transition></mc:Choice>'
         '<mc:Fallback><p:transition spd="slow"><p:fade/></p:transition></mc:Fallback></mc:AlternateContent>')
FADE = '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="med"><p:fade/></p:transition>'

prs = Presentation(DECK); slides = list(prs.slides)
assert not any(sh.name == "!!relay_ring" for s in slides for sh in s.shapes), "already applied"
TITLE_IDX = next(i for i, s in enumerate(slides) if any(sh.has_text_frame and sh.text_frame.text == "The crossing" for sh in s.shapes))
SHERDS = slides[TITLE_IDX + 1]


def trans(s, kind):
    el = etree.fromstring(MORPH if kind == "morph" else FADE)
    a = s._element.find("p:clrMapOvr", NS); (a if a is not None else s._element.find("p:cSld", NS)).addnext(el)


def text(s, x, y, w, h, runs, size=14, color=INK, italic=False, align=PP_ALIGN.LEFT, name=None, spacing=1.12, bold=False):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); tf = tb.text_frame; tf.word_wrap = True
    for a in ("margin_left", "margin_right", "margin_top", "margin_bottom"): setattr(tf, a, 0)
    for i, ptxt in enumerate(runs if isinstance(runs, list) else [runs]):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); p.alignment = align; p.line_spacing = spacing
        r = p.add_run(); r.text = ptxt; f = r.font; f.name = "Georgia"; f.size = Pt(size); f.color.rgb = color; f.italic = italic; f.bold = bold
    if name: tb.name = name
    return tb


def set_notes(s, txt):
    ns = s.notes_slide
    if ns.notes_text_frame is None:                      # the resaved notes master lost its body placeholder
        donor = next(x.notes_slide for x in slides if x.has_notes_slide and x.notes_slide.notes_placeholder is not None)
        el = copy.deepcopy(donor.notes_placeholder._element); ns.shapes._spTree.append(el)
    ns.notes_text_frame.text = txt


def new(title, notes, source, kind):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid(); s.background.fill.fore_color.rgb = PAPER
    set_notes(s, "\n".join(f"• {n}" for n in notes))
    text(s, M, 0.34, SW - 2 * M, 0.8, title, size=24, name="!!title", spacing=1.0)
    r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(M), Inches(1.24), Inches(0.9), Inches(0.035)); r.name = "!!rule"
    r.fill.solid(); r.fill.fore_color.rgb = RED; r.line.fill.background()
    text(s, M, SH - 0.38, SW - 2 * M - 0.8, 0.25, source, size=9, color=GREY, italic=True, name="!!source")
    text(s, SW - M - 0.6, SH - 0.38, 0.6, 0.25, "0", size=10, color=GREY, align=PP_ALIGN.RIGHT, name="!!num")
    trans(s, kind); return s


def arrow(s, x1, y1, x2, y2, color, name):
    c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = color; c.line.width = Pt(4); c.name = name
    ln = c.line._get_or_add_ln(); t = etree.SubElement(ln, A_NS + "tailEnd"); t.set("type", "triangle"); t.set("w", "med"); t.set("len", "med")
    return c


# ---- A: the relay ------------------------------------------------------------------------------------------------------
X0, Y0, X1 = 700, 520, 2400; Y1 = Y0 + (X1 - X0) * 9 / 16          # map pixels shown (full-resolution map)
FW, FH = 9.78, 5.5; FX, FY = (SW - FW) / 2, 1.5
P = lambda px, py: (FX + (px - X0) / (X1 - X0) * FW, FY + (py - Y0) / (Y1 - Y0) * FH)
s = new("Before the Periplus, Indian and Egyptian ships met at Aden: Indian goods reached Rome by relay",
        ["Periplus 26: Eudaimon Arabia (Aden) got its name because, before the author's day, ships from India did not go on to Egypt and ships from Egypt did not sail beyond it.",
         "So Indian goods reached the Mediterranean, but through a meeting point in Arabia, not by Indian ships sailing all the way.",
         "Which Indian ships came to Aden, and from when, is the question the pottery has been used to answer."],
        "Periplus 26, trans. Casson (1989: 65). Map: PHGCOM, 'Map of the Periplus of the Erythraean Sea', Wikimedia Commons, CC BY-SA 4.0; arrows added by the author",
        "fade")
W, H = Image.open(MAP).size
pic = s.shapes.add_picture(str(MAP), Inches(FX), Inches(FY), Inches(FW), Inches(FH)); pic.name = "!!pic"
pic.crop_left, pic.crop_right, pic.crop_top, pic.crop_bottom = X0 / W, (W - X1) / W, Y0 / H, (H - Y1) / H
ax, ay = P(1132, 971)                                                     # Eudaimon Arabia (Aden) on the map
mx, my = P(2022, 1061)                                                    # Muziris on the map
ex, ey = P(760, 560)                                                      # up the Red Sea, towards Egypt
arrow(s, mx - 0.15, my - 0.05, ax + 0.32, ay + 0.02, DEEP, "!!relay_india")
arrow(s, ex + 0.1, ey + 0.1, ax - 0.2, ay - 0.22, BROWN, "!!relay_egypt")
ring = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(ax - 0.3), Inches(ay - 0.3), Inches(0.6), Inches(0.6)); ring.name = "!!relay_ring"
ring.fill.background(); ring.line.color.rgb = RED; ring.line.width = Pt(3.5)
box = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(FX + 0.25), Inches(FY + FH - 1.32), Inches(6.2), Inches(1.1))
box.fill.solid(); box.fill.fore_color.rgb = RGBColor(0xFA, 0xF7, 0xF0); box.line.color.rgb = RGBColor(0xA8, 0x9F, 0x8C)
text(s, FX + 0.42, FY + FH - 1.2, 5.9, 0.95,
     ["“vessels from India did not go on to Egypt and those from Egypt did not dare sail to the places further on but came only this far”",
      "Periplus 26, on Eudaimon Arabia (Aden)"], size=13, color=INK, italic=True)

# ---- B1, B2: misread, then misdated ------------------------------------------------------------------------------------
TB = "The pottery was first misread as Roman, then misdated as early"
nb = ["Rouletted Ware is the fine pottery used to argue for an early crossing.",
      "First misread: long taken for Roman pottery (Wheeler Type 1, Arikamedu, 1946). Begley (1988) argued it was Indian, and X-ray diffraction (Gogte) traced the clay to the Ganges delta.",
      "Then misdated: found in Arabia, it was read as proof of an early Indian crossing. But that early date comes from Sri Lanka, not from where it was found."]
srcb = "Pattanam sherd: Cherian and Menon (eds), Unearthing Pattanam (2014), p. 50. Tomber, Indo-Roman Trade (2008: 44–45); Pavan and Schenk, AAE 23 (2012)"
for stage in (1, 2):
    s = new(TB, nb, srcb, "fade" if stage == 1 else "morph")
    im = Image.open(SHERD); h = 4.9; w = h * im.width / im.height
    p = s.shapes.add_picture(str(SHERD), Inches(M + 0.2), Inches(1.65), Inches(w), Inches(h)); p.name = "!!sherd"
    text(s, M + 0.2, 1.65 + h + 0.1, w, 0.3, "Rouletted Ware, Pattanam", size=12, color=GREY, italic=True, name="!!sherd_cap")
    tx = M + 0.2 + w + 0.7; tw = SW - tx - M
    text(s, tx, 1.85, tw, 0.4, "1   Misread as Roman", size=20, color=RED, name="!!h1")
    text(s, tx, 2.35, tw, 1.4, ["Long taken for Roman pottery: Wheeler Type 1, Arikamedu, 1946.",
                                "It is Indian. Its clay comes from the Ganges delta (Gogte), and Begley showed it was made in India."],
         size=15, name="!!b1", spacing=1.2)
    if stage == 2:
        text(s, tx, 4.05, tw, 0.4, "2   Misdated as early", size=20, color=RED, name="!!h2")
        text(s, tx, 4.55, tw, 1.4, ["Found in Arabia, it was read as proof that south India crossed before Rome.",
                                    "But the early date comes from Sri Lanka, not from the places it was found."],
             size=15, name="!!b2", spacing=1.2)

# ---- C: relabel the four-sherd slide -----------------------------------------------------------------------------------
pic4 = next(sh for sh in SHERDS.shapes if sh.name == "!!pic")
L, T, Wd, Hd = [v / 914400 for v in (pic4.left, pic4.top, pic4.width, pic4.height)]
for k, (lab, col) in enumerate([("dated by its own layers: early", DEEP), ("date borrowed from Sri Lanka", RED),
                                ("one late-Augustan deposit", RED), ("in every layer: no date of its own", RED)]):
    text(SHERDS, L + (0.03 + k * 0.243) * Wd, T + 0.865 * Hd, 0.215 * Wd, 0.5, lab, size=12, color=col, bold=True, name=f"!!verdict{k}")
for sh in SHERDS.shapes:
    if sh.name == "!!title":
        sh.text_frame.paragraphs[0].runs[0].text = "Where the pottery was found, its neighbours are Roman: south India crossed only from the late 1st century BC"
SHERDS.notes_slide.notes_text_frame.text += ("\n• Conclusion: north-west India was crossing before Rome (Indus merchants at Socotra; Gujarati pottery at Mleiha, 3rd–2nd c. BC). "
                                             "South India appears only from the late 1st century BC, with the Roman trade.")

# ---- move the new slides into place, renumber ----------------------------------------------------------------------------
ids = prs.slides._sldIdLst; new_ids = list(ids)[-3:]
for el in new_ids: ids.remove(el)
for j, el in enumerate(new_ids): ids.insert(TITLE_IDX + 1 + j, el)
for i, s in enumerate(prs.slides, 1):
    for sh in s.shapes:
        if sh.has_text_frame and abs(sh.left / 914400 - (SW - M - 0.6)) < 0.05 and abs(sh.top / 914400 - (SH - 0.38)) < 0.05 and sh.text_frame.text.strip().isdigit():
            sh.text_frame.paragraphs[0].runs[0].text = str(i)
prs.save(DECK); print("done:", len(prs.slides), "slides; new slides at", TITLE_IDX + 2, "to", TITLE_IDX + 4)

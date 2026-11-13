"""Hand-edit of nov13_malabar.pptx (12 Nov): split the Rouletted Ware build into two slides
(misread at 36 on the Pattanam sherd, misdated at 37 on the Sumhuram sherd) and add the depth legend
to the slide-13 seabed. Edits the user's saved deck in place; never re-run build_nov13_deck.py."""
import sys, copy, pathlib
from pptx import Presentation
from pptx.util import Inches
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from make_nov13_visuals import depth_legend
from PIL import Image

D = pathlib.Path(__file__).resolve().parents[1] / "nov_13th"
DECK = D / "nov13_malabar.pptx"
p = Presentation(DECK); S = p.slides
P = '{http://schemas.openxmlformats.org/presentationml/2006/main}'
MC = '{http://schemas.openxmlformats.org/markup-compatibility/2006}'
sh = lambda s, n: next(x for x in s.shapes if x.name == n)

def set_text(shape, txt):
    """Replace the text, keeping the first run's formatting in every paragraph."""
    tf = shape.text_frame; paras = tf.paragraphs
    tmpl = copy.deepcopy(paras[0]._p)
    for para in paras[1:]: para._p.getparent().remove(para._p)
    lines = txt.split("\n")
    first = paras[0]; first.runs[0].text = lines[0]
    for r in first.runs[1:]: r._r.getparent().remove(r._r)
    for line in lines[1:]:
        np_ = copy.deepcopy(tmpl); tf._txBody.append(np_)
        para = tf.paragraphs[-1]; para.runs[0].text = line
        for r in para.runs[1:]: r._r.getparent().remove(r._r)

def swap_picture(slide, name, img):
    old = sh(slide, name)
    new = slide.shapes.add_picture(str(img), old.left, old.top, old.width, old.height)
    new.crop_left, new.crop_right, new.crop_top, new.crop_bottom = old.crop_left, old.crop_right, old.crop_top, old.crop_bottom
    new.name = name
    old._element.addprevious(new._element)       # keep z-order
    old._element.getparent().remove(old._element)

s13, s36, s37 = S[12], S[35], S[36]
assert sh(s13, "!!title").text_frame.text.startswith("Established statistical models")
assert sh(s36, "!!h1").text_frame.text.startswith("1") and any(x.name == "!!h2" for x in s37.shapes), "already applied?"

# slide 13: the seabed with a depth legend, as on slide 18
leg = D / "s07b_seabed_3d_legend.png"
Image.open(D / "s07_seabed_3d.png").save(leg); depth_legend(leg, x=1380, y=860)
swap_picture(s13, "!!pic", leg)

# slide 36: misread as Roman, the user's wording
set_text(sh(s36, "!!b1"),
         "Initially mistaken for Roman pottery because of its fine finish and rouletted decoration, which resembled Greco-Roman ceramics.\n"
         "Its shape was later argued to be Indian (Begley), which was then confirmed by X-ray analysis (Gogte).")
s36.notes_slide.notes_text_frame.text = (
    "• Rouletted Ware is the fine pottery used to argue for an early crossing.\n"
    "• Wheeler took it for Roman at Arikamedu (his Type 1, 1946), on its finish and rouletting.\n"
    "• Begley (1988) argued it was Indian; X-ray diffraction (Gogte) traced the clay to the lower Ganges delta.")

# slide 37: misdated as early, on the Sumhuram sherd, in the slot slide 36 uses
for n in ("!!h1", "!!b1"):
    e = sh(s37, n)._element; e.getparent().remove(e)
for n_old, n_new in (("!!h2", "!!h1"), ("!!b2", "!!b1")):
    x, ref = sh(s37, n_old), sh(s36, n_new)
    x.left, x.top, x.width, x.height, x.name = ref.left, ref.top, ref.width, ref.height, n_new
b = sh(s37, "!!b1"); b.height = Inches(4.1)
set_text(sh(s37, "!!title"), "Later scholars then misdated the same pottery found in Arabia as early, using a date borrowed from Sri Lanka")
set_text(b,
         "Once it was recognised as Indian, the same ware turned up in Arabia, at Sumhuram in Oman, and was taken as evidence "
         "that south India traded across the Arabian Sea before Rome.\n"
         "But its early date was borrowed from Sri Lanka, where the ware is dated by its own layers at Tissamaharama. "
         "It was not taken from the layers in which the Arabian sherds were found.")
swap_picture(s37, "!!sherd", D / "s14e_sumhuram_rouletted_ware.jpg")
pic, cap = sh(s37, "!!sherd"), sh(s37, "!!sherd_cap")      # tight crop of fig. 3, centred in the sherd slot
L, R, T, B = 86, 1114, 263, 624
pic.crop_left, pic.crop_right, pic.crop_top, pic.crop_bottom = L / 1200, (1200 - R) / 1200, T / 900, (900 - B) / 900
pic.left, pic.width = Inches(0.75), Inches(5.66); pic.height = int(pic.width * (B - T) / (R - L))
pic.top = int(Inches(1.65 + 4.9 / 2) - pic.height / 2); cap.top = pic.top + pic.height + Inches(0.12)
set_text(cap, "Rouletted Ware, Sumhuram (Oman)")
set_text(sh(s37, "!!source"), "Sumhuram sherd: Pavan and Schenk, AAE 23 (2012), fig. 3. Tomber, Indo-Roman Trade (2008: 44–45)")
for el in list(s37._element):                     # separate slide now: no morph from 36
    if el.tag in (P + "transition", MC + "AlternateContent"): s37._element.remove(el)
s37.notes_slide.notes_text_frame.text = (
    "• Once it was known to be Indian, finds in Arabia, such as Sumhuram in Oman, were read as proof that south India crossed before Rome.\n"
    "• The early date comes from Sri Lanka, where Tissamaharama dates the ware by its own layers.\n"
    "• The Arabian sherds were dated by borrowing that date, not from the layers they were found in.")

p.save(DECK); print("done")

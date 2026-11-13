"""Hand-edit of nov13_malabar.pptx (12 Nov): slide 38's four-sherd picture becomes the pottery-on-a-date-axis graphic
(s14k). Keeps the user's headline. Edits the saved deck in place."""
import pathlib
from pptx import Presentation
D = pathlib.Path(__file__).resolve().parents[1] / "nov_13th"; DECK = D / "nov13_malabar.pptx"
p = Presentation(DECK); s = p.slides[37]
sh = lambda n: next(x for x in s.shapes if x.name == n)
assert sh("!!title").text_frame.text.startswith("While north-west Indian pottery")
old = sh("!!pic")
new = s.shapes.add_picture(str(D / "s14k_crossing_pottery.png"), old.left, old.top, old.width, old.height); new.name = "!!pic"
old._element.addprevious(new._element); old._element.getparent().remove(old._element)
src = sh("!!source").text_frame.paragraphs[0]
src.runs[0].text = ("Reddy 2013: 32, fig. 213 (after Mouton 2008); Pavan and Schenk 2012, fig. 3; Tomber 2008, figs 5–6, pp. 74–75; Shoebridge 2017: 112–13")
for r in src.runs[1:]: r.text = ""
s.notes_slide.notes_text_frame.text = (
    "• Each pot sits at the date of the layer it was found in.\n"
    "• North-west: Indian jars at Mleiha, clay from Maharashtra and Gujarat, 3rd to mid-2nd century BC (Reddy 2013: 32). Before Rome.\n"
    "• South: the only early piece is Sumhuram, and its date is the one borrowed from Sri Lanka (slide 37).\n"
    "• Everything else is Roman-period: Rouletted Ware at Myos Hormos in one late-Augustan deposit; Indian cooking pots at Berenike and Myos Hormos, at least one from Kerala, most common in the early Roman period (Tomber 2008: 75).\n"
    "• If asked: Rouletted Ware's clay is from the Ganges region; it counts here because it is the ware used to argue for an early south Indian crossing.")
p.save(DECK); print("done")

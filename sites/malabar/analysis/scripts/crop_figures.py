"""Crop the object figures used in the ceramics document from the readings.

Each entry names the source PDF, the PDF page (1-based), and the crop either as
a fraction of the page (x0, y0, x1, y1 in 0-1) or in PDF points ("pt"). Output
goes to analysis/figures/objects/ at 300 dpi. The source and page of every
image are recorded here, so any figure can be checked against the publication.
"""
import pathlib
import fitz

HERE = pathlib.Path(__file__).resolve().parents[1]
R = HERE.parent / "readings"
S = R / "supplementary"
OUT = HERE / "figures" / "objects"
OUT.mkdir(parents=True, exist_ok=True)

PAVAN = R / "Arab Archaeol Epigr - 2012 - Pavan - Crossing the Indian Ocean before the Periplus  a comparison of pottery assemblages at.pdf"
S2006 = R / "The_dating_and_historical_value_of_roule.pdf"
S2007 = R / "Parthian_Glazed_Pottery_from_Sri_Lanka_a.pdf"
S2014 = R / "Tissamaharama_Pottery_sequence_and_the_E.pdf"
TOMBER = R / "Tomber - Indo-Roman trade  from pots to pepper.pdf"
PAMA = S / "PAMA-Unearthing-Pattanam-Excavation-Catalogue.pdf"
SHAJAN04 = S / "Shajan-Tomber-Selvakumar-Cherian-2004-JRA-Locating-the-Ancient-Port-of-Muziris.pdf"

CROPS = {
    # name: (pdf, page, box, mode)
    "01_sumhuram_rw_fig3": (PAVAN, 9, (0.07, 0.41, 0.485, 0.525), "frac"),
    "01b_tissa_rw_early_late_fig6": (PAVAN, 9, (0.505, 0.61, 0.93, 0.875), "frac"),
    "02_tissa_riveted_rw_fig1c": (S2006, 2, (0.13, 0.68, 0.725, 0.88), "frac"),
    "02b_tissa_rw_composite_fig1a": (S2006, 2, (0.16, 0.07, 0.68, 0.375), "frac"),
    "03_tissa_trench3b_fig6": (S2014, 11, (0.11, 0.07, 0.93, 0.89), "frac"),
    "04_tissa_imitation_g1_fig15": (S2014, 21, (0.19, 0.10, 0.905, 0.72), "frac"),
    "05_sumhuram_wheeler18_fig4": (PAVAN, 9, (0.07, 0.575, 0.485, 0.70), "frac"),
    "06_sumhuram_household_fig1": (PAVAN, 3, (0.06, 0.128, 0.455, 0.575), "frac"),
    "06b_tissa_phase_c1_fig5": (PAVAN, 9, (0.505, 0.125, 0.93, 0.525), "frac"),
    "07_pattanam_dressel24_fig5": (SHAJAN04, 7, (118, 41, 430, 262), "pt"),
    "08_pattanam_sigillata_stamped": (PAMA, 22, (282, 66, 444, 257), "pt"),
    "08b_pattanam_sigillata_stamp_closeup": (PAMA, 28, (547, 275, 703, 431), "pt"),
    "09_tissa_glazed_rims_fig2": (S2007, 17, (0.12, 0.12, 0.87, 0.525), "frac"),
    "09b_tissa_glaze_fabric_fig6": (S2007, 23, (0.10, 0.51, 0.89, 0.865), "frac"),
    "10_pattanam_tgp_ringbase": (PAMA, 34, (622, 391, 784, 547), "pt"),
    "11_pattanam_torpedo_lined": (PAMA, 32, (355, 302, 678, 534), "pt"),
    "11b_pattanam_torpedo_triangular": (PAMA, 32, (544, 103, 743, 292), "pt"),
    "12_pattanam_amana_rim": (PAMA, 22, (35, 403, 474, 595), "pt"),
    "13_red_sea_crsw_fig6": (TOMBER, 49, (0.02, 0.08, 0.95, 0.38), "frac"),
    "13b_myos_hormos_graffiti_fig13": (TOMBER, 77, (0.02, 0.08, 0.95, 0.335), "frac"),
    "14_pattanam_rw_pama": (PAMA, 50, (260, 255, 446, 416), "pt"),
    "15_pattanam_brw_rim": (PAMA, 51, (587, 411, 920, 542), "pt"),
    "16_myos_hormos_rw_fig5": (TOMBER, 47, (8, 372, 215, 468), "pt"),
}

for name, (pdf, page, box, mode) in CROPS.items():
    pg = fitz.open(pdf)[page - 1]
    r = pg.rect
    if mode == "frac":
        clip = fitz.Rect(r.x0 + box[0] * r.width, r.y0 + box[1] * r.height,
                         r.x0 + box[2] * r.width, r.y0 + box[3] * r.height)
    else:
        clip = fitz.Rect(*box)
    pg.get_pixmap(dpi=300, clip=clip).save(OUT / f"{name}.png")
    print(name, pdf.name[:40], "p.", page)

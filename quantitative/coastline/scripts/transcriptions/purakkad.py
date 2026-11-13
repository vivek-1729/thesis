"""Hand transcription of soundings in the purakkad window of BA 750.

Site: purakkad (candidates for Nelkynda and Bakare: Purakkad, and Nirkunnam, which
the chart spells "Nircum").
Sheet: Admiralty BA 750 (Selby, surveyed 1850-2, 1:146,000, soundings in fathoms),
scan malabar-750-1857.jpg, window chart px (3200, 4500)-(4800, 6200).

Values were read by eye from the numbered tiles in data/soundings/purakkad/tiles/,
with the dense inshore tiles re-read from 4x crops of the full-resolution scan.
Status codes:
  ok        clear reading
  unsure    legible but could be misread, or a lone fraction that may not be a sounding
  edge      cut by the window border; excluded from modelling
  drop      ambiguous on the second check; excluded
  not       detector picked up something that is not a sounding (place names, the
            Nircum town mark, palms, river banks inland, anchor, "soft mud", the 1901 label)
  split     a detector box that merged two numbers; both are in ADDED
  later     a sounding the chart marks as added after the original survey
Rows starting with 'A' are numbers the detector missed. Their position is the
window pixel I read off the tile image (accurate to roughly +/- 5 chart px).

The 1901 soundings. The words "(soundings in 1901)" are engraved, rotated to run
NNW-SSE, between window (300, 760) and (450, 1140), with an opening parenthesis at
the north end and a closing one at the south end. Immediately east of the label, and
parallel to it, is a straight line of five soundings, all 4 3/4: S0129 (296, 727),
S0135 (337, 805), S0213 (376, 910), S0219 (413, 998), S0279 (457, 1122). Three things
tie them to the label and set them apart from the 1850-2 survey: (1) they are set in
a lighter, thinner, upright type with a horizontal fraction bar, the same type as the
label, whereas every surrounding sounding is the survey's heavy sloping italic; (2) the
label's two parentheses bracket exactly the length of this line, and no other sounding
in that style occurs anywhere in the window (I looked north to chart y 4300 and south
to 6500 along the line's bearing); (3) they are 4 3/4 among original soundings of 6 to
9 on either side, so they cannot belong to the original sequence. These five are marked
"later". Every other sounding in the window, including the 4 3/4 readings near the
mud bank (S0003, S0006, S0193, S0265, S0328, A035), is in the original italic and is
treated as 1850-2. The coloured lines (red over a dash-dot line, brown, green) are later
hand additions; the numbers under them were read normally. The 1901 line is therefore a
single line of five soundings, not an area, and it reports 4 3/4 fm where the 1850-2
survey has 6 to 9 fm nearby, about 7 km off the coast between Nircum and Porakad. That difference is
recorded here and not interpreted.

Mud-bank anchorage off Porakad (window px; chart px; lat, lon from the BA 750 georef):
  anchor S0188           (654, 805);  (3854, 5305);  9.3736 N, 76.3331 E
  anchor (not detected)  (777, 915);  (3977, 5415);  9.3615 N, 76.3468 E
  "soft mud"             (797, 952);  (3997, 5452);  9.3574 N, 76.3491 E, just below the second anchor
  a hatched bell-shaped mark with the letter "R", (690, 826), beside the first anchor;
  its 5 is A026. The chart's note off Porakad (chart px about 2500, 5740, outside
  the window) reads "There is good and safe Anchorage during the S.W. Monsoon after
  1st burst in June. The Rise of tide is very little at any time 3 feet at the highest
  Springs, and 1 or 2 at neaps. H.W.F. & C. about 2h 0m."
Nircum town mark and name: S0200, window (940, 483). Porakad name: S0297, (1101, 949).

Second pass (check sheets): one value changed, S0103 (under the green line, could be
6 or 8) from 6 to drop; two positions corrected (A004 and A015), no status changes.
"""
# detector id -> (value in fathoms or None, status)
READ = {
 # tile 00
 'S0000': (5.25,'ok'), 'S0001': (5.25,'ok'), 'S0002': (7,'ok'), 'S0003': (4.75,'ok'), 'S0004': (6,'ok'),
 'S0005': (7,'ok'), 'S0006': (4.75,'ok'), 'S0007': (6,'ok'), 'S0008': (5,'ok'), 'S0009': (6,'ok'),
 'S0010': (5.25,'ok'), 'S0011': (6,'ok'), 'S0012': (6,'ok'), 'S0013': (4.5,'ok'), 'S0014': (5,'ok'),
 'S0015': (5.5,'ok'), 'S0016': (6,'ok'), 'S0017': (7,'ok'), 'S0018': (6,'ok'), 'S0019': (7,'ok'),
 'S0020': (4.5,'ok'), 'S0021': (5.5,'ok'), 'S0022': (7,'ok'), 'S0023': (5,'ok'), 'S0024': (6,'ok'),
 'S0025': (8,'ok'), 'S0026': (6,'ok'), 'S0027': (5.5,'ok'), 'S0028': (7,'ok'), 'S0029': (6,'ok'),
 'S0030': (8,'ok'), 'S0031': (5.5,'ok'), 'S0032': (7,'ok'), 'S0033': (6,'ok'), 'S0034': (6,'ok'),
 'S0035': (7,'ok'), 'S0036': (6,'ok'), 'S0037': (5.5,'ok'), 'S0038': (6,'ok'), 'S0039': (7,'ok'),
 'S0040': (8,'ok'), 'S0041': (7,'ok'), 'S0042': (8,'ok'), 'S0043': (6,'ok'), 'S0044': (6,'ok'),
 # tile 01
 'S0045': (None,'not'), 'S0046': (4,'ok'), 'S0047': (1.5,'ok'), 'S0048': (4,'ok'), 'S0049': (2.5,'ok'),
 'S0050': (None,'not'), 'S0051': (1.75,'ok'), 'S0052': (4,'ok'), 'S0053': (None,'split'), 'S0054': (2,'ok'),
 'S0055': (4,'ok'), 'S0056': (4,'ok'), 'S0057': (3.25,'ok'), 'S0058': (0.5,'unsure'), 'S0059': (4.25,'ok'),
 'S0060': (2.5,'ok'), 'S0061': (1,'ok'), 'S0062': (2.75,'ok'), 'S0063': (2,'ok'), 'S0064': (1.75,'ok'),
 'S0065': (4.25,'ok'), 'S0066': (3,'ok'), 'S0067': (4,'ok'), 'S0068': (2,'ok'), 'S0069': (4,'ok'),
 'S0070': (None,'not'), 'S0071': (2.25,'ok'), 'S0072': (4,'ok'), 'S0073': (3.5,'ok'), 'S0074': (4.25,'ok'),
 'S0075': (2.5,'ok'), 'S0076': (2.5,'ok'), 'S0077': (2,'ok'), 'S0078': (4.25,'ok'), 'S0079': (4,'ok'),
 'S0080': (4.5,'unsure'), 'S0081': (None,'split'), 'S0082': (4,'ok'), 'S0083': (None,'split'), 'S0084': (4.25,'ok'),
 'S0085': (4.75,'unsure'), 'S0086': (4.25,'ok'), 'S0087': (1.5,'ok'), 'S0088': (3,'ok'), 'S0089': (5,'ok'),
 'S0090': (4.5,'ok'), 'S0091': (None,'not'), 'S0092': (2,'ok'),
 # tiles 02, 03 (land: river banks)
 'S0093': (None,'not'), 'S0094': (None,'not'), 'S0095': (None,'not'), 'S0096': (None,'not'),
 # tile 10 (S0129, S0135: two of the five lighter upright 4 3/4 bracketed by "(soundings in 1901)")
 'S0097': (8,'ok'), 'S0098': (8,'ok'), 'S0099': (6,'ok'), 'S0100': (7,'ok'), 'S0101': (9,'ok'),
 'S0102': (7,'ok'), 'S0103': (None,'drop'), 'S0104': (8,'ok'), 'S0105': (7,'ok'), 'S0106': (9,'ok'),
 'S0107': (6,'ok'), 'S0108': (7,'ok'), 'S0109': (6,'ok'), 'S0110': (8,'ok'), 'S0111': (9,'ok'),
 'S0112': (7,'ok'), 'S0113': (6,'ok'), 'S0114': (6,'ok'), 'S0115': (8,'ok'), 'S0116': (9,'ok'),
 'S0117': (7,'ok'), 'S0118': (9,'ok'), 'S0119': (6,'ok'), 'S0120': (None,'edge'), 'S0121': (7,'ok'),
 'S0122': (6,'ok'), 'S0123': (7,'ok'), 'S0124': (8,'ok'), 'S0125': (9,'ok'), 'S0126': (7,'ok'),
 'S0127': (6,'ok'), 'S0128': (6,'ok'), 'S0129': (4.75,'later'), 'S0130': (10,'ok'), 'S0131': (6,'ok'),
 'S0132': (9,'ok'), 'S0133': (None,'not'), 'S0134': (None,'not'), 'S0135': (4.75,'later'), 'S0136': (9,'ok'),
 'S0137': (10,'ok'), 'S0138': (None,'not'), 'S0139': (6,'ok'), 'S0140': (9,'ok'),
 # tile 11
 'S0141': (1.5,'ok'), 'S0142': (0.25,'unsure'), 'S0143': (5,'ok'), 'S0144': (5,'ok'), 'S0145': (3,'ok'),
 'S0146': (5,'ok'), 'S0147': (None,'split'), 'S0148': (0.5,'unsure'), 'S0149': (5,'ok'), 'S0150': (3.5,'ok'),
 'S0151': (2.75,'ok'), 'S0152': (5,'ok'), 'S0153': (0.5,'unsure'), 'S0154': (3,'ok'), 'S0155': (5.5,'ok'),
 'S0156': (5.25,'ok'), 'S0157': (6,'ok'), 'S0158': (1.5,'ok'), 'S0159': (5.5,'ok'), 'S0160': (5.25,'ok'),
 'S0161': (2,'ok'), 'S0162': (4.5,'ok'), 'S0163': (3.5,'ok'), 'S0164': (4.25,'ok'), 'S0165': (6,'ok'),
 'S0166': (5.5,'ok'), 'S0167': (5.5,'ok'), 'S0168': (3,'ok'), 'S0169': (4.25,'ok'), 'S0170': (5,'ok'),
 'S0171': (2.5,'ok'), 'S0172': (4.5,'ok'), 'S0173': (5,'ok'), 'S0174': (3,'ok'), 'S0175': (6,'ok'),
 'S0176': (5,'ok'), 'S0177': (5,'ok'), 'S0178': (5.5,'ok'), 'S0179': (3,'ok'), 'S0180': (6,'ok'),
 'S0181': (4,'ok'), 'S0182': (5.75,'ok'), 'S0183': (5.5,'ok'), 'S0184': (5.25,'ok'), 'S0185': (3.5,'ok'),
 'S0186': (6,'ok'), 'S0187': (5.5,'ok'), 'S0188': (None,'not'), 'S0189': (6,'ok'), 'S0190': (6,'ok'),
 'S0191': (3.75,'ok'), 'S0192': (4,'ok'), 'S0193': (4.75,'ok'), 'S0194': (None,'split'), 'S0195': (5,'ok'),
 'S0196': (6,'ok'), 'S0197': (6,'ok'), 'S0198': (6,'ok'),
 # tile 12 (S0200 is the town mark and name "Nircum")
 'S0199': (None,'not'), 'S0200': (None,'not'), 'S0201': (1,'ok'), 'S0202': (1.25,'ok'), 'S0203': (1,'ok'),
 'S0204': (2,'ok'), 'S0205': (0.5,'unsure'), 'S0206': (2.5,'ok'), 'S0207': (0.75,'unsure'),
 # tile 13 (land: river bank)
 'S0208': (None,'not'),
 # tile 20 (S0213, S0219: two more of the bracketed 1901 4 3/4; S0221 is "in" of the label)
 'S0209': (9,'ok'), 'S0210': (10,'ok'), 'S0211': (10,'ok'), 'S0212': (None,'edge'), 'S0213': (4.75,'later'),
 'S0214': (9,'ok'), 'S0215': (9,'ok'), 'S0216': (11,'ok'), 'S0217': (10,'ok'), 'S0218': (8,'ok'),
 'S0219': (4.75,'later'), 'S0220': (10,'ok'), 'S0221': (None,'not'), 'S0222': (8,'ok'), 'S0223': (10,'ok'),
 'S0224': (9,'ok'), 'S0225': (11,'ok'), 'S0226': (10,'ok'), 'S0227': (9,'ok'), 'S0228': (10,'ok'),
 'S0229': (12,'ok'), 'S0230': (9,'ok'), 'S0231': (12,'ok'), 'S0232': (12,'ok'), 'S0233': (9,'ok'),
 'S0234': (9,'ok'), 'S0235': (13,'ok'), 'S0236': (None,'edge'), 'S0237': (8,'ok'), 'S0238': (11,'ok'),
 'S0239': (14,'ok'), 'S0240': (11,'ok'), 'S0241': (9,'ok'), 'S0242': (9,'ok'), 'S0243': (9,'ok'),
 'S0244': (None,'edge'), 'S0245': (12,'ok'), 'S0246': (11,'ok'), 'S0247': (12,'ok'),
 # tile 21 (S0279: the fifth bracketed 1901 4 3/4; S0262 is "soft" of "soft mud")
 'S0248': (4.5,'ok'), 'S0249': (4,'ok'), 'S0250': (4.25,'ok'), 'S0251': (6,'ok'), 'S0252': (4.5,'ok'),
 'S0253': (5,'ok'), 'S0254': (4,'ok'), 'S0255': (6,'ok'), 'S0256': (5.75,'ok'), 'S0257': (5,'ok'),
 'S0258': (6,'ok'), 'S0259': (6,'ok'), 'S0260': (4.5,'ok'), 'S0261': (5.25,'ok'), 'S0262': (None,'not'),
 'S0263': (6,'ok'), 'S0264': (5.25,'ok'), 'S0265': (4.75,'ok'), 'S0266': (5.25,'ok'), 'S0267': (6,'ok'),
 'S0268': (7,'ok'), 'S0269': (4.5,'ok'), 'S0270': (5,'ok'), 'S0271': (5.5,'ok'), 'S0272': (6,'ok'),
 'S0273': (5,'ok'), 'S0274': (5.75,'ok'), 'S0275': (5,'ok'), 'S0276': (5.75,'ok'), 'S0277': (6,'ok'),
 'S0278': (5,'ok'), 'S0279': (4.75,'later'), 'S0280': (5.5,'ok'), 'S0281': (7,'ok'), 'S0282': (6,'ok'),
 'S0283': (7,'ok'), 'S0284': (6,'ok'), 'S0285': (8,'ok'), 'S0286': (6,'ok'), 'S0287': (6,'ok'),
 'S0288': (6,'ok'), 'S0289': (5,'ok'), 'S0290': (7,'ok'), 'S0291': (8,'ok'), 'S0292': (5.5,'ok'),
 'S0293': (6,'ok'),
 # tile 22 (S0297, S0298 "Porakad (Porca)"; S0320, S0321 "South Vazhapuram")
 'S0294': (None,'split'), 'S0295': (3.5,'ok'), 'S0296': (3.5,'ok'), 'S0297': (None,'not'), 'S0298': (None,'not'),
 'S0299': (3,'ok'), 'S0300': (3.75,'ok'), 'S0301': (2.5,'ok'), 'S0302': (4,'ok'), 'S0303': (1,'ok'),
 'S0304': (0.75,'unsure'), 'S0305': (3.75,'ok'), 'S0306': (1.5,'ok'), 'S0307': (4,'ok'), 'S0308': (2.25,'ok'),
 'S0309': (3.75,'ok'), 'S0310': (2.5,'ok'), 'S0311': (4,'ok'), 'S0312': (4.5,'ok'), 'S0313': (3,'ok'),
 'S0314': (2.5,'ok'), 'S0315': (None,'split'), 'S0316': (3.5,'ok'), 'S0317': (3,'ok'), 'S0318': (1.75,'ok'),
 'S0319': (4,'ok'), 'S0320': (None,'not'), 'S0321': (None,'not'), 'S0322': (3,'ok'), 'S0323': (2,'ok'),
 'S0324': (4.5,'ok'), 'S0325': (3.25,'ok'), 'S0326': (3.25,'ok'), 'S0327': (3.5,'ok'), 'S0328': (4.75,'ok'),
 # tile 23 (land: river banks)
 'S0329': (None,'not'), 'S0330': (None,'not'), 'S0331': (None,'not'), 'S0332': (None,'not'),
 # tile 30
 'S0333': (13,'ok'), 'S0334': (8,'ok'), 'S0335': (11,'ok'), 'S0336': (12,'ok'), 'S0337': (9,'ok'),
 'S0338': (12,'ok'), 'S0339': (9,'ok'), 'S0340': (12,'ok'), 'S0341': (11,'ok'), 'S0342': (13,'ok'),
 'S0343': (11,'ok'), 'S0344': (12,'ok'), 'S0345': (12,'ok'), 'S0346': (10,'ok'), 'S0347': (10,'ok'),
 'S0348': (13,'ok'), 'S0349': (15,'ok'), 'S0350': (13,'ok'), 'S0351': (10,'ok'), 'S0352': (11,'ok'),
 'S0353': (11,'ok'), 'S0354': (13,'ok'), 'S0355': (None,'edge'),
 # tile 31
 'S0356': (8,'ok'), 'S0357': (6,'ok'), 'S0358': (6,'ok'), 'S0359': (6,'ok'), 'S0360': (6,'ok'),
 'S0361': (8,'ok'), 'S0362': (6,'ok'), 'S0363': (7,'ok'), 'S0364': (8,'ok'), 'S0365': (6,'ok'),
 'S0366': (8,'ok'), 'S0367': (8,'ok'), 'S0368': (9,'ok'), 'S0369': (7,'ok'), 'S0370': (9,'ok'),
 'S0371': (7,'ok'), 'S0372': (8,'ok'), 'S0373': (6,'ok'), 'S0374': (7,'ok'), 'S0375': (6,'ok'),
 'S0376': (6,'ok'), 'S0377': (9,'ok'), 'S0378': (8,'ok'), 'S0379': (9,'ok'), 'S0380': (8,'ok'),
 'S0381': (9,'ok'), 'S0382': (7,'ok'), 'S0383': (7,'ok'), 'S0384': (10,'ok'), 'S0385': (9,'ok'),
 'S0386': (8,'ok'),
 # tile 32
 'S0387': (5,'ok'), 'S0388': (None,'not'), 'S0389': (4,'ok'), 'S0390': (3.5,'ok'), 'S0391': (4.5,'ok'),
 'S0392': (5,'ok'), 'S0393': (4.5,'ok'), 'S0394': (4.5,'ok'), 'S0395': (5,'ok'), 'S0396': (5.25,'ok'),
 'S0397': (4,'ok'), 'S0398': (None,'not'), 'S0399': (4.25,'ok'), 'S0400': (5.5,'ok'), 'S0401': (3,'ok'),
 'S0402': (4.5,'ok'), 'S0403': (6,'ok'), 'S0404': (4.5,'ok'), 'S0405': (5,'ok'), 'S0406': (3.5,'ok'),
 'S0407': (6,'ok'), 'S0408': (4.5,'ok'), 'S0409': (3,'ok'), 'S0410': (6,'ok'), 'S0411': (5,'ok'),
 'S0412': (3.5,'ok'), 'S0413': (4,'ok'), 'S0414': (5.25,'ok'), 'S0415': (5,'ok'), 'S0416': (4.25,'ok'),
 'S0417': (6,'ok'), 'S0418': (4.5,'ok'), 'S0419': (5.5,'ok'), 'S0420': (5.5,'ok'), 'S0421': (6,'ok'),
 'S0422': (4.5,'ok'), 'S0423': (1,'ok'), 'S0424': (5,'ok'), 'S0425': (3,'ok'), 'S0426': (6,'ok'),
 'S0427': (6,'ok'), 'S0428': (5.5,'ok'), 'S0429': (5,'ok'), 'S0430': (5.25,'ok'), 'S0431': (3.5,'ok'),
 'S0432': (6,'ok'), 'S0433': (6,'ok'), 'S0434': (5.25,'ok'), 'S0435': (6,'ok'), 'S0436': (3.5,'ok'),
 # tile 33
 'S0437': (2,'ok'),
}

# numbers the detector missed or merged: (window_x, window_y, fathoms, status, note)
ADDED = [
 # tile 00
 (94, 235, 7, 'ok', 'missed'), (141, 261, 7, 'ok', 'missed'),
 # tile 01
 (535, 32, 2.5, 'ok', 'missed'), (603, 25, 1.5, 'ok', 'missed'),
 (527, 117, 3.5, 'ok', 'split from S0053; position corrected on check'), (560, 108, 3, 'ok', 'split from S0053'),
 (617, 250, 3, 'ok', 'missed, on contour'), (628, 286, 3, 'ok', 'missed, on contour'),
 (720, 253, 0.5, 'unsure', 'missed lone fraction'), (733, 314, 1.5, 'ok', 'missed'),
 (731, 362, 1.5, 'ok', 'split from S0081'), (757, 360, 0.5, 'unsure', 'split from S0081'),
 (655, 372, 3.25, 'ok', 'split from S0083'), (697, 357, 2, 'ok', 'split from S0083'),
 # tile 10
 (22, 707, 10, 'ok', 'missed, under red line'), (35, 787, 10, 'ok', 'missed, under red line; position corrected on check'),
 # tile 11
 (757, 463, 2.25, 'ok', 'split from S0147'), (783, 477, 1.5, 'ok', 'split from S0147'),
 (616, 569, 4.5, 'ok', 'missed, on meridian'), (632, 616, 4.5, 'ok', 'missed, on meridian'),
 (750, 571, 3, 'ok', 'missed, on contour'), (772, 599, 3, 'ok', 'missed, on contour'),
 (603, 647, 4.5, 'ok', 'missed, on contour'), (635, 664, 4.75, 'ok', 'missed, on meridian'),
 (542, 688, 5.5, 'ok', 'missed'), (628, 837, 5.5, 'ok', 'missed, on meridian'),
 (695, 803, 5, 'ok', 'split from S0194 (5 above the letter R)'),
 # tile 12
 (857, 722, 2, 'ok', 'missed'), (861, 752, 2.25, 'ok', 'missed'), (854, 780, 2, 'ok', 'missed'),
 # tile 20
 (100, 930, 10, 'ok', 'missed, under red line'), (145, 1030, 10, 'ok', 'missed, under red line'),
 (167, 1130, 10, 'ok', 'missed, under red line'), (265, 1155, 10, 'ok', 'missed, under red line'),
 (125, 1217, 12, 'ok', 'missed, under brown line'),
 # tile 21
 (689, 852, 4.75, 'ok', 'missed, below the R mark'), (620, 878, 5.25, 'ok', 'missed, on meridian'),
 (817, 975, 4.25, 'ok', 'missed, below "soft mud"'), (617, 1147, 6, 'ok', 'missed, under green line'),
 (774, 1172, 5.75, 'ok', 'missed, on parallel'),
 # tile 22
 (889, 853, 3, 'ok', 'split from S0294'), (918, 857, 1.5, 'ok', 'split from S0294'),
 (886, 1155, 4, 'ok', 'split from S0315'), (886, 1180, 4.5, 'ok', 'split from S0315'),
 (864, 940, 4, 'ok', 'missed'), (912, 1166, 4, 'ok', 'missed, on parallel'),
 # tile 30
 (295, 1290, 10, 'ok', 'missed, under red line'), (370, 1455, 10, 'ok', 'missed, under red line'),
 (387, 1572, 10, 'ok', 'missed'),
 # tile 31
 (632, 1262, 6, 'ok', 'missed, on meridian'), (630, 1385, 7, 'ok', 'missed, on meridian'),
 (700, 1502, 7, 'ok', 'missed'), (682, 1567, 7, 'ok', 'missed'), (795, 1590, 7, 'ok', 'missed, under green line'),
 # tile 32
 (1134, 1337, 2, 'ok', 'missed'), (1140, 1375, 2, 'ok', 'missed'), (1180, 1435, 2, 'ok', 'missed'),
 (895, 1647, 7, 'ok', 'missed'), (1175, 1673, 5, 'ok', 'missed'),
]

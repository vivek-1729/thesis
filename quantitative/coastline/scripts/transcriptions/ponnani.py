"""Hand transcription of soundings in the ponnani window of BA 749 (Selby, surveyed 1851-3, 1:146,000).

Site: ponnani (Ponnani, a candidate for Tyndis). Window (3300, 2200, 4900, 3800) in chart pixels of
malabar-749-1857.jpg; soundings in fathoms. Values were read by eye from the numbered tiles in
data/soundings/ponnani/tiles/.
Status codes:
  ok        clear reading
  unsure    legible but could be misread, or a lone fraction that may not be a sounding
  edge      cut by the window border; excluded from modelling
  drop      ambiguous on the second check; excluded
  not       detector picked up something that is not a sounding (text, palm, bank line, island)
  split     detector box merged two numbers (or a number and text); the numbers are in ADDED
Rows starting with 'A' are numbers the detector missed. Their position is the
window pixel I read off the tile image (accurate to roughly +/- 5 chart px).

Second pass (contact sheets in data/soundings/ponnani/check/): no values changed. Three positions
of hand-added numbers were corrected (A004, A005, A007, each off by 10-20 px from an arithmetic slip
in converting tile pixels), checked against the ink centroid of every added number.
Edge readings: S0110, S0201, S0304 (left border) and S0318, S0319 (bottom border) are clipped by the
window but legible, so they are kept as unsure; S0000, S0023, S0186 are cut too far to read.
No later additions or unusual notation in this window. Bottom-quality notes (m, s, m.sh, s.m)
are marked not; lone fraction S0257 (1/2, close inshore north of the river mouth) is unsure.
"""
# detector id -> (value in fathoms or None, status)
READ = {
 # tile 00
 'S0000': (None,'edge'), 'S0001': (11,'ok'), 'S0002': (9,'ok'), 'S0003': (13,'ok'), 'S0004': (11,'ok'),
 'S0005': (12,'ok'), 'S0006': (14,'ok'), 'S0007': (11,'ok'), 'S0008': (9,'ok'), 'S0009': (12,'ok'),
 'S0010': (11,'ok'), 'S0011': (12,'ok'), 'S0012': (11,'ok'), 'S0013': (10,'ok'), 'S0014': (11,'ok'),
 'S0015': (11,'ok'), 'S0016': (12,'ok'), 'S0017': (10,'ok'), 'S0018': (11,'ok'), 'S0019': (12,'ok'),
 'S0020': (13,'ok'), 'S0021': (12,'ok'), 'S0022': (9,'ok'), 'S0023': (None,'edge'), 'S0024': (12,'ok'),
 'S0025': (10,'ok'), 'S0026': (12,'ok'),
 # tile 01
 'S0027': (6,'ok'), 'S0028': (3.25,'ok'), 'S0029': (9,'ok'), 'S0030': (7,'ok'), 'S0031': (9,'ok'),
 'S0032': (2.5,'ok'), 'S0033': (5,'ok'), 'S0034': (2,'ok'), 'S0035': (4,'ok'), 'S0036': (8,'ok'),
 'S0037': (9,'ok'), 'S0038': (5.5,'ok'), 'S0039': (1,'ok'), 'S0040': (5,'ok'), 'S0041': (4,'ok'),
 'S0042': (6,'ok'), 'S0043': (9,'ok'), 'S0044': (8,'ok'), 'S0045': (2,'ok'), 'S0046': (6,'ok'),
 'S0047': (5.5,'ok'), 'S0048': (9,'ok'), 'S0049': (4,'ok'), 'S0050': (5,'ok'), 'S0051': (1.5,'ok'),
 'S0052': (5.5,'ok'), 'S0053': (7,'ok'), 'S0054': (2.5,'ok'), 'S0055': (10,'ok'), 'S0056': (6,'ok'),
 'S0057': (5.5,'ok'), 'S0058': (9,'ok'), 'S0059': (5.5,'ok'), 'S0060': (8,'ok'), 'S0061': (4,'ok'),
 'S0062': (5,'ok'), 'S0063': (9,'ok'), 'S0064': (6,'ok'), 'S0065': (4.5,'ok'), 'S0066': (8,'ok'),
 'S0067': (3,'ok'), 'S0068': (9,'ok'), 'S0069': (5,'ok'), 'S0070': (5.5,'ok'), 'S0071': (3,'ok'),
 'S0072': (8,'ok'), 'S0073': (7,'ok'), 'S0074': (2,'ok'), 'S0075': (5.5,'ok'), 'S0076': (5.25,'ok'),
 'S0077': (3.5,'ok'), 'S0078': (2.5,'ok'), 'S0079': (6,'ok'), 'S0080': (8,'ok'), 'S0081': (7,'ok'),
 # tiles 02, 03
 'S0082': (None,'not'), 'S0083': (None,'not'), 'S0084': (None,'not'), 'S0085': (None,'not'),
 'S0086': (2.25,'ok'), 'S0087': (None,'not'), 'S0088': (1.5,'ok'), 'S0089': (None,'not'),
 # tile 10
 'S0090': (11,'ok'), 'S0091': (10,'ok'), 'S0092': (14,'ok'), 'S0093': (12,'ok'), 'S0094': (11,'ok'),
 'S0095': (13,'ok'), 'S0096': (14,'ok'), 'S0097': (11,'ok'), 'S0098': (12,'ok'), 'S0099': (11,'ok'),
 'S0100': (14,'ok'), 'S0101': (12,'ok'), 'S0102': (11,'ok'), 'S0103': (13,'ok'), 'S0104': (15,'ok'),
 'S0105': (12,'ok'), 'S0106': (13,'ok'), 'S0107': (11,'ok'), 'S0108': (10,'ok'), 'S0109': (13,'ok'),
 'S0110': (15,'unsure'), 'S0111': (10,'ok'), 'S0112': (10,'ok'), 'S0113': (9,'ok'),
 # tile 11
 'S0114': (5.5,'ok'), 'S0115': (2,'ok'), 'S0116': (4,'ok'), 'S0117': (6,'ok'), 'S0118': (8,'ok'),
 'S0119': (5.5,'ok'), 'S0120': (8,'ok'), 'S0121': (8,'ok'), 'S0122': (5,'ok'), 'S0123': (6,'ok'),
 'S0124': (9,'ok'), 'S0125': (5.25,'ok'), 'S0126': (None,'split'), 'S0127': (6,'ok'), 'S0128': (4,'ok'),
 'S0129': (5,'ok'), 'S0130': (3.5,'ok'), 'S0131': (9,'ok'), 'S0132': (8,'ok'), 'S0133': (4.5,'ok'),
 'S0134': (6,'ok'), 'S0135': (10,'ok'), 'S0136': (9,'ok'), 'S0137': (None,'split'), 'S0138': (7,'ok'),
 'S0139': (8,'ok'), 'S0140': (6,'ok'), 'S0141': (9,'ok'), 'S0142': (9,'ok'), 'S0143': (5,'ok'),
 'S0144': (8,'ok'), 'S0145': (9,'ok'), 'S0146': (4.5,'ok'), 'S0147': (9,'ok'), 'S0148': (5.5,'ok'),
 'S0149': (7,'ok'), 'S0150': (9,'ok'), 'S0151': (8,'ok'), 'S0152': (5.5,'ok'), 'S0153': (4,'ok'),
 'S0154': (6,'ok'), 'S0155': (7,'ok'), 'S0156': (8,'ok'), 'S0157': (6,'ok'), 'S0158': (6,'ok'),
 # tile 12
 'S0159': (2,'ok'), 'S0160': (None,'not'), 'S0161': (2.5,'ok'), 'S0162': (1.5,'ok'), 'S0163': (None,'not'),
 'S0164': (None,'not'), 'S0165': (None,'not'), 'S0166': (None,'not'), 'S0167': (None,'split'),
 'S0168': (None,'not'), 'S0169': (3,'ok'), 'S0170': (None,'split'), 'S0171': (None,'not'),
 'S0172': (None,'split'), 'S0173': (1,'ok'), 'S0174': (None,'not'), 'S0175': (None,'not'),
 'S0176': (3.5,'ok'), 'S0177': (4,'ok'), 'S0178': (2.25,'ok'), 'S0179': (2.5,'ok'), 'S0180': (3,'ok'),
 'S0181': (2,'ok'),
 # tile 13
 'S0182': (None,'not'), 'S0183': (None,'not'), 'S0184': (None,'not'),
 # tile 20
 'S0185': (11,'ok'), 'S0186': (None,'edge'), 'S0187': (11,'ok'), 'S0188': (10,'ok'), 'S0189': (11,'ok'),
 'S0190': (10,'ok'), 'S0191': (11,'ok'), 'S0192': (10,'ok'), 'S0193': (10,'ok'), 'S0194': (10,'ok'),
 'S0195': (10,'ok'), 'S0196': (11,'ok'), 'S0197': (11,'ok'), 'S0198': (11,'ok'), 'S0199': (10,'ok'),
 'S0200': (10,'ok'), 'S0201': (12,'unsure'), 'S0202': (11,'ok'), 'S0203': (12,'ok'), 'S0204': (11,'ok'),
 'S0205': (11,'ok'), 'S0206': (12,'ok'), 'S0207': (12,'ok'), 'S0208': (11,'ok'), 'S0209': (11,'ok'),
 # tile 21
 'S0210': (9,'ok'), 'S0211': (5.5,'ok'), 'S0212': (6,'ok'), 'S0213': (9,'ok'), 'S0214': (5,'ok'),
 'S0215': (6,'ok'), 'S0216': (5.5,'ok'), 'S0217': (10,'ok'), 'S0218': (8,'ok'), 'S0219': (9,'ok'),
 'S0220': (6,'ok'), 'S0221': (9,'ok'), 'S0222': (5.5,'ok'), 'S0223': (6,'ok'), 'S0224': (None,'not'),
 'S0225': (10,'ok'), 'S0226': (8,'ok'), 'S0227': (8,'ok'), 'S0228': (6,'ok'), 'S0229': (9,'ok'),
 'S0230': (10,'ok'), 'S0231': (6,'ok'), 'S0232': (9,'ok'), 'S0233': (8,'ok'), 'S0234': (6,'ok'),
 'S0235': (7,'ok'), 'S0236': (9,'ok'), 'S0237': (6,'ok'), 'S0238': (9,'ok'), 'S0239': (8,'ok'),
 'S0240': (8,'ok'), 'S0241': (8,'ok'), 'S0242': (7,'ok'), 'S0243': (8,'ok'), 'S0244': (9,'ok'),
 'S0245': (8,'ok'), 'S0246': (8,'ok'), 'S0247': (7,'ok'), 'S0248': (8,'ok'), 'S0249': (9,'ok'),
 'S0250': (7,'ok'), 'S0251': (9,'ok'), 'S0252': (9,'ok'), 'S0253': (8,'ok'), 'S0254': (8,'ok'),
 'S0255': (9,'ok'),
 # tile 22
 'S0256': (4,'ok'), 'S0257': (0.5,'unsure'), 'S0258': (2.5,'ok'), 'S0259': (3,'ok'), 'S0260': (4.5,'ok'),
 'S0261': (2,'ok'), 'S0262': (None,'not'), 'S0263': (4.5,'ok'), 'S0264': (None,'split'), 'S0265': (5,'ok'),
 'S0266': (None,'split'), 'S0267': (4,'ok'), 'S0268': (3,'ok'), 'S0269': (1,'ok'), 'S0270': (2,'ok'),
 'S0271': (2.75,'ok'), 'S0272': (None,'not'), 'S0273': (3,'ok'), 'S0274': (2,'ok'), 'S0275': (6,'ok'),
 'S0276': (None,'not'), 'S0277': (3.25,'ok'), 'S0278': (5.75,'ok'), 'S0279': (2.5,'ok'), 'S0280': (5.5,'ok'),
 'S0281': (5.5,'ok'), 'S0282': (1,'ok'), 'S0283': (6,'ok'), 'S0284': (3,'ok'), 'S0285': (5,'ok'),
 'S0286': (2,'ok'), 'S0287': (3,'ok'), 'S0288': (4.5,'ok'), 'S0289': (6,'ok'), 'S0290': (2,'ok'),
 'S0291': (3,'ok'), 'S0292': (4,'ok'), 'S0293': (6,'ok'), 'S0294': (2.5,'ok'), 'S0295': (4,'ok'),
 'S0296': (6,'ok'), 'S0297': (3.25,'ok'),
 # tile 23
 'S0298': (None,'not'),
 # tile 30
 'S0299': (13,'ok'), 'S0300': (12,'ok'), 'S0301': (11,'ok'), 'S0302': (11,'ok'), 'S0303': (11,'ok'),
 'S0304': (13,'unsure'), 'S0305': (11,'ok'), 'S0306': (11,'ok'), 'S0307': (12,'ok'), 'S0308': (13,'ok'),
 'S0309': (11,'ok'), 'S0310': (12,'ok'), 'S0311': (13,'ok'), 'S0312': (12,'ok'), 'S0313': (13,'ok'),
 'S0314': (13,'ok'), 'S0315': (12,'ok'), 'S0316': (12,'ok'), 'S0317': (12,'ok'), 'S0318': (13,'unsure'),
 'S0319': (12,'unsure'),
 # tile 31
 'S0320': (9,'ok'), 'S0321': (10,'ok'), 'S0322': (9,'ok'), 'S0323': (8,'ok'), 'S0324': (9,'ok'),
 'S0325': (10,'ok'), 'S0326': (8,'ok'), 'S0327': (9,'ok'), 'S0328': (9,'ok'), 'S0329': (9,'ok'),
 'S0330': (10,'ok'), 'S0331': (10,'ok'), 'S0332': (10,'ok'), 'S0333': (10,'ok'), 'S0334': (9,'ok'),
 'S0335': (10,'ok'), 'S0336': (9,'ok'), 'S0337': (10,'ok'), 'S0338': (12,'ok'), 'S0339': (12,'ok'),
 # tile 32
 'S0340': (3,'ok'), 'S0341': (6,'ok'), 'S0342': (3.5,'ok'), 'S0343': (7,'ok'), 'S0344': (3,'ok'),
 'S0345': (5.5,'ok'), 'S0346': (2.5,'ok'), 'S0347': (None,'split'), 'S0348': (6,'ok'), 'S0349': (2,'ok'),
 'S0350': (5.5,'ok'), 'S0351': (1.5,'ok'), 'S0352': (3.5,'ok'), 'S0353': (4.75,'ok'), 'S0354': (6,'ok'),
 'S0355': (2.5,'ok'), 'S0356': (5,'ok'), 'S0357': (8,'ok'), 'S0358': (5.25,'ok'), 'S0359': (4,'ok'),
 'S0360': (6,'ok'), 'S0361': (6,'ok'), 'S0362': (3.5,'ok'), 'S0363': (8,'ok'), 'S0364': (7,'ok'),
 'S0365': (3,'ok'), 'S0366': (8,'ok'), 'S0367': (6,'ok'),
 # tile 33
 'S0368': (None,'not'), 'S0369': (2.25,'ok'), 'S0370': (2.5,'ok'), 'S0371': (1,'ok'), 'S0372': (None,'not'),
 'S0373': (2,'ok'),
}

# numbers the detector missed or merged: (window_x, window_y, fathoms, status, note)
ADDED = [
 # tile 00
 (170, 310, 12, 'ok', 'missed'), (265, 297, 12, 'ok', 'missed'), (332, 404, 10, 'ok', 'missed, on contour'),
 # tile 01
 (582, 82, 7, 'ok', 'missed'), (566, 175, 7, 'ok', 'missed; position corrected on check'), (568, 237, 7, 'ok', 'missed; position corrected on check'),
 (765, 140, 4.25, 'ok', 'missed, on dotted line'), (805, 237, 3.25, 'ok', 'missed, on dotted line; position corrected on check'),
 # tile 11
 (592, 565, 8, 'ok', 'split from S0126 (with "m")'), (753, 645, 5, 'ok', 'split from S0137 (under "Isolated")'),
 (536, 474, 7, 'ok', 'missed'), (581, 462, 7, 'ok', 'missed'), (616, 515, 7, 'ok', 'missed'),
 (653, 592, 7, 'ok', 'missed'), (637, 668, 7, 'ok', 'missed'),
 (791, 669, 4.75, 'ok', 'missed'), (822, 739, 4.25, 'ok', 'missed'), (845, 847, 4.25, 'ok', 'missed'),
 # tile 12
 (875, 599, 3, 'ok', 'split from S0167 (with "Grove")'), (951, 716, 1.5, 'ok', 'split from S0170 (with "s")'),
 (912, 727, 2.5, 'ok', 'split from S0172'), (877, 746, 3.5, 'ok', 'split from S0172'),
 # tile 20
 (59, 912, 12, 'ok', 'missed'), (252, 920, 10, 'ok', 'missed, on contour'), (82, 1270, 12, 'ok', 'missed'),
 # tile 21
 (577, 867, 7, 'ok', 'missed'), (614, 905, 7, 'ok', 'missed'), (671, 975, 7, 'ok', 'missed'),
 (842, 1217, 7, 'ok', 'missed'), (782, 1257, 7, 'ok', 'missed'), (455, 1240, 10, 'ok', 'missed, on contour'),
 # tile 22
 (997, 954, 3.5, 'ok', 'split from S0264'), (1036, 959, 2.5, 'ok', 'split from S0264'),
 (1071, 962, 2, 'ok', 'split from S0266'), (1095, 955, 1, 'ok', 'split from S0266'),
 # tile 30
 (185, 1360, 12, 'ok', 'missed'), (300, 1472, 12, 'ok', 'missed, after "s.m"'),
 # tile 31
 (590, 1322, 10, 'ok', 'missed'), (602, 1375, 10, 'ok', 'missed, after "m.sh"'),
 (605, 1497, 10, 'ok', 'missed, on contour'), (617, 1557, 10, 'ok', 'missed, on contour'),
 (765, 1572, 10, 'ok', 'missed'),
 # tile 32
 (1155, 1362, 3.75, 'ok', 'split from S0347 (with "m")'),
 (902, 1387, 7, 'ok', 'missed'), (855, 1405, 7, 'ok', 'missed'), (890, 1447, 7, 'ok', 'missed'),
 (930, 1492, 7, 'ok', 'missed'), (982, 1515, 7, 'ok', 'missed'),
 (1127, 1452, 4.5, 'ok', 'missed, on dotted line'), (1172, 1477, 4.5, 'ok', 'missed'),
 (1162, 1564, 5.25, 'ok', 'missed'), (1207, 1565, 4.5, 'ok', 'missed'),
]

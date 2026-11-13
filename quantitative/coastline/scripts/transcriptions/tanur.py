"""Hand transcription of soundings in the tanur window of BA 749.

Site: tanur (candidate for Tyndis). Sheet: Admiralty 749 (Selby, surveyed 1851-3,
1:146,000, soundings in fathoms). Window: chart pixels (3000, 450) to (4600, 2050).
The top of the window runs into the sheet's top border and longitude scale; the
right half is land (palms, Tanur village) and carries no soundings.

Values were read by eye from the numbered tiles in data/soundings/tanur/tiles/,
with ambiguous glyphs re-read on enlarged crops of the chart.
Status codes:
  ok        clear reading
  unsure    legible but could be misread, or a lone fraction that may not be a sounding
  edge      cut by the window border; excluded from modelling
  drop      ambiguous on the second check; excluded
  not       detector picked up something that is not a sounding (text, palm, border, bank line)
  split     detector box merged two numbers; both are in ADDED
Rows starting with 'A' are numbers the detector missed. Their position is the
window pixel read off the tile image (accurate to roughly +/- 5 chart px).

Checks. A coverage sweep (every recorded reading blanked out on the window, to
expose numbers with no entry) found no further missed soundings, but showed
that the seven additions from tile 10 had been placed 20 px too low; their
positions were corrected. The second pass over the contact sheets in check/
changed no values. It changed one status: S0049 (1) to unsure, because the
lone 1/2 beside it (S0043) may be its fraction, making the sounding 1 1/2.
Numbers cut by the left and bottom window borders are 'edge' (detector boxes)
or omitted (unboxed partial glyphs), although most are legible on the chart
just outside the window.
"""
# detector id -> (value in fathoms or None, status)
READ = {
 # tile 00
 'S0000': (9,'ok'), 'S0001': (7,'ok'), 'S0002': (10,'ok'), 'S0003': (8,'ok'), 'S0004': (9,'ok'),
 'S0005': (8,'ok'), 'S0006': (None,'edge'), 'S0007': (9,'ok'), 'S0008': (11,'ok'), 'S0009': (10,'ok'),
 'S0010': (8,'ok'), 'S0011': (9,'ok'), 'S0012': (11,'ok'), 'S0013': (None,'edge'), 'S0014': (11,'ok'),
 'S0015': (8,'ok'), 'S0016': (9,'ok'), 'S0017': (8,'ok'), 'S0018': (11,'ok'), 'S0019': (10,'ok'),
 'S0020': (11,'ok'), 'S0021': (8,'ok'), 'S0022': (9,'ok'), 'S0023': (11,'ok'), 'S0024': (9,'ok'),
 'S0025': (9,'ok'), 'S0026': (11,'ok'), 'S0027': (8,'ok'), 'S0028': (10,'ok'),
 # tile 01
 'S0029': (None,'not'), 'S0030': (3.5,'ok'), 'S0031': (7,'ok'), 'S0032': (4,'ok'), 'S0033': (6,'ok'),
 'S0034': (None,'split'), 'S0035': (2,'ok'), 'S0036': (3.5,'ok'), 'S0037': (7,'ok'), 'S0038': (4,'ok'),
 'S0039': (7,'ok'), 'S0040': (2.5,'ok'), 'S0041': (7,'ok'), 'S0042': (3.5,'ok'), 'S0043': (0.5,'unsure'),
 'S0044': (6,'ok'), 'S0045': (None,'not'), 'S0046': (5.5,'ok'), 'S0047': (7,'ok'), 'S0048': (6,'ok'),
 'S0049': (1,'unsure'), 'S0050': (7,'ok'), 'S0051': (4.5,'ok'), 'S0052': (2,'ok'), 'S0053': (7,'ok'),
 'S0054': (6,'ok'), 'S0055': (3.5,'ok'), 'S0056': (4,'ok'), 'S0057': (8,'ok'), 'S0058': (6,'ok'),
 'S0059': (3,'ok'), 'S0060': (2,'ok'), 'S0061': (5,'ok'),
 # tile 03
 'S0062': (None,'not'),
 # tile 10
 'S0063': (None,'edge'), 'S0064': (11,'ok'), 'S0065': (10,'ok'), 'S0066': (8,'ok'), 'S0067': (10,'ok'),
 'S0068': (8,'ok'), 'S0069': (10,'ok'), 'S0070': (9,'ok'), 'S0071': (8,'ok'), 'S0072': (None,'edge'),
 'S0073': (11,'ok'), 'S0074': (9,'ok'), 'S0075': (10,'ok'), 'S0076': (13,'ok'), 'S0077': (9,'ok'),
 'S0078': (9,'ok'), 'S0079': (9,'ok'), 'S0080': (8,'ok'), 'S0081': (10,'ok'), 'S0082': (10,'ok'),
 'S0083': (9,'ok'), 'S0084': (None,'edge'), 'S0085': (10,'ok'), 'S0086': (9,'ok'), 'S0087': (10,'ok'),
 'S0088': (12,'ok'), 'S0089': (10,'ok'), 'S0090': (None,'edge'), 'S0091': (11,'ok'), 'S0092': (10,'ok'),
 'S0093': (10,'ok'), 'S0094': (11,'ok'), 'S0095': (12,'ok'),
 # tile 11
 'S0096': (3,'ok'), 'S0097': (4,'ok'), 'S0098': (8,'ok'), 'S0099': (6,'ok'), 'S0100': (6,'ok'),
 'S0101': (7,'ok'), 'S0102': (6,'ok'), 'S0103': (5,'ok'), 'S0104': (3,'ok'), 'S0105': (4,'ok'),
 'S0106': (4.75,'ok'), 'S0107': (6,'ok'), 'S0108': (7,'ok'), 'S0109': (7,'ok'), 'S0110': (7,'ok'),
 'S0111': (4,'ok'), 'S0112': (None,'split'), 'S0113': (4.5,'ok'), 'S0114': (2,'ok'), 'S0115': (6,'ok'),
 'S0116': (7,'ok'), 'S0117': (6,'ok'), 'S0118': (5,'ok'), 'S0119': (7,'ok'), 'S0120': (4,'ok'),
 'S0121': (7,'ok'), 'S0122': (3,'ok'), 'S0123': (5.5,'ok'), 'S0124': (6,'ok'), 'S0125': (5,'ok'),
 'S0126': (3.5,'ok'), 'S0127': (3,'ok'), 'S0128': (7,'ok'), 'S0129': (6,'ok'), 'S0130': (5.5,'ok'),
 'S0131': (4,'ok'), 'S0132': (8,'ok'), 'S0133': (7,'ok'), 'S0134': (8,'ok'), 'S0135': (6,'ok'),
 'S0136': (7,'ok'), 'S0137': (5,'ok'), 'S0138': (3,'ok'), 'S0139': (7,'ok'), 'S0140': (7,'ok'),
 'S0141': (5.25,'ok'), 'S0142': (4,'ok'), 'S0143': (6,'ok'), 'S0144': (3,'ok'), 'S0145': (8,'ok'),
 'S0146': (9,'ok'), 'S0147': (3.5,'ok'), 'S0148': (7,'ok'), 'S0149': (7,'ok'), 'S0150': (6,'ok'),
 'S0151': (4,'ok'), 'S0152': (7,'ok'), 'S0153': (7,'ok'), 'S0154': (6,'ok'),
 # tile 12
 'S0155': (2,'ok'), 'S0156': (None,'not'), 'S0157': (2,'ok'), 'S0158': (None,'not'), 'S0159': (2.5,'ok'),
 'S0160': (1.25,'ok'), 'S0161': (2.5,'ok'), 'S0162': (3,'ok'),
 # tile 20
 'S0163': (14,'ok'), 'S0164': (12,'ok'), 'S0165': (14,'ok'), 'S0166': (None,'not'), 'S0167': (13,'ok'),
 'S0168': (11,'ok'), 'S0169': (12,'ok'), 'S0170': (10,'ok'), 'S0171': (14,'ok'), 'S0172': (12,'ok'),
 'S0173': (11,'ok'), 'S0174': (13,'ok'), 'S0175': (12,'ok'), 'S0176': (11,'ok'), 'S0177': (13,'ok'),
 'S0178': (11,'ok'), 'S0179': (12,'ok'), 'S0180': (14,'ok'), 'S0181': (12,'ok'), 'S0182': (10,'ok'),
 'S0183': (14,'ok'), 'S0184': (12,'ok'), 'S0185': (14,'ok'), 'S0186': (11,'ok'), 'S0187': (13,'ok'),
 'S0188': (12,'ok'), 'S0189': (14,'ok'), 'S0190': (14,'ok'), 'S0191': (11,'ok'), 'S0192': (13,'ok'),
 'S0193': (12,'ok'), 'S0194': (14,'ok'), 'S0195': (14,'ok'), 'S0196': (None,'edge'), 'S0197': (14,'ok'),
 'S0198': (11,'ok'), 'S0199': (12,'ok'),
 # tile 21
 'S0200': (4.5,'ok'), 'S0201': (8,'ok'), 'S0202': (6,'ok'), 'S0203': (7,'ok'), 'S0204': (5,'ok'),
 'S0205': (6,'ok'), 'S0206': (7,'ok'), 'S0207': (8,'ok'), 'S0208': (5.5,'ok'), 'S0209': (9,'ok'),
 'S0210': (5.5,'ok'), 'S0211': (8,'ok'), 'S0212': (6,'ok'), 'S0213': (4.5,'ok'), 'S0214': (6,'ok'),
 'S0215': (8,'ok'), 'S0216': (5,'ok'), 'S0217': (9,'ok'), 'S0218': (6,'ok'), 'S0219': (7,'ok'),
 'S0220': (8,'ok'), 'S0221': (6,'ok'), 'S0222': (5,'ok'), 'S0223': (8,'ok'), 'S0224': (10,'ok'),
 'S0225': (7,'ok'), 'S0226': (6,'ok'), 'S0227': (8,'ok'), 'S0228': (5.5,'ok'), 'S0229': (5,'ok'),
 'S0230': (9,'ok'), 'S0231': (6,'ok'), 'S0232': (9,'ok'), 'S0233': (10,'ok'), 'S0234': (8,'ok'),
 'S0235': (6,'ok'), 'S0236': (8,'ok'), 'S0237': (6,'ok'), 'S0238': (10,'ok'), 'S0239': (7,'ok'),
 'S0240': (9,'ok'), 'S0241': (8,'ok'), 'S0242': (10,'ok'), 'S0243': (9,'ok'), 'S0244': (6,'ok'),
 'S0245': (11,'ok'), 'S0246': (10,'ok'), 'S0247': (8,'ok'), 'S0248': (9,'ok'), 'S0249': (9,'ok'),
 'S0250': (10,'ok'), 'S0251': (8,'ok'), 'S0252': (10,'ok'), 'S0253': (11,'ok'), 'S0254': (7,'ok'),
 'S0255': (9,'ok'), 'S0256': (10,'ok'),
 # tile 22
 'S0257': (1.25,'ok'), 'S0258': (3.75,'ok'), 'S0259': (3.5,'ok'), 'S0260': (2.5,'ok'), 'S0261': (4,'ok'),
 'S0262': (3,'ok'), 'S0263': (4,'ok'), 'S0264': (1.5,'ok'), 'S0265': (2,'ok'), 'S0266': (5,'ok'),
 'S0267': (3.5,'ok'), 'S0268': (4,'ok'), 'S0269': (2.5,'ok'), 'S0270': (2.75,'ok'), 'S0271': (2,'ok'),
 'S0272': (3,'ok'), 'S0273': (5,'ok'), 'S0274': (3,'ok'), 'S0275': (4,'ok'), 'S0276': (3.5,'ok'),
 'S0277': (4,'ok'), 'S0278': (4.5,'ok'),
 # tile 30
 'S0279': (15,'ok'), 'S0280': (None,'edge'), 'S0281': (11,'ok'), 'S0282': (12,'ok'), 'S0283': (12,'ok'),
 'S0284': (13,'ok'), 'S0285': (12,'ok'), 'S0286': (13,'ok'), 'S0287': (13,'ok'), 'S0288': (14,'ok'),
 'S0289': (12,'ok'), 'S0290': (13,'ok'), 'S0291': (14,'ok'), 'S0292': (15,'ok'), 'S0293': (13,'ok'),
 'S0294': (12,'ok'), 'S0295': (13,'ok'), 'S0296': (12,'ok'), 'S0297': (13,'ok'),
 # tile 31
 'S0298': (7,'ok'), 'S0299': (9,'ok'), 'S0300': (8,'ok'), 'S0301': (10,'ok'), 'S0302': (8,'ok'),
 'S0303': (6,'ok'), 'S0304': (10,'ok'), 'S0305': (10,'ok'), 'S0306': (6,'ok'), 'S0307': (11,'ok'),
 'S0308': (10,'ok'), 'S0309': (8,'ok'), 'S0310': (9,'ok'), 'S0311': (11,'ok'), 'S0312': (8,'ok'),
 'S0313': (10,'ok'), 'S0314': (10,'ok'), 'S0315': (11,'ok'), 'S0316': (9,'ok'), 'S0317': (11,'ok'),
 'S0318': (None,'split'), 'S0319': (12,'ok'), 'S0320': (8,'ok'), 'S0321': (11,'ok'), 'S0322': (10,'ok'),
 'S0323': (8,'ok'), 'S0324': (11,'ok'), 'S0325': (10,'ok'), 'S0326': (None,'not'),
 # tile 32
 'S0327': (None,'not'), 'S0328': (0.5,'unsure'), 'S0329': (2.5,'ok'), 'S0330': (2,'ok'), 'S0331': (3.25,'ok'),
 'S0332': (2.5,'ok'), 'S0333': (3.5,'ok'), 'S0334': (5.5,'ok'), 'S0335': (2.5,'ok'), 'S0336': (6,'ok'),
 'S0337': (2,'ok'), 'S0338': (4.25,'ok'), 'S0339': (2,'ok'), 'S0340': (5.75,'ok'), 'S0341': (2,'ok'),
 'S0342': (6,'ok'), 'S0343': (2,'ok'), 'S0344': (None,'not'), 'S0345': (6,'ok'), 'S0346': (3,'ok'),
 'S0347': (None,'not'),
}

# numbers the detector missed or merged: (window_x, window_y, fathoms, status, note)
ADDED = [
 # tile 00
 (185, 202, 10, 'ok', 'missed'), (402, 230, 7, 'ok', 'missed'),
 # tile 01
 (775, 172, 1, 'ok', 'split from S0034'), (750, 190, 2.5, 'ok', 'split from S0034'),
 (670, 262, 4.25, 'ok', 'missed'), (718, 322, 3.75, 'ok', 'missed'), (668, 375, 4.5, 'ok', 'missed'),
 # tile 10
 (60, 475, 12, 'ok', 'missed'), (217, 507, 10, 'ok', 'missed, on contour'), (175, 532, 10, 'ok', 'missed, on contour'),
 (190, 595, 10, 'ok', 'missed, on contour'), (77, 635, 13, 'ok', 'missed'), (150, 694, 12, 'ok', 'missed'),
 (280, 735, 10, 'ok', 'missed'),
 # tile 11
 (765, 515, 3.25, 'ok', 'split from S0112'), (803, 516, 3, 'ok', 'split from S0112'),
 (675, 428, 4.5, 'ok', 'missed'), (815, 433, 2, 'ok', 'missed'), (645, 518, 5.25, 'ok', 'missed, on bank line'),
 (432, 577, 8, 'ok', 'missed, on parallel'), (752, 630, 4.25, 'unsure', 'missed, fraction faint'),
 (713, 648, 4.5, 'ok', 'missed'), (530, 655, 7, 'ok', 'missed'), (527, 785, 7, 'ok', 'missed'),
 (657, 800, 7, 'ok', 'missed'),
 # tile 12
 (857, 675, 2.5, 'ok', 'missed'),
 # tile 20
 (357, 880, 10, 'ok', 'missed, on contour above "m"'), (100, 990, 14, 'ok', 'missed'),
 # tile 21
 (625, 965, 7, 'ok', 'missed'), (432, 1017, 10, 'ok', 'missed, on contour'), (662, 1017, 7, 'ok', 'missed'),
 (705, 1120, 7, 'ok', 'missed'), (781, 1167, 7, 'ok', 'missed'), (540, 1217, 10, 'ok', 'missed'),
 (622, 1267, 10, 'ok', 'missed'),
 # tile 22
 (875, 970, 4.5, 'ok', 'missed'), (935, 975, 2, 'ok', 'missed, on bank line'), (897, 1087, 3.5, 'ok', 'missed'),
 # tile 30
 (227, 1588, 14, 'unsure', 'missed, touching bottom border'),
 # tile 31
 (592, 1477, 10, 'ok', 'split from S0318'), (636, 1471, 10, 'ok', 'split from S0318'),
 (460, 1297, 10, 'ok', 'missed, on contour'), (510, 1287, 10, 'ok', 'missed'), (740, 1445, 9, 'ok', 'missed'),
 (730, 1475, 8, 'ok', 'missed'), (837, 1497, 7, 'ok', 'missed'), (817, 1557, 7, 'ok', 'missed'),
 # tile 32
 (954, 1295, 4.75, 'ok', 'missed'), (936, 1332, 5, 'ok', 'missed'), (930, 1356, 5.25, 'ok', 'missed'),
 (891, 1367, 5.5, 'ok', 'missed'), (931, 1401, 4.75, 'ok', 'missed'), (1075, 1466, 1.5, 'ok', 'missed'),
 (976, 1514, 5.25, 'ok', 'missed'), (1007, 1521, 4, 'ok', 'missed'), (1036, 1506, 3, 'ok', 'missed, on bank line'),
 (1029, 1536, 3.5, 'ok', 'missed'), (972, 1547, 5, 'ok', 'missed'), (950, 1576, 5.5, 'ok', 'missed'),
]

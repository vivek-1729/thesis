"""Hand transcription of soundings in the kollam window of BA 750.

Site: kollam (candidates for Nelkynda and Bakare: Kollam, Neendakara, Thangassery).
Sheet: Admiralty BA 750 (Selby, surveyed 1850-2, 1:146,000, soundings in fathoms),
scan malabar-750-1857.jpg, window chart px (4700, 8500)-(6400, 10100).

Values were read by eye from the numbered tiles in data/soundings/kollam/tiles/.
Status codes:
  ok        clear reading
  unsure    legible but could be misread, or a lone fraction that may not be a sounding
  edge      cut by the window border; excluded from modelling
  drop      ambiguous on the second check; excluded
  not       detector picked up something that is not a sounding (text, palm, rock, breaker, bank line)
  split     a detector box that merged two numbers; both are in ADDED
  later     a sounding the chart marks as added after the original survey (none found here)
Rows starting with 'A' are numbers the detector missed. Their position is the
window pixel I read off the tile image (accurate to roughly +/- 5 chart px).
Rows marked split replace a detector box that merged two or three numbers.

Notes on this part of the chart:
- No label dating soundings to a later year was found in the window, so nothing
  is marked 'later'. The only later-looking addition is the light at Tangacheri
  Point (window ~1230-1290, 1150-1230): a hand-coloured yellow wash and red dot,
  and rotated engraved text reading roughly "Lt. G.P. Fl. ev. 10 sec. 135 ft. vis 18 m".
  It is text, not a sounding; three fractional soundings sit inside the yellow wash
  and are read as unsure.
- The hand-drawn red, green and brown lines run down the offshore half. Numbers
  under them were read normally; the boxes that caught only the lines are 'not'.
- Dotted rings around a sounding (patches) are read as ordinary soundings.
  Small 'r', 's', 'm' written under a number are bottom notes and were ignored.
- Tangacheri reef and the inshore water off Quilon are dense with rock crosses,
  breaker marks and dotted rings; most of the hand additions come from there, and
  three glyphs hidden in rock dots are recorded as drop.
- The backwater behind Quilon (the arm of the "Aibika or Iviker River") carries
  eleven soundings of 0.75 to 1.75 fathoms; the rest of the lake has none.

Second pass (contact sheets in data/soundings/kollam/check/): seven values changed
(S0296 8 -> drop, S0305 3.25 -> 3.75, S0306 1.5 -> 1.25, S0327 1.5 -> 1.25,
added 2.5 -> 2.25 at (1164, 1175), added 4.5 -> 4.25 at (1323, 1319), added 3 -> drop
at (1355, 1297)), and two statuses changed without a value change (S0126 unsure -> ok,
added 2.75 at (1395, 1237) ok -> unsure).
"""
# detector id -> (value in fathoms or None, status)
READ = {
 # tile 00
 'S0000': (None,'edge'), 'S0001': (None,'not'), 'S0002': (12,'ok'), 'S0003': (10,'ok'), 'S0004': (8,'ok'),
 'S0005': (10,'ok'), 'S0006': (11,'ok'), 'S0007': (13,'ok'), 'S0008': (9,'ok'), 'S0009': (14,'ok'),
 'S0010': (12,'ok'), 'S0011': (10,'ok'), 'S0012': (8,'ok'), 'S0013': (14,'ok'), 'S0014': (11,'ok'),
 'S0015': (13,'ok'), 'S0016': (9,'ok'), 'S0017': (None,'edge'), 'S0018': (13,'ok'), 'S0019': (12,'ok'),
 'S0020': (10,'ok'), 'S0021': (9,'ok'), 'S0022': (None,'edge'), 'S0023': (11,'ok'), 'S0024': (12,'ok'),
 'S0025': (14,'ok'), 'S0026': (9,'ok'), 'S0027': (8,'ok'), 'S0028': (10,'ok'), 'S0029': (13,'ok'),
 'S0030': (11,'ok'), 'S0031': (11,'ok'), 'S0032': (10,'ok'), 'S0033': (10,'ok'), 'S0034': (15,'ok'),
 'S0035': (11,'ok'), 'S0036': (9,'ok'), 'S0037': (13,'ok'), 'S0038': (10,'ok'), 'S0039': (13,'ok'),
 'S0040': (11,'ok'), 'S0041': (14,'ok'),
 # tile 01
 'S0042': (5,'ok'), 'S0043': (5,'ok'), 'S0044': (None,'not'), 'S0045': (3.5,'ok'), 'S0046': (3,'ok'),
 'S0047': (4.5,'ok'), 'S0048': (7,'ok'), 'S0049': (6,'ok'), 'S0050': (3.5,'ok'), 'S0051': (5.5,'ok'),
 'S0052': (5,'ok'), 'S0053': (7,'ok'), 'S0054': (3,'ok'), 'S0055': (6,'ok'), 'S0056': (6,'ok'),
 'S0057': (6,'ok'), 'S0058': (None,'not'), 'S0059': (2.5,'ok'), 'S0060': (6,'ok'), 'S0061': (7,'ok'),
 'S0062': (None,'not'), 'S0063': (6,'ok'), 'S0064': (8,'ok'), 'S0065': (6,'ok'), 'S0066': (5,'ok'),
 'S0067': (7,'ok'), 'S0068': (6,'ok'), 'S0069': (4,'ok'), 'S0070': (None,'not'), 'S0071': (3,'ok'),
 'S0072': (5,'ok'), 'S0073': (7,'ok'), 'S0074': (8,'ok'), 'S0075': (3.5,'ok'), 'S0076': (5,'ok'),
 'S0077': (5,'ok'), 'S0078': (7,'ok'), 'S0079': (6,'ok'), 'S0080': (4,'ok'), 'S0081': (7,'ok'),
 'S0082': (5,'ok'), 'S0083': (8,'ok'), 'S0084': (8,'ok'), 'S0085': (9,'ok'), 'S0086': (6,'ok'),
 'S0087': (4,'ok'), 'S0088': (5,'ok'), 'S0089': (6,'ok'), 'S0090': (9,'ok'), 'S0091': (7,'ok'),
 'S0092': (6,'ok'), 'S0093': (5.5,'ok'),
 # tiles 02, 03 (land and backwater)
 'S0094': (None,'not'), 'S0095': (None,'not'),
 # tile 10
 'S0096': (10,'ok'), 'S0097': (16,'ok'), 'S0098': (14,'ok'), 'S0099': (13,'ok'), 'S0100': (13,'ok'),
 'S0101': (11,'ok'), 'S0102': (14,'ok'), 'S0103': (10,'ok'), 'S0104': (12,'ok'), 'S0105': (16,'ok'),
 'S0106': (13,'ok'), 'S0107': (10,'ok'), 'S0108': (11,'ok'), 'S0109': (14,'ok'), 'S0110': (10,'ok'),
 'S0111': (16,'ok'), 'S0112': (13,'ok'), 'S0113': (10,'ok'), 'S0114': (13,'ok'), 'S0115': (15,'ok'),
 'S0116': (14,'ok'), 'S0117': (16,'ok'), 'S0118': (13,'ok'), 'S0119': (None,'not'), 'S0120': (17,'ok'),
 'S0121': (11,'ok'), 'S0122': (14,'ok'), 'S0123': (None,'not'), 'S0124': (17,'ok'), 'S0125': (12,'ok'),
 'S0126': (19,'ok'), 'S0127': (14,'ok'), 'S0128': (17,'ok'),
 # tile 11
 'S0129': (8,'ok'), 'S0130': (4,'ok'), 'S0131': (7,'ok'), 'S0132': (5,'ok'), 'S0133': (6,'ok'),
 'S0134': (3.5,'ok'), 'S0135': (6,'ok'), 'S0136': (9,'ok'), 'S0137': (3.5,'ok'), 'S0138': (6,'ok'),
 'S0139': (7,'ok'), 'S0140': (3.5,'ok'), 'S0141': (4.5,'ok'), 'S0142': (7,'ok'), 'S0143': (7,'ok'),
 'S0144': (4,'ok'), 'S0145': (9,'ok'), 'S0146': (8,'ok'), 'S0147': (8,'ok'), 'S0148': (9,'ok'),
 'S0149': (None,'not'), 'S0150': (6,'ok'), 'S0151': (8,'ok'), 'S0152': (9,'ok'), 'S0153': (8,'ok'),
 'S0154': (8,'ok'), 'S0155': (4.5,'ok'), 'S0156': (7,'ok'), 'S0157': (5.5,'ok'), 'S0158': (4,'ok'),
 'S0159': (8,'ok'), 'S0160': (10,'ok'), 'S0161': (6,'ok'), 'S0162': (8,'ok'), 'S0163': (6,'ok'),
 'S0164': (9,'ok'), 'S0165': (4,'ok'), 'S0166': (3.5,'ok'), 'S0167': (3.25,'ok'), 'S0168': (7,'ok'),
 'S0169': (10,'ok'), 'S0170': (9,'ok'), 'S0171': (4.5,'ok'), 'S0172': (9,'ok'), 'S0173': (4.5,'ok'),
 'S0174': (7,'ok'), 'S0175': (8,'ok'), 'S0176': (8,'ok'), 'S0177': (10,'ok'), 'S0178': (4.5,'ok'),
 'S0179': (11,'ok'), 'S0180': (7,'ok'), 'S0181': (6,'ok'), 'S0182': (10,'ok'), 'S0183': (4.5,'ok'),
 # tile 12 (Neendakara entrance)
 'S0184': (None,'not'), 'S0185': (3.5,'ok'), 'S0186': (3,'ok'), 'S0187': (1.5,'ok'), 'S0188': (3.5,'ok'),
 'S0189': (None,'not'), 'S0190': (None,'not'), 'S0191': (3,'ok'), 'S0192': (3.25,'ok'), 'S0193': (3,'ok'),
 'S0194': (1,'ok'), 'S0195': (3,'ok'), 'S0196': (3.5,'ok'), 'S0197': (None,'not'), 'S0198': (4,'ok'),
 'S0199': (1.25,'ok'), 'S0200': (3.5,'ok'),
 # tile 13 (river name)
 'S0201': (None,'not'), 'S0202': (None,'not'),
 # tile 20
 'S0203': (13,'ok'), 'S0204': (15,'ok'), 'S0205': (18,'ok'), 'S0206': (20,'ok'), 'S0207': (14,'ok'),
 'S0208': (15,'ok'), 'S0209': (18,'ok'), 'S0210': (15,'ok'), 'S0211': (14,'ok'), 'S0212': (19,'ok'),
 'S0213': (20,'ok'), 'S0214': (15,'ok'), 'S0215': (17,'ok'), 'S0216': (20,'ok'), 'S0217': (20,'ok'),
 'S0218': (18,'ok'), 'S0219': (16,'ok'), 'S0220': (21,'ok'), 'S0221': (18,'ok'), 'S0222': (21,'ok'),
 # tile 21
 'S0223': (8,'ok'), 'S0224': (6,'ok'), 'S0225': (10,'ok'), 'S0226': (4,'ok'), 'S0227': (6.5,'ok'),
 'S0228': (7,'ok'), 'S0229': (11,'ok'), 'S0230': (8,'ok'), 'S0231': (9,'ok'), 'S0232': (6.5,'ok'),
 'S0233': (6.5,'ok'), 'S0234': (10,'ok'), 'S0235': (11,'ok'), 'S0236': (8,'ok'), 'S0237': (7,'ok'),
 'S0238': (6.5,'ok'), 'S0239': (11,'ok'), 'S0240': (None,'not'), 'S0241': (10,'ok'), 'S0242': (8,'ok'),
 'S0243': (12,'ok'), 'S0244': (9,'ok'), 'S0245': (10,'ok'), 'S0246': (6.5,'ok'), 'S0247': (11,'ok'),
 'S0248': (9,'ok'), 'S0249': (4,'ok'), 'S0250': (None,'not'), 'S0251': (13,'ok'), 'S0252': (9,'ok'),
 'S0253': (11,'ok'), 'S0254': (6,'ok'), 'S0255': (9,'ok'), 'S0256': (10,'ok'), 'S0257': (5.5,'ok'),
 'S0258': (11,'ok'), 'S0259': (10,'ok'), 'S0260': (6.5,'ok'), 'S0261': (14,'ok'), 'S0262': (11,'ok'),
 'S0263': (13,'ok'), 'S0264': (8,'ok'), 'S0265': (12,'ok'), 'S0266': (12,'ok'), 'S0267': (18,'ok'),
 'S0268': (10,'ok'), 'S0269': (12,'ok'), 'S0270': (12,'ok'), 'S0271': (11,'ok'), 'S0272': (13,'ok'),
 # tile 22 (Thangassery reef and point)
 'S0273': (3.5,'ok'), 'S0274': (None,'not'), 'S0275': (None,'not'), 'S0276': (None,'split'),
 'S0277': (None,'not'), 'S0278': (1.5,'ok'), 'S0279': (3.5,'ok'), 'S0280': (3,'ok'), 'S0281': (2.5,'ok'),
 'S0282': (2.5,'ok'), 'S0283': (None,'split'), 'S0284': (2.5,'ok'), 'S0285': (None,'not'),
 'S0286': (5.25,'ok'), 'S0287': (6,'ok'), 'S0288': (None,'not'), 'S0289': (4,'ok'), 'S0290': (4,'ok'),
 'S0291': (4,'ok'), 'S0292': (None,'not'), 'S0293': (4,'ok'), 'S0294': (4.5,'ok'), 'S0295': (6,'ok'),
 'S0296': (None,'drop'), 'S0297': (4,'ok'), 'S0298': (None,'split'), 'S0299': (7,'ok'), 'S0300': (2,'unsure'),
 'S0301': (None,'not'), 'S0302': (8,'ok'), 'S0303': (7,'unsure'), 'S0304': (2.25,'ok'),
 'S0305': (3.75,'ok'), 'S0306': (1.25,'unsure'), 'S0307': (6.5,'ok'), 'S0308': (4.5,'ok'),
 'S0309': (3,'ok'), 'S0310': (4.25,'unsure'),
 # tile 23 (Quilon and the Ashtamudi arm behind it)
 'S0311': (1.75,'ok'), 'S0312': (1.5,'ok'), 'S0313': (1.5,'ok'), 'S0314': (1.5,'ok'), 'S0315': (1,'ok'),
 'S0316': (1.75,'ok'), 'S0317': (1.5,'unsure'), 'S0318': (1,'ok'), 'S0319': (None,'not'), 'S0320': (1.5,'ok'),
 'S0321': (None,'not'), 'S0322': (0.75,'unsure'), 'S0323': (None,'not'), 'S0324': (None,'not'),
 'S0325': (None,'not'), 'S0326': (None,'not'), 'S0327': (1.25,'unsure'), 'S0328': (2.25,'unsure'),
 # tiles 30, 31
 'S0329': (21,'ok'), 'S0330': (19,'ok'), 'S0331': (17,'ok'), 'S0332': (12,'ok'), 'S0333': (13,'ok'),
 'S0334': (20,'ok'), 'S0335': (20,'ok'), 'S0336': (13,'ok'), 'S0337': (21,'ok'), 'S0338': (21,'ok'),
 'S0339': (23,'ok'),
 # tile 32
 'S0340': (11,'ok'), 'S0341': (4,'ok'), 'S0342': (3.5,'ok'), 'S0343': (8,'ok'), 'S0344': (12,'ok'),
 'S0345': (11,'ok'), 'S0346': (10,'ok'), 'S0347': (5.5,'ok'), 'S0348': (9,'ok'), 'S0349': (12,'ok'),
 'S0350': (6.5,'ok'), 'S0351': (8,'ok'), 'S0352': (11,'ok'), 'S0353': (6,'ok'), 'S0354': (10,'ok'),
 'S0355': (12,'ok'), 'S0356': (8,'ok'), 'S0357': (11,'ok'), 'S0358': (8,'ok'), 'S0359': (13,'ok'),
 'S0360': (11,'ok'), 'S0361': (12,'ok'), 'S0362': (9,'ok'), 'S0363': (9,'ok'), 'S0364': (10,'ok'),
 'S0365': (13,'ok'), 'S0366': (12,'ok'), 'S0367': (10,'ok'), 'S0368': (15,'ok'), 'S0369': (12,'ok'),
 'S0370': (12,'ok'), 'S0371': (13,'ok'), 'S0372': (11,'ok'), 'S0373': (15,'ok'), 'S0374': (11,'ok'),
 'S0375': (17,'ok'), 'S0376': (12,'ok'), 'S0377': (13,'ok'), 'S0378': (11,'ok'), 'S0379': (15,'ok'),
 'S0380': (15,'ok'), 'S0381': (12,'ok'),
 # tile 33 (inshore off Quilon)
 'S0382': (3,'ok'), 'S0383': (3.75,'ok'), 'S0384': (None,'split'), 'S0385': (None,'split'),
 'S0386': (4.75,'ok'), 'S0387': (4.25,'unsure'), 'S0388': (4,'ok'), 'S0389': (5.25,'unsure'),
 'S0390': (6,'ok'), 'S0391': (5.5,'ok'), 'S0392': (3.5,'ok'), 'S0393': (None,'not'), 'S0394': (6.5,'ok'),
 'S0395': (4.75,'ok'), 'S0396': (7,'ok'), 'S0397': (8,'ok'), 'S0398': (8,'ok'), 'S0399': (7,'ok'),
 'S0400': (7,'ok'), 'S0401': (4.5,'ok'), 'S0402': (None,'not'), 'S0403': (9,'ok'), 'S0404': (8,'ok'),
 'S0405': (5.5,'ok'), 'S0406': (9,'ok'), 'S0407': (7,'ok'), 'S0408': (3,'ok'), 'S0409': (8,'ok'),
 'S0410': (7,'ok'), 'S0411': (9,'ok'), 'S0412': (8,'ok'), 'S0413': (7,'ok'), 'S0414': (9,'ok'),
 'S0415': (10,'ok'), 'S0416': (10,'ok'), 'S0417': (4,'ok'), 'S0418': (8,'ok'), 'S0419': (4,'ok'),
 'S0420': (7,'ok'), 'S0421': (9,'ok'), 'S0422': (5,'ok'), 'S0423': (9,'ok'), 'S0424': (None,'split'),
 'S0425': (9,'ok'), 'S0426': (5,'ok'), 'S0427': (None,'edge'), 'S0428': (None,'edge'),
}

ADDED = [
 # tile 01
 (592, 120, 5, 'ok', 'missed, in dotted circle'), (497, 212, 7, 'ok', 'missed, on graticule line'),
 (775, 200, 2.5, 'ok', 'missed, on graticule line'), (522, 260, 7, 'ok', 'missed'),
 (540, 405, 7, 'ok', 'missed'), (735, 415, 5, 'ok', 'missed'), (802, 410, 3, 'ok', 'missed'),
 # tile 10
 (360, 640, 10, 'ok', 'missed, on red line'),
 # tile 11
 (490, 485, 7, 'ok', 'missed'), (787, 470, 5, 'ok', 'missed'), (845, 435, 2, 'ok', 'missed'),
 (640, 547, 7, 'ok', 'missed'), (760, 542, 4.25, 'ok', 'missed'), (835, 542, 3.25, 'ok', 'missed'),
 (705, 577, 6, 'ok', 'missed'), (745, 605, 5, 'ok', 'missed'), (647, 637, 7, 'ok', 'missed'),
 (657, 692, 5, 'ok', 'missed, in dotted circle'), (679, 755, 7, 'ok', 'missed'),
 (779, 787, 5, 'ok', 'missed'), (696, 825, 7, 'ok', 'missed'),
 # tile 12
 (867, 497, 2, 'ok', 'missed'), (865, 532, 3, 'ok', 'missed'), (860, 580, 3.5, 'ok', 'missed'),
 (897, 610, 2.5, 'ok', 'missed'), (895, 707, 2, 'ok', 'missed'),
 # tile 20
 (45, 875, 19, 'ok', 'missed, beside brown line'), (85, 987, 20, 'ok', 'missed, beside brown line'),
 # tile 21
 (750, 980, 7, 'ok', 'missed'), (742, 1030, 7, 'ok', 'missed'), (819, 965, 4, 'ok', 'missed'),
 (802, 990, 4.5, 'ok', 'missed'), (837, 947, 3.25, 'ok', 'missed'), (815, 1065, 5, 'ok', 'missed'),
 (555, 1210, 15, 'ok', 'missed'),
 (787, 942, None, 'drop', 'lone 1/2 beside "Within", integer hidden by the text'),
 # tile 22
 (897, 900, 3.25, 'ok', 'split from S0276'), (856, 921, 3.25, 'ok', 'split from S0276'),
 (882, 917, 3, 'ok', 'split from S0276'),
 (959, 1059, 2, 'ok', 'split from S0283'), (940, 1070, 3, 'ok', 'split from S0283'),
 (924, 1085, 4, 'ok', 'split from S0283'),
 (1088, 1163, 2, 'ok', 'split from S0298'), (1121, 1174, 2.5, 'ok', 'split from S0298'),
 (905, 940, 2, 'ok', 'missed, above S0278'), (966, 1106, 2, 'ok', 'missed, beside rock'),
 (864, 1130, 5.5, 'ok', 'missed'), (902, 1134, 5, 'ok', 'missed'), (954, 1132, 5, 'ok', 'missed'),
 (987, 1189, 5.5, 'ok', 'missed, above "Breakers"'), (1050, 1192, 2.5, 'unsure', 'missed, in dotted ring'),
 (1032, 1213, 4.5, 'ok', 'missed'), (965, 1231, 7, 'ok', 'missed'), (971, 1265, 8, 'ok', 'missed'),
 (1077, 1210, 2, 'ok', 'missed, beside rock'), (1083, 1230, 2, 'ok', 'missed, in dotted ring'),
 (1139, 1198, 1.5, 'ok', 'missed'), (1164, 1175, 2.25, 'unsure', 'missed; value corrected on check'),
 (1194, 1176, 1.5, 'ok', 'missed'), (1197, 1227, 2.75, 'ok', 'missed'), (1182, 1256, 3.75, 'ok', 'missed'),
 (1233, 1253, 1.5, 'unsure', 'missed, inside yellow wash'), (1256, 1263, 2.75, 'ok', 'missed'),
 (1150, 1252, None, 'drop', 'illegible glyph below S0305'),
 # tile 23
 (1410, 1097, 1, 'ok', 'missed, backwater'),
 (1292, 1222, 1.5, 'unsure', 'missed, below S0327'), (1350, 1216, 2.25, 'ok', 'missed'),
 (1326, 1230, 2.25, 'unsure', 'missed, dotted'), (1366, 1236, 3, 'ok', 'missed'), (1395, 1237, 2.75, 'unsure', 'missed, fraction 3/4 or 1/4'),
 (1300, 1244, 3, 'ok', 'missed'), (1326, 1250, 4, 'ok', 'missed'), (1355, 1256, 1.75, 'unsure', 'missed'),
 (1382, 1262, 3.75, 'ok', 'missed'), (1427, 1255, 3.75, 'ok', 'missed'), (1327, 1267, 1.25, 'unsure', 'missed'),
 (1392, 1280, 4, 'ok', 'missed'), (1432, 1281, 3.75, 'ok', 'missed'),
 # tile 32
 (962, 1305, 10, 'ok', 'missed'), (1106, 1283, 2.5, 'unsure', 'missed, in dotted ring'),
 (1125, 1298, 3, 'ok', 'missed'), (1104, 1317, 7, 'ok', 'missed'), (1256, 1291, 3.75, 'ok', 'missed'),
 (1243, 1316, 5.5, 'ok', 'missed'), (1282, 1381, 7, 'ok', 'missed'), (1122, 1389, 10, 'ok', 'missed, on red line'),
 (1182, 1470, 10, 'ok', 'missed'),
 # tile 33
 (1296, 1303, 4, 'ok', 'split from S0385 (4 over r)'), (1298, 1332, 4.5, 'ok', 'split from S0385'),
 (1504, 1315, 3.25, 'ok', 'split from S0384'), (1480, 1329, 4, 'ok', 'split from S0384'),
 (1355, 1562, 10, 'ok', 'split from S0424'), (1325, 1588, 10, 'ok', 'split from S0424'),
 (1323, 1319, 4.25, 'unsure', 'missed; value corrected on check'), (1355, 1297, None, 'drop', 'faint 3? among rock dots; not confirmed on check'),
 (1393, 1315, 4.5, 'ok', 'missed, below anchor'), (1357, 1353, None, 'drop', 'glyph hidden in rock dots below S0387'),
 (1373, 1375, None, 'drop', 'glyph hidden in rock dots'), (1403, 1387, 6, 'ok', 'missed'),
 (1419, 1401, 4.75, 'unsure', 'missed, in dotted ring'), (1447, 1391, 5.25, 'ok', 'missed'),
 (1437, 1423, 6.5, 'ok', 'missed'), (1464, 1361, 5, 'ok', 'missed'), (1567, 1394, 4, 'ok', 'missed'),
 (1472, 1415, 5.25, 'ok', 'missed'), (1512, 1420, 5.25, 'ok', 'missed'), (1545, 1415, 4.75, 'ok', 'missed'),
 (1486, 1439, 4.75, 'unsure', 'missed, in dotted ring'), (1534, 1442, 5.75, 'ok', 'missed'),
 (1631, 1450, 2, 'ok', 'missed'), (1425, 1452, 7, 'ok', 'missed'), (1628, 1507, 5, 'ok', 'missed'),
 (1607, 1532, 6, 'ok', 'missed'), (1535, 1538, 7, 'ok', 'missed'),
]

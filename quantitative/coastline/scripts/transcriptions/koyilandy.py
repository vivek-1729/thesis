"""Hand transcription of soundings in the koyilandy window of BA 64.

Site: koyilandy (candidate for Tyndis: Koyilandy, i.e. Panthalayani Kollam, marked
"KOLLAM" and "Kollam Bazaar" beside "Quilandi"). Sheet: Admiralty chart 64,
Sacrifice Rock to Beipur (survey 1887, 1:48,380, soundings in fathoms reduced to
the lowest low water spring tides). Window: 2600 x 2600 chart pixels (see
sounding_sites.py).
The window holds Kadalur (Cotta) Point with its reef and rocks in the north-west, the
long dotted shoal of "very soft mud" running along the shore, an anchorage mark at
window ~(1497, 1327), a rocky patch (crosses) at ~(2230, 2300) and land with hills
and palms over the whole north-east half. About 60 per cent of the window is land.

Values were read by eye from the numbered tiles in data/soundings/koyilandy/tiles/,
with doubtful glyphs re-read on enlarged crops of the chart. Lone fractions (1/4,
1/2, 3/4) are frequent on the inshore shoal; where the glyph is clear and sits in a
field of soundings it is marked ok. Detector boxes that caught only the numerator or
the bottom-quality letter of a sounding carry the value on one box and 'not' on the
rest (noted per tile). S0034 reads as a printed "1/6", which is not a sounding
fraction; it is dropped. S0402 is cut by the bottom border.

Second pass: every reading was re-inspected on the contact sheets in check/; no
value or position needed changing (0 changes). One hand addition made from the
margin of tile 21 duplicated detector box S0228 and was removed before the check.

Status codes:
  ok        clear reading
  unsure    legible but could be misread, or a lone fraction that may not be a sounding
  edge      cut by the window border; excluded from modelling
  drop      ambiguous on the second check; excluded
  not       detector picked up something that is not a sounding (text, palm, hill, rock, m)
Rows starting with 'A' are numbers the detector missed. Their position is the
window pixel read off the tile image (accurate to roughly +/- 5 chart px).
"""
# detector id -> (value in fathoms or None, status)
READ = {
 # tile 00
 'S0000': (None,'not'), 'S0001': (None,'not'), 'S0002': (None,'not'), 'S0003': (None,'not'), 'S0004': (None,'not'),
 'S0005': (None,'not'), 'S0006': (None,'not'), 'S0007': (None,'not'), 'S0008': (0.5,'ok'), 'S0009': (0.5,'ok'),
 'S0010': (0.25,'ok'), 'S0011': (0.25,'ok'), 'S0012': (0.5,'ok'), 'S0013': (0.5,'ok'), 'S0014': (None,'not'),
 'S0015': (None,'not'), 'S0016': (0.75,'ok'), 'S0017': (0.75,'ok'), 'S0018': (None,'edge'), 'S0019': (1,'ok'),
 'S0020': (0.75,'ok'), 'S0021': (1.25,'ok'), 'S0022': (1.25,'ok'),
 # tile 01
 'S0023': (None,'not'), 'S0024': (None,'not'), 'S0025': (None,'not'), 'S0026': (None,'not'), 'S0027': (None,'not'),
 'S0028': (None,'not'), 'S0029': (0.5,'ok'), 'S0030': (None,'not'), 'S0031': (0.75,'ok'), 'S0032': (0.5,'ok'),
 'S0033': (0.75,'ok'), 'S0034': (None,'drop'), 'S0035': (0.75,'ok'), 'S0036': (0.75,'ok'), 'S0037': (None,'not'),
 'S0038': (1,'ok'), 'S0039': (1.25,'ok'), 'S0040': (0.75,'ok'),
 # tiles 02-05: land (hills, palms, road, "Urangab 200", Tank)
 'S0041': (None,'not'), 'S0042': (None,'not'), 'S0043': (None,'not'), 'S0044': (None,'not'), 'S0045': (None,'not'),
 'S0046': (None,'not'), 'S0047': (None,'not'), 'S0048': (None,'not'), 'S0049': (None,'not'), 'S0050': (None,'not'),
 'S0051': (None,'not'), 'S0052': (None,'not'), 'S0053': (None,'not'), 'S0054': (None,'not'), 'S0055': (None,'not'),
 'S0056': (None,'not'), 'S0057': (None,'not'), 'S0058': (None,'not'), 'S0059': (None,'not'), 'S0060': (None,'not'),
 'S0061': (None,'not'), 'S0062': (None,'not'),
 # tile 10
 'S0063': (1.25,'ok'), 'S0064': (1.75,'ok'), 'S0065': (1.25,'ok'), 'S0066': (1.25,'ok'), 'S0067': (None,'not'),
 'S0068': (1.75,'ok'), 'S0069': (1.25,'ok'), 'S0070': (1.25,'ok'), 'S0071': (1.25,'ok'), 'S0072': (2.25,'ok'),
 'S0073': (2,'ok'), 'S0074': (None,'not'), 'S0075': (1.25,'ok'), 'S0076': (None,'not'), 'S0077': (None,'not'),
 'S0078': (1.5,'ok'), 'S0079': (2.25,'ok'), 'S0080': (2,'ok'), 'S0081': (2.5,'ok'), 'S0082': (2.25,'ok'),
 'S0083': (2.5,'ok'),
 # tile 11
 'S0084': (1.5,'ok'), 'S0085': (1,'ok'), 'S0086': (1.25,'ok'), 'S0087': (0.75,'ok'), 'S0088': (None,'not'),
 'S0089': (1.75,'ok'), 'S0090': (1.5,'ok'), 'S0091': (1.25,'ok'), 'S0092': (1.5,'ok'), 'S0093': (2,'ok'),
 'S0094': (1.75,'ok'), 'S0095': (2.25,'ok'), 'S0096': (1.75,'ok'),
 # tile 12
 'S0097': (None,'not'), 'S0098': (0.75,'ok'), 'S0099': (None,'not'), 'S0100': (None,'not'), 'S0101': (0.75,'ok'),
 'S0102': (1,'ok'), 'S0103': (0.25,'ok'), 'S0104': (0.75,'ok'), 'S0105': (1.25,'ok'), 'S0106': (0.75,'ok'),
 'S0107': (1.75,'ok'), 'S0108': (1.25,'ok'), 'S0109': (1.5,'ok'),
 # tiles 13-16: land (Kollam Bazaar, palms, hills, "Kolat-kuno 175", road)
 'S0110': (None,'not'), 'S0111': (None,'not'), 'S0112': (None,'not'), 'S0113': (None,'not'), 'S0114': (None,'not'),
 'S0115': (None,'not'), 'S0116': (None,'not'), 'S0117': (None,'not'), 'S0118': (None,'not'), 'S0119': (None,'not'),
 'S0120': (None,'not'), 'S0121': (None,'not'), 'S0122': (None,'not'), 'S0123': (None,'not'), 'S0124': (None,'not'),
 'S0125': (None,'not'), 'S0126': (None,'not'), 'S0127': (None,'not'), 'S0128': (None,'not'), 'S0129': (None,'not'),
 'S0130': (None,'not'), 'S0131': (None,'not'), 'S0132': (None,'not'), 'S0133': (None,'not'), 'S0134': (None,'not'),
 'S0135': (None,'not'), 'S0136': (None,'not'), 'S0137': (None,'not'), 'S0138': (None,'not'), 'S0139': (None,'not'),
 'S0140': (None,'not'), 'S0141': (None,'not'), 'S0142': (None,'not'), 'S0143': (None,'not'), 'S0144': (None,'not'),

 # tile 20
 'S0145': (2.75,'ok'), 'S0146': (2.25,'ok'), 'S0147': (3,'ok'), 'S0148': (3,'ok'), 'S0149': (3.25,'ok'),
 'S0150': (3.25,'ok'), 'S0151': (3.75,'ok'), 'S0152': (3.25,'ok'), 'S0153': (4,'ok'), 'S0154': (3.75,'ok'),
 'S0155': (3.75,'ok'), 'S0156': (4,'ok'),
 # tile 21 (S0160 + S0161 are the two halves of one 2 3/4; S0166 is the r under a missed 3)
 'S0157': (2.25,'ok'), 'S0158': (2.25,'ok'), 'S0159': (2.25,'ok'), 'S0160': (2.75,'ok'), 'S0161': (None,'not'),
 'S0162': (2.25,'ok'), 'S0163': (2.75,'ok'), 'S0164': (2.75,'ok'), 'S0165': (2.5,'ok'), 'S0166': (None,'not'),
 'S0167': (None,'not'), 'S0168': (2.75,'ok'), 'S0169': (3.25,'ok'), 'S0170': (3.25,'ok'),
 # tile 22 (S0171, S0173, S0174 are pieces of one 1 3/4)
 'S0171': (None,'not'), 'S0172': (1.75,'ok'), 'S0173': (1.75,'ok'), 'S0174': (None,'not'), 'S0175': (1.25,'unsure'),
 'S0176': (1.75,'ok'), 'S0177': (1.75,'ok'), 'S0178': (2.25,'ok'), 'S0179': (1.75,'ok'), 'S0180': (2.25,'ok'),
 'S0181': (2.25,'ok'), 'S0182': (None,'not'),
 # tile 23
 'S0183': (1,'ok'), 'S0184': (1,'ok'), 'S0185': (1.25,'ok'), 'S0186': (1.25,'ok'), 'S0187': (1.5,'ok'),
 'S0188': (1.25,'ok'), 'S0189': (None,'not'), 'S0190': (1.25,'ok'),
 # tiles 24-25: land (palms, huts, road, "Quilandi")
 'S0191': (None,'not'), 'S0192': (None,'not'), 'S0193': (None,'not'), 'S0194': (None,'not'), 'S0195': (None,'not'),
 'S0196': (None,'not'), 'S0197': (None,'not'), 'S0198': (None,'not'), 'S0199': (None,'not'), 'S0200': (None,'not'),
 'S0201': (None,'not'), 'S0202': (None,'not'), 'S0203': (None,'not'), 'S0204': (None,'not'), 'S0205': (None,'not'),
 'S0206': (None,'not'), 'S0207': (None,'not'), 'S0208': (None,'not'), 'S0209': (None,'not'), 'S0210': (None,'not'),
 'S0211': (None,'not'), 'S0212': (None,'not'), 'S0213': (None,'not'), 'S0214': (None,'not'), 'S0215': (None,'not'),

 # tile 30
 'S0216': (None,'not'), 'S0217': (4.25,'ok'), 'S0218': (3.5,'ok'), 'S0219': (4,'ok'), 'S0220': (4.25,'ok'),
 'S0221': (4.25,'ok'), 'S0222': (4.75,'ok'), 'S0223': (4.25,'ok'), 'S0224': (4.5,'ok'), 'S0225': (5,'ok'),
 'S0226': (4.75,'ok'), 'S0227': (4.75,'ok'),
 # tile 31
 'S0228': (2.75,'ok'), 'S0229': (3.75,'ok'), 'S0230': (3,'ok'), 'S0231': (3.25,'ok'), 'S0232': (4,'ok'),
 'S0233': (3.25,'unsure'), 'S0234': (3.75,'ok'), 'S0235': (None,'not'), 'S0236': (3.75,'ok'), 'S0237': (4,'ok'),
 'S0238': (3.5,'ok'),
 # tile 32
 'S0239': (2.25,'ok'), 'S0240': (2.75,'ok'), 'S0241': (2.25,'ok'), 'S0242': (2.75,'ok'), 'S0243': (2.75,'ok'),
 'S0244': (2.75,'ok'),
 # tile 33 (anchorage mark at window ~(1497, 1327))
 'S0245': (1.5,'ok'), 'S0246': (1.75,'ok'), 'S0247': (1.25,'ok'), 'S0248': (1.75,'ok'), 'S0249': (None,'not'),
 'S0250': (2.25,'ok'), 'S0251': (1.75,'ok'), 'S0252': (1.5,'ok'), 'S0253': (2.25,'ok'),
 # tile 34 (S0261 is the numerator of a 3/4 with m beneath)
 'S0254': (None,'not'), 'S0255': (None,'not'), 'S0256': (None,'not'), 'S0257': (None,'not'), 'S0258': (1.25,'ok'),
 'S0259': (None,'not'), 'S0260': (None,'not'), 'S0261': (0.75,'ok'), 'S0262': (1.25,'ok'), 'S0263': (1.25,'ok'),
 'S0264': (None,'not'), 'S0265': (None,'not'), 'S0266': (None,'not'), 'S0267': (None,'not'), 'S0268': (1.75,'ok'),
 'S0269': (1.25,'ok'),
 # tile 35: land
 'S0270': (None,'not'), 'S0271': (None,'not'),
 # tile 40
 'S0272': (5.25,'ok'), 'S0273': (5,'ok'), 'S0274': (5.25,'ok'), 'S0275': (4.5,'ok'), 'S0276': (5.75,'ok'),
 'S0277': (5.25,'ok'), 'S0278': (5,'ok'), 'S0279': (5,'ok'), 'S0280': (5.5,'ok'),
 # tile 41
 'S0281': (4,'ok'), 'S0282': (3.75,'ok'), 'S0283': (4.75,'ok'), 'S0284': (4.5,'ok'), 'S0285': (4,'ok'),
 'S0286': (4.5,'ok'), 'S0287': (5,'ok'), 'S0288': (4,'ok'), 'S0289': (None,'not'), 'S0290': (4.5,'ok'),
 'S0291': (5,'ok'),
 # tile 42
 'S0292': (3.25,'ok'), 'S0293': (3.5,'ok'), 'S0294': (3.75,'ok'), 'S0295': (3.25,'ok'), 'S0296': (3.5,'ok'),
 'S0297': (3.5,'ok'), 'S0298': (4,'ok'), 'S0299': (4.5,'ok'), 'S0300': (4,'ok'), 'S0301': (3.5,'ok'),
 # tile 43 (S0303 + S0305 are one 2 3/4; S0309 is the m under S0307)
 'S0302': (2,'ok'), 'S0303': (None,'not'), 'S0304': (2.25,'ok'), 'S0305': (2.75,'ok'), 'S0306': (2.75,'ok'),
 'S0307': (3,'ok'), 'S0308': (2.25,'ok'), 'S0309': (None,'not'), 'S0310': (3.25,'ok'), 'S0311': (2.75,'ok'),
 'S0312': (3,'ok'), 'S0313': (3.25,'ok'),
 # tile 44
 'S0314': (1.5,'ok'), 'S0315': (0.75,'ok'), 'S0316': (1,'ok'), 'S0317': (1.25,'ok'), 'S0318': (None,'not'),
 'S0319': (0.75,'ok'), 'S0320': (1.5,'ok'), 'S0321': (1.75,'ok'), 'S0322': (2,'ok'), 'S0323': (2.25,'ok'),
 'S0324': (2,'ok'),
 # tile 45
 'S0325': (None,'not'), 'S0326': (0.25,'ok'), 'S0327': (1.25,'ok'), 'S0328': (None,'not'), 'S0329': (None,'not'),
 'S0330': (None,'not'), 'S0331': (1,'ok'), 'S0332': (1.5,'ok'),
 # tile 50
 'S0333': (5.5,'ok'), 'S0334': (6,'ok'), 'S0335': (5.5,'ok'), 'S0336': (None,'not'), 'S0337': (7,'ok'),
 'S0338': (6,'ok'), 'S0339': (7,'ok'), 'S0340': (6,'ok'),
 # tile 51
 'S0341': (5,'ok'), 'S0342': (5.5,'ok'), 'S0343': (5.5,'ok'), 'S0344': (6,'ok'), 'S0345': (6,'ok'),
 # tile 52
 'S0346': (4,'ok'), 'S0347': (5,'ok'), 'S0348': (4.5,'ok'), 'S0349': (None,'not'), 'S0350': (5,'ok'),
 'S0351': (5,'ok'), 'S0352': (4.5,'ok'),
 # tile 53
 'S0353': (2.5,'ok'), 'S0354': (4,'ok'), 'S0355': (3.5,'ok'), 'S0356': (3,'ok'), 'S0357': (None,'not'),
 'S0358': (4,'ok'), 'S0359': (3.5,'ok'), 'S0360': (3.25,'ok'), 'S0361': (None,'not'),
 # tile 54
 'S0362': (2.25,'ok'), 'S0363': (1.5,'ok'), 'S0364': (2.5,'ok'), 'S0365': (2.75,'ok'), 'S0366': (2,'ok'),
 'S0367': (None,'not'), 'S0368': (2.75,'ok'), 'S0369': (2.5,'ok'), 'S0370': (2.25,'ok'),
 # tile 55 (S0378-S0380 are the rock crosses of a rocky patch; S0386 a rock off the shore)
 'S0371': (None,'not'), 'S0372': (1,'ok'), 'S0373': (1.5,'ok'), 'S0374': (None,'not'), 'S0375': (None,'not'),
 'S0376': (1.5,'ok'), 'S0377': (1.25,'ok'), 'S0378': (None,'not'), 'S0379': (None,'not'), 'S0380': (None,'not'),
 'S0381': (1.75,'ok'), 'S0382': (None,'not'), 'S0383': (1,'ok'), 'S0384': (1.5,'ok'), 'S0385': (1.5,'ok'),
 'S0386': (None,'not'),
 # tile 56: land
 'S0387': (None,'not'),
 # tiles 60-66: the bottom strip of the window
 'S0388': (7,'ok'), 'S0389': (6,'ok'), 'S0390': (5.5,'ok'), 'S0391': (6,'ok'), 'S0392': (5,'ok'),
 'S0393': (4,'ok'), 'S0394': (4.5,'ok'), 'S0395': (3.5,'ok'), 'S0396': (3.25,'ok'), 'S0397': (2.75,'ok'),
 'S0398': (3.25,'ok'), 'S0399': (2.5,'ok'), 'S0400': (2.25,'ok'), 'S0401': (1.5,'ok'), 'S0402': (None,'edge'),
 'S0403': (None,'not'),
}

# numbers the detector missed or merged: (window_x, window_y, fathoms, status, note)
ADDED = [
 # tile 00
 (70, 202, 0.5, 'ok', 'missed'), (117, 280, 0.75, 'ok', 'missed'), (42, 337, 0.75, 'ok', 'missed'),
 (400, 200, 0.75, 'ok', 'missed'),
 # tile 01
 (567, 195, 0.75, 'ok', 'missed'), (447, 275, 0.75, 'ok', 'missed'),
 # tile 10
 (242, 512, 1.25, 'ok', 'missed, with r'), (207, 777, 1.75, 'ok', 'missed, with r'),
 # tile 11
 (502, 680, 2, 'ok', 'missed'), (692, 787, 2, 'ok', 'missed'),
 # tile 12
 (1259, 785, 0.5, 'ok', 'missed'),
 # tile 20
 (162, 857, 2.75, 'ok', 'missed'), (115, 947, 2.75, 'ok', 'missed, with r, on bank line'), (20, 1017, 3.5, 'ok', 'missed, with m'),
 # tile 21
 (515, 907, 2.5, 'ok', 'missed'), (670, 1035, 2.5, 'ok', 'missed'), (460, 1140, 3, 'ok', 'missed, r beneath boxed as S0166'),
 # tile 22
 (1115, 1157, 2, 'ok', 'missed, m beneath boxed as S0182'), (972, 1265, 2.5, 'ok', 'missed'),
 # tile 23
 (1619, 1157, 0.75, 'ok', 'missed, in the mud band, m beneath boxed as S0189'),
 # tile 32
 (1230, 1280, 2, 'ok', 'missed'), (940, 1387, 2.75, 'ok', 'missed'), (962, 1505, 3, 'ok', 'missed'),
 (950, 1615, 3.25, 'ok', 'missed'),
 # tile 33
 (1320, 1390, 2, 'ok', 'missed'), (1587, 1390, 1.5, 'ok', 'missed, m beneath boxed as S0249'), (1560, 1597, 2, 'ok', 'missed'),
 # tile 34
 (1992, 1610, 0.5, 'ok', 'missed, between the shoal and the shore'),
 # tile 42
 (1125, 1730, 3, 'ok', 'missed, faint'),
 # tile 44
 (2000, 1952, 1.5, 'ok', 'missed, with m'), (2052, 2122, 1.75, 'ok', 'missed'),
]

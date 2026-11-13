"""Hand transcription of soundings in the beypore window of BA 64.

Site: beypore (candidates for Tyndis: Beypore and Chaliyam; Kadalundi is off the chart's
eastern edge). Sheet: Admiralty chart 64, "Sacrifice Rock to Beipur" (surveyed 1887,
natural scale 1:48,380, soundings in fathoms reduced to lowest low water spring tides).
Window: chart pixels (8300, 11900) to (10740, 14400). The window holds the open
roadstead off Beypore (soundings 1 1/2 to 8 fm), the Beypore river mouth between Beypore
(Beipur) and Chaliyam, the bar and the shoal inside it marked "dry at L.W.", Rocky Lumps
and Black Rocks off Chaliyam, and land on the right (Beipur town, the Factory, Chaliyam,
the R.C. cemetery). The chart's eastern border closes the window on the right; the window
is cut at the bottom before the coastal-view panorama.

Values were read by eye from the numbered tiles in data/soundings/beypore/tiles/,
with ambiguous glyphs re-read on enlarged crops of the chart.
Status codes:
  ok        clear reading
  unsure    legible but could be misread, or a lone fraction that may not be a sounding
  edge      cut by the window border; excluded from modelling
  drop      ambiguous on the second check; excluded
  not       detector picked up something that is not a sounding (text, house, palm, rock
            '+', bank line, bottom-quality letter)
  split     detector box merged two numbers; both are in ADDED
Rows starting with 'A' are numbers the detector missed. Their position is the
window pixel read off the tile image (accurate to roughly +/- 5 chart px).
Where the detector boxed the numerator and denominator of a lone fraction separately
(S0096/S0164, S0131/S0133, S0153/S0154, S0249/S0252), both boxes are 'not' and the
fraction is entered once in ADDED at its centre.

Notes:
- Lone 1/4, 1/2 and 3/4 cluster in the river mouth, on the bar and around Rocky Lumps;
  all are marked unsure, because some sit on the dotted foreshore and drying-bank lines.
- Several lone "3"s sit on the double-dotted line running down the roadstead (S0009,
  S0016, S0064, S0121, S0122, A020). They may be labels of that depth line rather than
  soundings; either way they give 3 fm at that point, and are kept as ok.
- A "1" beside the flagstaff ("F.S.") at about window (1986, 1480) sits on the shore at
  Chaliyam and was not entered.
- Second pass: every reading was checked against its contact sheet in check/. No value
  was changed; four hand-added positions (A001, A026, A027, A029) were re-centred.
"""
# detector id -> (value in fathoms or None, status)
READ = {
 # tile 00
 'S0000': (4.25,'ok'), 'S0001': (4.75,'ok'), 'S0002': (4,'ok'), 'S0003': (4.75,'ok'), 'S0004': (4.25,'ok'),
 'S0005': (4.75,'ok'), 'S0006': (5.25,'ok'), 'S0007': (4.5,'ok'),
 # tile 01
 'S0008': (2.75,'ok'), 'S0009': (3,'ok'), 'S0010': (3.25,'ok'), 'S0011': (3.75,'ok'), 'S0012': (3.5,'ok'),
 'S0013': (None,'not'), 'S0014': (4,'ok'), 'S0015': (3.75,'ok'), 'S0016': (3,'ok'),
 # tile 02
 'S0017': (1.5,'ok'), 'S0018': (2,'ok'), 'S0019': (2.25,'ok'), 'S0020': (2.75,'ok'), 'S0021': (2.25,'ok'),
 'S0022': (1.75,'ok'), 'S0023': (2.25,'ok'), 'S0024': (None,'not'), 'S0025': (2.75,'ok'), 'S0026': (1.75,'ok'),
 'S0027': (2.25,'ok'), 'S0028': (1.75,'ok'), 'S0029': (3,'ok'), 'S0030': (2.25,'ok'),
 # tile 03 (shore, palms and houses)
 'S0031': (None,'not'), 'S0032': (None,'not'), 'S0033': (0.75,'unsure'), 'S0034': (None,'not'), 'S0035': (None,'not'),
 'S0036': (None,'not'), 'S0037': (None,'not'), 'S0038': (None,'not'), 'S0039': (None,'not'),
 # tile 04 (land: houses)
 'S0040': (None,'not'), 'S0041': (None,'not'), 'S0042': (None,'not'), 'S0043': (None,'not'), 'S0044': (None,'not'),
 'S0045': (None,'not'),
 # tile 10
 'S0046': (5.5,'ok'), 'S0047': (5,'ok'), 'S0048': (5,'ok'), 'S0049': (None,'not'), 'S0050': (5.75,'ok'),
 'S0051': (5.25,'ok'), 'S0052': (6,'ok'),
 # tile 11
 'S0053': (4.25,'ok'), 'S0054': (3.25,'ok'), 'S0055': (4,'ok'), 'S0056': (None,'not'), 'S0057': (4.75,'ok'),
 'S0058': (3.5,'ok'), 'S0059': (3.75,'ok'), 'S0060': (4.75,'ok'),
 # tile 12
 'S0061': (2.5,'ok'), 'S0062': (2.75,'ok'), 'S0063': (2.25,'ok'), 'S0064': (3,'ok'), 'S0065': (2.75,'ok'),
 'S0066': (2.25,'ok'), 'S0067': (3.5,'ok'), 'S0068': (2.25,'ok'), 'S0069': (2.75,'ok'), 'S0070': (3.25,'ok'),
 # tile 13
 'S0071': (1,'ok'), 'S0072': (1.25,'ok'), 'S0073': (1.75,'ok'), 'S0074': (1.25,'ok'), 'S0075': (2,'ok'),
 'S0076': (1.75,'ok'), 'S0077': (None,'not'), 'S0078': (1.5,'ok'), 'S0079': (1.75,'ok'),
 # tile 14 (land: houses, "North port boundary Pillar")
 'S0080': (None,'not'), 'S0081': (None,'not'), 'S0082': (None,'not'), 'S0083': (None,'not'), 'S0084': (None,'not'),
 'S0085': (None,'not'), 'S0086': (None,'not'), 'S0087': (None,'not'),
 # tile 15 (Factory, river north of Chaliyam)
 'S0088': (None,'not'), 'S0089': (None,'not'), 'S0090': (None,'not'), 'S0091': (1,'ok'), 'S0092': (None,'not'),
 'S0093': (1.75,'ok'), 'S0094': (None,'not'), 'S0095': (0.75,'unsure'), 'S0096': (None,'not'),
 # tile 20
 'S0097': (5.75,'ok'), 'S0098': (5.25,'ok'), 'S0099': (5.75,'ok'), 'S0100': (6,'ok'), 'S0101': (5.25,'ok'),
 'S0102': (6,'ok'), 'S0103': (5.5,'ok'),
 # tile 21
 'S0104': (3.75,'ok'), 'S0105': (4.75,'ok'), 'S0106': (4.25,'ok'), 'S0107': (3.75,'ok'), 'S0108': (4.75,'ok'),
 'S0109': (4.25,'ok'), 'S0110': (4.25,'ok'), 'S0111': (4.75,'ok'), 'S0112': (4.5,'ok'), 'S0113': (4.25,'ok'),
 'S0114': (4.75,'ok'), 'S0115': (5.25,'ok'),
 # tile 22
 'S0116': (2.75,'ok'), 'S0117': (3.25,'ok'), 'S0118': (3.5,'ok'), 'S0119': (3.25,'ok'), 'S0120': (3.75,'ok'),
 'S0121': (3,'ok'), 'S0122': (3,'ok'), 'S0123': (3.25,'ok'), 'S0124': (3.5,'ok'), 'S0125': (3.25,'ok'),
 # tile 23
 'S0126': (1.25,'ok'), 'S0127': (1.75,'ok'), 'S0128': (2.25,'ok'), 'S0129': (None,'not'), 'S0130': (None,'not'),
 'S0131': (None,'not'), 'S0132': (None,'not'), 'S0133': (None,'not'), 'S0134': (1.75,'ok'), 'S0135': (2.75,'ok'),
 'S0136': (2.25,'ok'), 'S0137': (1.5,'ok'), 'S0138': (2.75,'ok'), 'S0139': (2,'ok'), 'S0140': (1.5,'ok'),
 'S0141': (2.75,'ok'), 'S0142': (2.5,'ok'),
 # tile 24 (Beipur town; S0131/S0133 and S0153/S0154 are the two halves of lone fractions, entered in ADDED)
 'S0143': (None,'not'), 'S0144': (None,'not'), 'S0145': (None,'not'), 'S0146': (None,'not'), 'S0147': (None,'not'),
 'S0148': (None,'not'), 'S0149': (None,'not'), 'S0150': (None,'not'), 'S0151': (0.25,'unsure'), 'S0152': (None,'not'),
 'S0153': (None,'not'), 'S0154': (None,'not'), 'S0155': (None,'not'), 'S0156': (None,'not'), 'S0157': (1.75,'ok'),
 'S0158': (None,'not'), 'S0159': (None,'not'), 'S0160': (1.25,'ok'), 'S0161': (1.25,'ok'),
 # tile 25 (river mouth between Beipur and Chaliyam)
 'S0162': (0.25,'unsure'), 'S0163': (1,'ok'), 'S0164': (None,'not'), 'S0165': (None,'not'), 'S0166': (0.75,'unsure'),
 'S0167': (1.5,'ok'), 'S0168': (1.75,'ok'), 'S0169': (0.5,'unsure'), 'S0170': (0.25,'unsure'), 'S0171': (1.5,'ok'),
 'S0172': (0.5,'unsure'), 'S0173': (None,'not'), 'S0174': (None,'not'), 'S0175': (0.25,'unsure'), 'S0176': (None,'not'),
 'S0177': (0.5,'unsure'),
 # tile 30
 'S0178': (6.5,'ok'), 'S0179': (6,'ok'), 'S0180': (6,'ok'), 'S0181': (6,'ok'), 'S0182': (7,'ok'), 'S0183': (6,'ok'),
 # tile 31
 'S0184': (4.25,'ok'), 'S0185': (4.75,'ok'), 'S0186': (5.25,'ok'), 'S0187': (4.25,'ok'), 'S0188': (4.75,'ok'),
 'S0189': (5,'ok'), 'S0190': (5.5,'ok'), 'S0191': (None,'not'), 'S0192': (4.75,'ok'), 'S0193': (5.25,'ok'),
 'S0194': (6,'ok'), 'S0195': (5,'ok'),
 # tile 32
 'S0196': (4,'ok'), 'S0197': (3.75,'ok'), 'S0198': (3.25,'ok'), 'S0199': (4.25,'ok'), 'S0200': (4.75,'ok'),
 'S0201': (3.25,'ok'), 'S0202': (3.5,'ok'), 'S0203': (4.5,'ok'), 'S0204': (3.75,'ok'), 'S0205': (3.5,'ok'),
 'S0206': (4.75,'ok'),
 # tile 33
 'S0207': (1.5,'ok'), 'S0208': (1.75,'ok'), 'S0209': (None,'not'), 'S0210': (2.75,'ok'), 'S0211': (None,'not'),
 'S0212': (2.75,'ok'), 'S0213': (2.25,'ok'), 'S0214': (2,'ok'), 'S0215': (None,'not'), 'S0216': (2.5,'ok'),
 'S0217': (2,'ok'), 'S0218': (None,'not'), 'S0219': (2.25,'ok'), 'S0220': (3,'ok'), 'S0221': (2.75,'ok'),
 'S0222': (3,'ok'), 'S0223': (1.5,'ok'), 'S0224': (2.75,'ok'), 'S0225': (3.25,'ok'), 'S0226': (2.5,'ok'),
 # tile 34 (Beypore bar and the shoal inside it, "dry at L.W."; east half is land at Chaliyam)
 'S0227': (2.25,'ok'), 'S0228': (1.75,'ok'), 'S0229': (0.25,'unsure'), 'S0230': (None,'not'), 'S0231': (None,'not'),
 'S0232': (2.5,'ok'), 'S0233': (None,'not'), 'S0234': (None,'not'), 'S0235': (None,'not'), 'S0236': (1.75,'ok'),
 'S0237': (3,'ok'), 'S0238': (1,'ok'), 'S0239': (0.25,'unsure'), 'S0240': (0.25,'unsure'), 'S0241': (None,'not'),
 'S0242': (2.75,'ok'), 'S0243': (None,'not'), 'S0244': (None,'not'), 'S0245': (0.5,'unsure'), 'S0246': (0.25,'unsure'),
 'S0247': (2,'ok'), 'S0248': (None,'not'), 'S0249': (None,'not'), 'S0250': (None,'not'), 'S0251': (None,'not'),
 'S0252': (None,'not'), 'S0253': (None,'not'), 'S0254': (None,'not'), 'S0255': (None,'not'), 'S0256': (None,'not'),
 'S0257': (0.5,'unsure'), 'S0258': (None,'not'), 'S0259': (1.25,'ok'), 'S0260': (None,'not'), 'S0261': (None,'not'),
 # tile 35 (land at Chaliyam and the inner channel; no soundings)
 'S0262': (None,'not'), 'S0263': (None,'not'), 'S0264': (None,'not'), 'S0265': (None,'not'), 'S0266': (None,'not'),
 'S0267': (None,'not'), 'S0268': (None,'not'), 'S0269': (None,'not'), 'S0270': (None,'not'),
 # tile 40
 'S0271': (6,'ok'), 'S0272': (7,'ok'), 'S0273': (7,'ok'), 'S0274': (7,'ok'), 'S0275': (7,'ok'), 'S0276': (7,'ok'),
 # tile 41
 'S0277': (None,'not'), 'S0278': (5.25,'ok'), 'S0279': (6,'ok'), 'S0280': (5.25,'ok'), 'S0281': (5.5,'ok'),
 'S0282': (None,'not'), 'S0283': (6,'ok'), 'S0284': (6,'ok'), 'S0285': (5.5,'ok'), 'S0286': (5.75,'ok'),
 # tile 42
 'S0287': (4.25,'ok'), 'S0288': (3.75,'ok'), 'S0289': (3.75,'ok'), 'S0290': (4.75,'ok'), 'S0291': (4.75,'ok'),
 'S0292': (4.5,'ok'), 'S0293': (5.25,'ok'), 'S0294': (4.75,'ok'), 'S0295': (4.5,'ok'), 'S0296': (4.25,'ok'),
 'S0297': (5.25,'ok'),
 # tile 43 ("BEIPUR RIVER (see plan)")
 'S0298': (2.25,'ok'), 'S0299': (2.75,'ok'), 'S0300': (None,'not'), 'S0301': (2.5,'ok'), 'S0302': (3.25,'ok'),
 'S0303': (2.75,'ok'), 'S0304': (3.75,'ok'), 'S0305': (None,'not'), 'S0306': (None,'not'), 'S0307': (None,'not'),
 'S0308': (None,'not'), 'S0309': (3,'ok'), 'S0310': (None,'not'), 'S0311': (3.25,'ok'), 'S0312': (3.75,'ok'),
 'S0313': (3,'ok'), 'S0314': (3.75,'ok'), 'S0315': (3.5,'ok'),
 # tile 44 (Rocky Lumps and Black Rocks off Chaliyam; '+' are rocks awash)
 'S0316': (None,'not'), 'S0317': (None,'not'), 'S0318': (None,'not'), 'S0319': (2,'ok'), 'S0320': (0.25,'unsure'),
 'S0321': (1.25,'ok'), 'S0322': (0.5,'unsure'), 'S0323': (None,'not'), 'S0324': (2,'ok'), 'S0325': (0.25,'unsure'),
 'S0326': (None,'not'), 'S0327': (None,'not'), 'S0328': (None,'not'), 'S0329': (None,'not'), 'S0330': (None,'not'),
 'S0331': (None,'not'), 'S0332': (2.5,'ok'), 'S0333': (1,'ok'), 'S0334': (2,'ok'), 'S0335': (2.25,'ok'),
 'S0336': (2.5,'ok'), 'S0337': (1.25,'ok'), 'S0338': (2.25,'ok'), 'S0339': (2,'ok'), 'S0340': (2.5,'ok'),
 'S0341': (1.75,'ok'), 'S0342': (2,'ok'),
 # tile 45 (Chaliyam; fractions on the foreshore south of the river mouth)
 'S0343': (None,'not'), 'S0344': (None,'not'), 'S0345': (None,'not'), 'S0346': (None,'not'), 'S0347': (None,'not'),
 'S0348': (None,'not'), 'S0349': (None,'not'), 'S0350': (None,'not'), 'S0351': (None,'not'), 'S0352': (None,'not'),
 'S0353': (None,'not'), 'S0354': (0.25,'unsure'), 'S0355': (None,'not'), 'S0356': (None,'not'), 'S0357': (0.75,'unsure'),
 'S0358': (None,'not'), 'S0359': (None,'not'), 'S0360': (0.25,'unsure'), 'S0361': (0.75,'unsure'), 'S0362': (0.25,'unsure'),
 'S0363': (None,'not'), 'S0364': (None,'not'), 'S0365': (1,'ok'),
 # tile 50
 'S0366': (7,'ok'), 'S0367': (None,'edge'), 'S0368': (8,'ok'), 'S0369': (None,'edge'),
 # tile 51
 'S0370': (7,'ok'), 'S0371': (6,'ok'), 'S0372': (7,'ok'), 'S0373': (6,'ok'), 'S0374': (6,'ok'), 'S0375': (6.5,'ok'),
 'S0376': (7,'ok'),
 # tile 52
 'S0377': (5,'ok'), 'S0378': (4.75,'ok'), 'S0379': (5.75,'ok'), 'S0380': (5.25,'ok'), 'S0381': (4.75,'ok'),
 'S0382': (5.5,'ok'), 'S0383': (5.75,'ok'), 'S0384': (5,'ok'), 'S0385': (6,'ok'), 'S0386': (5.25,'ok'),
 # tile 53
 'S0387': (4.25,'ok'), 'S0388': (2.75,'ok'), 'S0389': (3.5,'ok'), 'S0390': (None,'not'), 'S0391': (None,'not'),
 'S0392': (3.25,'ok'), 'S0393': (3.5,'ok'), 'S0394': (4,'ok'), 'S0395': (3.75,'ok'), 'S0396': (4.25,'ok'),
 'S0397': (3.25,'ok'), 'S0398': (4.25,'ok'), 'S0399': (3.75,'ok'), 'S0400': (4,'ok'), 'S0401': (None,'edge'),
 # tile 54
 'S0402': (2.25,'ok'), 'S0403': (2,'ok'), 'S0404': (2.5,'ok'), 'S0405': (2.25,'ok'), 'S0406': (2.75,'ok'),
 'S0407': (2.75,'ok'), 'S0408': (None,'not'), 'S0409': (2.75,'ok'), 'S0410': (2.25,'ok'), 'S0411': (2,'ok'),
 'S0412': (1,'ok'), 'S0413': (1.25,'ok'), 'S0414': (2.75,'ok'), 'S0415': (2.5,'ok'), 'S0416': (2,'ok'),
 'S0417': (3.25,'ok'), 'S0418': (2.75,'ok'), 'S0419': (None,'not'), 'S0420': (None,'edge'),
 # tile 55
 'S0421': (1.5,'ok'), 'S0422': (0.25,'unsure'), 'S0423': (1.5,'ok'), 'S0424': (1.75,'ok'), 'S0425': (1.5,'ok'),
 'S0426': (None,'not'), 'S0427': (1.5,'ok'), 'S0428': (None,'not'), 'S0429': (None,'not'), 'S0430': (1.75,'ok'),
 'S0431': (1.5,'ok'),
}

# numbers the detector missed or merged: (window_x, window_y, fathoms, status, note)
ADDED = [
 (623, 437, 3.5, 'ok', 'missed'), (1367, 408, 1.5, 'ok', 'missed; position corrected on check'), (702, 827, 4.25, 'ok', 'missed'),
 (1410, 1158, 2.5, 'ok', 'missed'),
 (1654, 985, 0.75, 'unsure', 'lone fraction; detector split it as S0131/S0133'),
 (1740, 1097, 0.75, 'unsure', 'lone fraction; detector split it as S0153/S0154'),
 (2287, 855, 0.75, 'unsure', 'lone fraction; detector split it as S0096/S0164'),
 (2398, 1048, 0.75, 'unsure', 'missed lone fraction'),
 (1806, 1280, 0.75, 'unsure', 'missed lone fraction'), (1885, 1554, 2.25, 'ok', 'missed'),
 (1760, 1592, 0.75, 'unsure', 'lone fraction; detector split it as S0249/S0252'),
 (1806, 1596, 1.25, 'ok', 'missed'), (1846, 1596, 1.75, 'ok', 'missed'), (1890, 1591, 1.25, 'ok', 'missed'),
 (1819, 1637, 1.5, 'ok', 'missed'), (1779, 1655, 0.75, 'unsure', 'missed lone fraction'),
 (2085, 1377, 0.25, 'unsure', 'missed lone fraction'), (1928, 1612, 0.75, 'unsure', 'missed lone fraction'),
 (905, 1767, 4.75, 'ok', 'missed'), (1120, 1855, 4.25, 'ok', 'missed'),
 (1650, 2065, 3, 'ok', 'missed, on contour'),
 (1811, 1712, 0.75, 'unsure', 'missed lone fraction'), (1864, 1832, 0.75, 'unsure', 'missed lone fraction, Rocky Lumps'),
 (1917, 1830, 0.75, 'unsure', 'missed lone fraction, Rocky Lumps'), (2061, 1884, 0.25, 'unsure', 'missed lone fraction'),
 (1996, 1892, 0.5, 'unsure', 'missed lone fraction'), (2054, 2019, 1.75, 'ok', 'missed; position corrected on check'),
 (2131, 2074, 1.75, 'ok', 'missed; position corrected on check'), (1242, 2130, 4.5, 'ok', 'missed'),
 (1345, 2240, 4.25, 'ok', 'missed; position corrected on check'), (1930, 2360, 1.25, 'ok', 'missed, inside dotted rock ring'),
 (2095, 2275, 2.25, 'ok', 'missed'), (2365, 2265, 1, 'ok', 'missed, on foreshore edge'),
 (2220, 2362, 1.75, 'ok', 'missed'),
]

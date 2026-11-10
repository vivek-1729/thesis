"""Geocode the findspots that Indian Archaeology: A Review names by village.

IAR reports fieldwork as "megalithic burials of topikal type at Alancode,
Ongallur, Ponumundum, Tennala, Thannairkod and Thavanur". Those names are the
actual footprint of the 1978-79 search for Roman contact in the Ponnani valley,
and the 1969-70 excavations around Cranganore. Plotting them shows where
archaeologists have physically been.

Nominatim will return something for almost any string, so every result keeps
its returned display_name and is checked against the district IAR gives. A
mismatch is recorded, not silently accepted.
"""
import json, time, urllib.parse, urllib.request, csv, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "data" / "raw"
UA = {"User-Agent": "harvard-thesis-periplus/1.0 (vivekshah@college.harvard.edu)"}

# (name, expected district or region, IAR volume, what was found)
PLACES = [
    # 1969-70 no.18 -- ASI + Kerala Dept excavations in and around Cranganore
    ("Mathilakam",            "Thrissur",   "1969-70", "excavation; 9th-11th c. Chera", "Muziris"),
    ("Thiruvanchikulam",      "Thrissur",   "1969-70", "excavation; 9th-11th c. Chera", "Muziris"),
    ("Thrikkulasekharapuram", "Thrissur",   "1969-70", "excavation; 9th-11th c. Chera", "Muziris"),
    ("Karupadanna",           "Thrissur",   "1969-70", "excavation; 9th-11th c. Chera", "Muziris"),
    ("Kodungallur",           "Thrissur",   "1969-70", "excavation; 9th-11th c. Chera", "Muziris"),
    # 1978-79 no.40 -- survey "investigating for the sites showing Roman contact"
    ("Ongallur",              "Palakkad",   "1978-79", "megalithic topikal burials", "Tyndis"),
    ("Thennala",              "Malappuram", "1978-79", "megalithic topikal burials", "Tyndis"),
    ("Thavanur",              "Malappuram", "1978-79", "megalithic topikal burials", "Tyndis"),
    ("Thirunavaya",           "Malappuram", "1978-79", "menhirs", "Tyndis"),
    ("Alanallur",             "Palakkad",   "1978-79", "megalithic topikal burials", "Tyndis"),
    ("Ponnani",               "Malappuram", "1978-79", "survey area (Ponnani valley)", "Tyndis"),
    ("Kuttippuram",           "Malappuram", "1976-77", "microliths, river terrace", "Tyndis"),
    # 1970-71 no.26
    ("Pattambi",              "Palakkad",   "1970-71", "Russet-coated Painted Ware area", "Tyndis"),
    # 1960s-70s rock-cut caves, Kerala coast
    ("Triprangode",           "Malappuram", "1962-63", "rock-cut caves, megalithic BRW", "Tyndis"),
    ("Koyilandy",             "Kozhikode",  "-",       "candidate, no recorded fieldwork", "Tyndis"),
    ("Tanur",                 "Malappuram", "-",       "candidate, no recorded fieldwork", "Tyndis"),
    ("Kadalundi",             "Kozhikode",  "-",       "candidate, no recorded fieldwork", "Tyndis"),
    ("Beypore",               "Kozhikode",  "-",       "candidate, no recorded fieldwork", "Tyndis"),
    # Nelkynda / Bakare candidates
    ("Niranam",               "Pathanamthitta", "-",   "candidate, no recorded fieldwork", "Nelkynda"),
    ("Neendakara",            "Kollam",     "-",       "candidate, no recorded fieldwork", "Nelkynda"),
    ("Purakkad",              "Alappuzha",  "-",       "candidate, no recorded fieldwork", "Bakare"),
    ("Thevalakkara",          "Kollam",     "-",       "candidate, no recorded fieldwork", "Bakare"),
    ("Pattanam",              "Ernakulam",  "2008-09", "KCHR excavation", "Muziris"),
    ("North Paravur",         "Ernakulam",  "-",       "PARUR hoard locality", "Muziris"),
]

def geocode(name, district):
    q = f"{name}, {district}, Kerala, India" if district != "-" else f"{name}, Kerala, India"
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode(
        {"q": q, "format": "json", "limit": 3, "addressdetails": 1})
    try:
        d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=45))
    except Exception as e:
        return None, "", f"ERR {str(e)[:30]}"
    if not d:
        return None, "", "no result"
    best = d[0]
    disp = best.get("display_name", "")
    ok = district == "-" or district.lower().split()[0] in disp.lower()
    return (float(best["lat"]), float(best["lon"])), disp, ("district match" if ok
                                                            else "DISTRICT MISMATCH")

def main():
    rows = []
    for name, district, vol, what, port in PLACES:
        coord, disp, status = geocode(name, district)
        rows.append({
            "name": name, "district": district, "iar_volume": vol,
            "what_was_found": what, "port": port,
            "lat": coord[0] if coord else "", "lon": coord[1] if coord else "",
            "geocode_status": status, "nominatim_display_name": disp[:150],
        })
        flag = "" if status == "district match" else f"   <-- {status}"
        ll = f"{coord[0]:.4f},{coord[1]:.4f}" if coord else "--"
        print(f"  {name:24s} {ll:20s} {flag}")
        time.sleep(1.1)                   # Nominatim asks for <= 1 req/sec
    dest = OUT / "iar_findspots.csv"
    with open(dest, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    good = sum(1 for r in rows if r["geocode_status"] == "district match")
    print(f"\n{good}/{len(rows)} geocoded with a district match -> {dest.name}")

if __name__ == "__main__":
    main()

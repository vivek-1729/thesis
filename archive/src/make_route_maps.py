"""One map per itinerary.

The Periplus describes two separate voyages out of Egypt, not one circuit: down
the African coast to Rhapta, and along Arabia to India. At basin scale the Malabar
and Horn clusters collapse into smudges; at route scale every port is legible and
the reading order of the text can be numbered onto the map.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mapkit as mk

plt.rcParams.update({"font.family": ["Helvetica Neue", "Helvetica", "DejaVu Sans"]})

ROUTES = {
    "Western Route": dict(
        slug="02_route_western",
        title="The western route — Egypt to Azania",
        blurb=("Down the African coast from the Red Sea ports to Rhapta, which the text "
               "calls the last market of Azania: “beyond these places the unexplored "
               "ocean curves around toward the west.”"),
        bbox=(31, 53.5, -10.5, 31.5), figsize=(10.5, 15.2), fs=8.0,
        legend=dict(loc="lower right", bbox_to_anchor=(0.995, 0.015)),
    ),
    "Eastern Route": dict(
        slug="03_route_eastern",
        title="The eastern route — Arabia to India",
        blurb=("Along Arabia and the Persian Gulf to the Indus, then down the Indian "
               "coast. Ch. 57 credits Hippalus with the open-sea crossing that let ships "
               "run straight across on the southwest monsoon instead of hugging the coast."),
        bbox=(35.5, 85.5, 5.5, 28.5), figsize=(17, 9.4), fs=7.6,
        legend=dict(loc="lower left", bbox_to_anchor=(0.005, 0.015)),
    ),
}


def draw_route(route_name, cfg, g, chains, pos):
    chain = chains[route_name]
    order = {name: i + 1 for i, name in enumerate(chain)}
    sub = g[(g.route == route_name) & (g.route_role == "port of call")
            & g.lat.notna()].copy()
    bbox = cfg["bbox"]

    fig = plt.figure(figsize=cfg["figsize"], facecolor=mk.SURFACE)
    ax = fig.add_axes([0.055, 0.045, 0.925, 0.845])
    mk.draw_base(ax, bbox)
    mk.draw_legs(ax, chain, pos, lw=1.1)
    mk.draw_candidates(ax, set(sub[sub.in_brief_disputed].toponym), s=24)
    mk.draw_sites(ax, sub, size=78)

    # Number the ports in the order the text visits them, so the itinerary is readable.
    mk.place_labels(ax, fig, [
        {"name": (f"{order[r.toponym]}  {r.toponym}" if r.toponym in order
                  else f"·  {r.toponym}"),
         "lon": r.lon, "lat": r.lat,
         "key": bool(r.in_brief_disputed) or r.tier_letter == "A"}
        for r in sub.itertuples()], bbox, fs=cfg["fs"])

    mk.tier_legend(ax, sub, title="How well located", fontsize=9, **cfg["legend"])
    ax.set_xlabel("longitude °E", fontsize=9, color=mk.MUTED)
    ax.set_ylabel("latitude °", fontsize=9, color=mk.MUTED)

    unchained = sorted(set(sub.toponym) - set(order))
    fig.text(0.055, 0.975, cfg["title"], fontsize=17, color=mk.INK, va="top")
    fig.text(0.055, 0.941, cfg["blurb"], fontsize=10, color=mk.INK_2, va="top",
             wrap=True)
    note = (f"{len(sub)} ports of call, chapters "
            f"{sub.chapter_num.min():.0f}–{sub.chapter_num.max():.0f}. "
            f"Numbers give the order the text visits them. "
            f"{int((sub.tier_letter == 'A').sum())} rest on an excavated identification.")
    if unchained:
        note += (f" Not in the chain (no successor recorded): {', '.join(unchained)}.")
    fig.text(0.055, 0.905, note, fontsize=8.5, color=mk.MUTED, va="top",
             linespacing=1.5)

    out = mk.FIG / f"{cfg['slug']}.png"
    fig.savefig(out, dpi=190, facecolor=mk.SURFACE)
    plt.close(fig)
    print("wrote", out)


def main():
    g = mk.load_sites()
    chains, pos = mk.sailing_chains(g)
    for name, cfg in ROUTES.items():
        draw_route(name, cfg, g, chains, pos)


if __name__ == "__main__":
    main()

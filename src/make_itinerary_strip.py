"""The itinerary as a strip: one row per port, in the order the text visits them.

Bar    = the real distance to the next port (great-circle).
Tick   = the distance the TEXT states for that leg, converted at the stadion
         calibrated from securely-located legs.
Label  = a stated duration where the text gives days instead of stadia.
Blank  = the text says nothing about that leg, which is most of them.

Where bar and tick line up, text and geography agree. Where they do not, either
the distance is corrupt or a port is misplaced -- and the tier dot beside the name
says which is more likely.
"""
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mapkit as mk

# Calibrated from the four legs whose endpoints are both securely located
# (median 154 m, a lower bound since great-circle understates a sailed route).
STADION_M = 160
BAR, TICK = "#9ec5f4", "#0b0b0b"
plt.rcParams.update({"font.family": ["Helvetica Neue", "Helvetica", "DejaVu Sans"]})


def great_circle(g, a, b):
    p1, p2 = math.radians(g.lat[a]), math.radians(g.lat[b])
    return 2 * 6371 * math.asin(math.sqrt(
        math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2)
        * math.sin(math.radians(g.lon[b] - g.lon[a]) / 2) ** 2))


def leg_table(g, chain, dist):
    """One row per port; the measurement columns describe the leg to the NEXT port."""
    stated = {r.from_site: r for r in dist[dist.kind == "leg"].itertuples()
              if pd.notna(r.to_site) and pd.notna(r.from_site)}
    rows = []
    for i, name in enumerate(chain):
        nxt = chain[i + 1] if i + 1 < len(chain) else None
        s = stated.get(name)
        # Compare like with like: if the text measures to a port further along the
        # chain, the bar has to run to that same port or the tick is meaningless.
        target = s.to_site if (s is not None and s.to_site in chain) else nxt
        skips = target != nxt and target is not None
        rows.append({
            "port": name, "tier": g.tier_letter[name],
            "disputed": bool(g.in_brief_disputed[name]),
            "actual_km": great_circle(g, name, target) if target else None,
            "skip_to": target if skips else None,
            "stated_km": (s.value * STADION_M / 1000
                          if s is not None and s.unit == "stadia" else None),
            "duration": (f"{'' if pd.isna(s.value) else int(s.value)}"
                         + {"days_sail": " days' sail", "days_journey": " days",
                            "days_bare": " days", "day_and_night": " day+night"}[s.unit]
                         if s is not None and s.unit != "stadia" else None),
        })
    return pd.DataFrame(rows)


def draw(ax, t, title, xmax):
    y = range(len(t))
    ax.barh(list(y), t.actual_km.fillna(0).clip(upper=xmax), height=0.55,
            color=BAR, zorder=2)
    for i, r in enumerate(t.itertuples()):
        if pd.notna(r.actual_km) and r.actual_km > xmax:
            ax.text(xmax * 0.985, i, f"{r.actual_km:.0f} km →", fontsize=6.6,
                    va="center", ha="right", color=mk.INK, zorder=6)
        if r.skip_to:
            ax.text(min(r.actual_km, xmax) + xmax * 0.015, i, f"to {r.skip_to}",
                    fontsize=6.2, va="center", color=mk.MUTED, zorder=4)
        if pd.notna(r.stated_km):
            ax.plot([r.stated_km, r.stated_km], [i - 0.38, i + 0.38],
                    color=TICK, lw=1.8, zorder=4, solid_capstyle="butt")
        if r.duration:
            ax.text(min(r.actual_km or 0, xmax) + xmax * 0.015, i, r.duration, fontsize=6.6,
                    va="center", color=mk.INK_2, zorder=4)
        ax.scatter([-0.26], [i], s=34, color=mk.TIER_COLOR[r.tier], zorder=5,
                   clip_on=False, transform=ax.get_yaxis_transform())
    ax.set_yticks(list(y))
    ax.set_yticklabels([f"{i+1}. {r.port}" for i, r in enumerate(t.itertuples())],
                       fontsize=7.4)
    for lbl, r in zip(ax.get_yticklabels(), t.itertuples()):
        lbl.set_color(mk.INK if r.disputed else mk.INK_2)
        lbl.set_fontweight("bold" if r.disputed else "normal")
    ax.invert_yaxis()
    ax.set_xlim(0, xmax)
    ax.set_ylim(len(t) - 0.5, -0.5)
    ax.set_xlabel("km to the next port", fontsize=8, color=mk.MUTED)
    ax.set_title(title, fontsize=11, color=mk.INK, pad=8, loc="left")
    ax.tick_params(axis="x", colors=mk.MUTED, labelsize=7.5)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color=mk.HAIRLINE, lw=0.6, zorder=0)
    ax.set_facecolor(mk.SURFACE)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(mk.LAND_EDGE)


def main():
    g = mk.load_sites().set_index("toponym")
    dist = pd.read_csv(mk.PROC / "distances.csv")
    chains, _ = mk.sailing_chains(mk.load_sites())
    west = leg_table(g, chains["Western Route"], dist)
    east = leg_table(g, chains["Eastern Route"], dist)
    xmax = 900

    fig = plt.figure(figsize=(13.5, 11), facecolor=mk.SURFACE)
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1], wspace=0.34,
                          left=0.155, right=0.985, top=0.800, bottom=0.065)
    draw(fig.add_subplot(gs[0]), west,
         f"Western route — Egypt to Azania  ({len(west)} ports)", xmax)
    draw(fig.add_subplot(gs[1]), east,
         f"Eastern route — Arabia to India  ({len(east)} ports)", xmax)

    n_stated = int(west.stated_km.notna().sum() + east.stated_km.notna().sum())
    n_dur = int(west.duration.notna().sum() + east.duration.notna().sum())
    n_legs = len(west) + len(east) - 2
    fig.text(0.155, 0.972, "What the Periplus actually measures",
             fontsize=17, color=mk.INK, va="top")
    fig.text(0.155, 0.940,
             f"Every port in the order the text visits it. Bars are the real distance to the next port; "
             f"black ticks are the distance the text states.\nOf {n_legs} sailing legs, "
             f"{n_stated} carry a stated distance and {n_dur} a stated duration — the rest of the route the text simply does not measure.",
             fontsize=9.5, color=mk.INK_2, va="top", linespacing=1.6)

    handles = [
        Line2D([], [], marker="s", ls="", ms=9, mfc=BAR, mec=BAR, label="Actual distance"),
        Line2D([], [], color=TICK, lw=1.8, label=f"Stated in the text (stadion = {STADION_M} m)"),
    ] + [Line2D([], [], marker="o", ls="", ms=7, mfc=mk.TIER_COLOR[k], mec=mk.SURFACE,
                label=f"{k}  {mk.TIER_LABEL[k]}") for k in "ABCD"]
    leg = fig.legend(handles=handles, loc="upper right", frameon=False, fontsize=8.4,
                     ncol=3, bbox_to_anchor=(0.985, 0.893), labelcolor=mk.INK,
                     columnspacing=1.6, handletextpad=0.7)
    leg.set_zorder(9)

    out = mk.FIG / "04_itinerary_strip.png"
    fig.savefig(out, dpi=190, facecolor=mk.SURFACE)
    print("wrote", out)


if __name__ == "__main__":
    main()

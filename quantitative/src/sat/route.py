"""Sailed distance between candidates, measured through water rather than across land.

The Periplus gives the Malabar legs "by river and by sea", so a straight line
between two candidates is not the quantity the text is reporting. Nobody has
measured these distances through the waterways, which is the gap CLAUDE.md calls
the single most consequential unfinished measurement.

The honest limitation, stated up front: the network used here is the modern one
from the JRC Landsat record. The 1341 cyclone reorganised the Vembanad, and
Gurukkal and Whittaker regard the result as not reconstructible. So these are
not first-century distances. They are the first measurement of what the text
describes through any real water network, and they establish by how much a
routed distance differs from the straight line everyone has used instead.
"""

import heapq
import numpy as np
from pyproj import Geod

GEOD = Geod(ellps="WGS84")

# Eight-connectivity, with the diagonals costing their true length.
NEIGHBOURS = [(-1, 0, 1.0), (1, 0, 1.0), (0, -1, 1.0), (0, 1, 1.0),
              (-1, -1, 2 ** 0.5), (-1, 1, 2 ** 0.5),
              (1, -1, 2 ** 0.5), (1, 1, 2 ** 0.5)]


def pixel_km(bbox, shape):
    """Mean north-south and east-west pixel size, in km."""
    lat0, lat1 = bbox[1], bbox[3]
    lon0, lon1 = bbox[0], bbox[2]
    _, _, ew = GEOD.inv(lon0, (lat0 + lat1) / 2, lon1, (lat0 + lat1) / 2)
    _, _, ns = GEOD.inv((lon0 + lon1) / 2, lat0, (lon0 + lon1) / 2, lat1)
    return 0.5 * (ew / 1000 / shape[1] + ns / 1000 / shape[0])


def to_rc(lon, lat, bbox, shape):
    """Geographic coordinate to (row, col) on a regular lon/lat grid."""
    c = (lon - bbox[0]) / (bbox[2] - bbox[0]) * shape[1]
    r = (bbox[3] - lat) / (bbox[3] - bbox[1]) * shape[0]
    return int(round(r)), int(round(c))


def nearest_water(mask, rc, max_radius=200):
    """The closest navigable pixel to a point, since a port sits on the bank
    rather than in the channel. Returns None if nothing is within max_radius."""
    r0, c0 = rc
    h, w = mask.shape
    if 0 <= r0 < h and 0 <= c0 < w and mask[r0, c0]:
        return (r0, c0)
    for rad in range(1, max_radius):
        r1, r2 = max(0, r0 - rad), min(h, r0 + rad + 1)
        c1, c2 = max(0, c0 - rad), min(w, c0 + rad + 1)
        sub = mask[r1:r2, c1:c2]
        if not sub.any():
            continue
        rr, cc = np.nonzero(sub)
        d = (rr + r1 - r0) ** 2 + (cc + c1 - c0) ** 2
        i = int(np.argmin(d))
        return (int(rr[i] + r1), int(cc[i] + c1))
    return None


def shortest_path(mask, start, goal, km_per_px):
    """Dijkstra over the navigable mask. Returns (distance_km, path).

    A* would be faster, but the network is small and a plain uniform-cost search
    has no heuristic to get wrong.
    """
    h, w = mask.shape
    dist = np.full(mask.shape, np.inf, dtype="float64")
    prev = {}
    dist[start] = 0.0
    pq = [(0.0, start)]
    while pq:
        d, (r, c) = heapq.heappop(pq)
        if (r, c) == goal:
            break
        if d > dist[r, c]:
            continue
        for dr, dc, step in NEIGHBOURS:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < h and 0 <= nc < w) or not mask[nr, nc]:
                continue
            nd = d + step
            if nd < dist[nr, nc]:
                dist[nr, nc] = nd
                prev[(nr, nc)] = (r, c)
                heapq.heappush(pq, (nd, (nr, nc)))

    if not np.isfinite(dist[goal]):
        return None, None
    path, node = [goal], goal
    while node != start:
        node = prev[node]
        path.append(node)
    return float(dist[goal] * km_per_px), path[::-1]


def straight_km(a, b):
    """Great-circle distance between two (lon, lat) points, in km."""
    _, _, m = GEOD.inv(a[0], a[1], b[0], b[1])
    return m / 1000.0

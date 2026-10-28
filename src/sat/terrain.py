"""Terrain visualisations that make a shallow channel visible, and a fair test of them.

The project detrended a 30 m DEM, scored 0.43 to 0.54, and concluded that
terrain cannot contribute because a channel is one to two metres deep and
detrending leaves a residual standard deviation of 1.2 to 4.7 m. That diagnosis
blamed the resolution. It may have been blaming the wrong thing, because
detrending is the crudest filter available and the geoarchaeological literature
does not use it.

What that literature uses is sky-view factor, reported as "effective in the
discrimination and visualisation of palaeochannels, especially when preceded by
trend removal", and openness, which unlike hillshade has no directional bias and
shifts no feature sideways. Both ask a different question from detrending. A
detrended residual asks how high this pixel is relative to its surroundings. Sky
-view factor asks how much sky it can see, which for a shallow trough is a
sharper question: the floor of a 1 m channel sees measurably less sky than the
bank beside it even when both sit on the same regional slope.

Implementations follow Zakšek, Oštir and Kokalj for sky-view factor and Yokoyama
for openness. The search radius is the one parameter that matters and it is set
to the feature width being hunted, since a radius much larger than the channel
generalises it away.
"""
import numpy as np
from scipy import ndimage


def _horizon_angles(dem, pixel_m, radius_px, n_dir=16):
    """Maximum elevation angle to the horizon, per pixel, per direction.

    Walks outward one step at a time along each azimuth, shifting the whole
    array rather than looping over pixels, which is what makes this tractable
    on a 2,500 square grid in numpy.
    """
    H, W = dem.shape
    out = np.full((n_dir, H, W), -np.pi / 2, dtype="float32")
    for k in range(n_dir):
        az = 2 * np.pi * k / n_dir
        dy, dx = -np.cos(az), np.sin(az)
        best = np.full((H, W), -np.pi / 2, dtype="float32")
        for r in range(1, radius_px + 1):
            sy, sx = int(round(dy * r)), int(round(dx * r))
            if sy == 0 and sx == 0:
                continue
            shifted = np.roll(np.roll(dem, -sy, axis=0), -sx, axis=1)
            # edges wrap under roll, so blank the wrapped band
            if sy > 0:
                shifted[-sy:, :] = np.nan
            elif sy < 0:
                shifted[:-sy, :] = np.nan
            if sx > 0:
                shifted[:, -sx:] = np.nan
            elif sx < 0:
                shifted[:, :-sx] = np.nan
            dist = np.hypot(sy, sx) * pixel_m
            with np.errstate(invalid="ignore"):
                ang = np.arctan2(shifted - dem, dist)
            best = np.fmax(best, np.nan_to_num(ang, nan=-np.pi / 2))
        out[k] = best
    return out


def sky_view_factor(dem, pixel_m=30.0, radius_px=20, n_dir=16):
    """Proportion of the sky hemisphere visible from each pixel, 0 to 1.

    A trough sees less sky than its banks, so a channel reads low. This is the
    quantity the lidar literature reports as effective for palaeochannels.
    """
    h = _horizon_angles(dem, pixel_m, radius_px, n_dir)
    return np.mean(1.0 - np.sin(np.clip(h, 0, np.pi / 2)), axis=0).astype("float32")


def openness(dem, pixel_m=30.0, radius_px=20, n_dir=16, positive=True):
    """Mean zenith angle to the horizon, in radians.

    Positive openness is large where a pixel is exposed and small where it is
    enclosed, so a channel floor reads low and a levee reads high. Negative
    openness is the same computed downward and picks out convex features
    instead, which is why the two are usually read together.
    """
    d = dem if positive else -dem
    h = _horizon_angles(d, pixel_m, radius_px, n_dir)
    return np.mean(np.pi / 2 - h, axis=0).astype("float32")


def local_relief(dem, kernel_px=25):
    """The classic local relief model: elevation minus a smoothed surface.

    This is what the project already did, kept here so the comparison is
    like for like rather than against a remembered number.
    """
    sm = ndimage.uniform_filter(np.nan_to_num(dem, nan=float(np.nanmean(dem))),
                                size=kernel_px)
    return (dem - sm).astype("float32")


def detrend(dem, sigma=40):
    """Gaussian high-pass, the filter the earlier terrain test used."""
    base = np.nan_to_num(dem, nan=float(np.nanmean(dem)))
    return (dem - ndimage.gaussian_filter(base, sigma)).astype("float32")


def suite(dem, pixel_m=30.0, channel_width_m=600):
    """Every visualisation, with the radius set from the channel width sought.

    Returns scores oriented so that larger means more channel-like: sky-view
    factor and openness are negated, since a channel is a trough and reads low
    in both.
    """
    r = max(3, int(round(channel_width_m / pixel_m)))
    return {
        "neg_sky_view_factor": -sky_view_factor(dem, pixel_m, r),
        "neg_openness": -openness(dem, pixel_m, r),
        "neg_local_relief": -local_relief(dem, kernel_px=2 * r + 1),
        "neg_detrend": -detrend(dem, sigma=max(5, r * 2)),
    }

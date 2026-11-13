# The fine-scale relief term of model F (bathymetry_1857.ipynb, section 8b; validation_bathymetry.ipynb).
#
# A survey with soundings ~250 m apart cannot resolve channels and shoals narrower than that, and a single
# stationary Matern field with an estimated nugget puts that relief into "measurement noise". The seabed
# surface it returns is then too smooth and its intervals too narrow, worst at the river mouth.
#
# Model F adds a second Matern field u2 with unit variance and fixed range, multiplied by a known weight
# w(s), an sd in metres that is largest at the mouth and along the shore:
#
#   w(s)^2 = a_mouth^2 exp(-2 d_mouth / L_mouth) + a_shore^2 exp(-2 d_shore / L_shore) + a_floor^2
#
# The sparse soundings cannot estimate w (an estimated version shrinks to zero), so it is fixed from a
# fully surveyed modern analogue: the relief that a 250 m smoothing removes from the NOAA CUDEM seabed at
# San Luis Pass, Texas (0.9 m within 1 km of the pass, 0.4-0.5 m in the next km and along the shore,
# 0.15 m offshore), then rebalanced once so that 90% intervals cover about 90% of the true seabed there.
# It was then frozen and tested on Pass Cavallo, Texas, which played no part in choosing it.
# The observation noise is fixed at the measurement-error budget rather than estimated.

FS_PAR <- list(range = 0.3,                 # km, range of u2: the scale a 250 m survey misses
               a_mouth = 1.6, L_mouth = 1.5, # m, km
               a_shore = 0.45, L_shore = 0.7,
               a_floor = 0.15)

fs_weight <- function(x, y, dist, mouth, p = FS_PAR) {
  dm <- sqrt((x - mouth[1])^2 + (y - mouth[2])^2)
  sqrt(p$a_mouth^2 * exp(-2 * dm / p$L_mouth) + p$a_shore^2 * exp(-2 * dist / p$L_shore) + p$a_floor^2)
}

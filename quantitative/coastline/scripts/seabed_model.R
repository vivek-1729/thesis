# Model F at one candidate mouth: the near-shore seabed model of bathymetry_1857.ipynb (section 8b), validated
# against two fully surveyed inlets in validation_bathymetry.ipynb.
#
#   depth(s) = b0 + b1 d(s) + b2 (1 - exp(-d(s)/0.1)) + u(s) + w(s) v(s) + noise
#
#   d      distance to the charted coast (km)
#   u      Matern field, PC priors P(range < 0.3 km) = 0.1, P(sd > 5 m) = 0.1
#   v      fine-scale Matern field, unit sd, range 0.3 km, both fixed; w(s) from scripts/fine_scale.R
#          (the mouth term is switched off where the site has no river or lagoon entrance)
#   noise  sd fixed at the measurement-error budget, 0.4 m (lead line, quarter-fathom rounding, tide reduction)
#   shoreline anchors at -0.46 m (half the 0.91 m spring rise, the high-water coast against a low-water datum),
#   sd 1 m, as a second Gaussian likelihood
#
# Mesh: 150 m edges within 3 km of the coast (and in the water just landward), 600 m elsewhere; shoreline
# anchors every 100 m are mesh vertices. Hyperparameters at their posterior mode (int.strategy = "eb").
#
# fit_site(dir) reads the inputs written by seabed_inputs.py and writes, to the same folder:
#   samples.bin     200 joint posterior draws of the seabed (no observation noise) at every grid cell, float32,
#                   cell-major (cells x draws)
#   fit.json        fixed effects, hyperparameters, mesh size, run time

suppressMessages({library(INLA); library(fmesher); library(sf); library(Matrix); library(jsonlite)})

seabed_fit_site <- function(dir, fs_r, noise = 0.4, n_draws = 200) {
  t0 <- Sys.time(); D <- paste0(dir, "/")
  source(fs_r, local = TRUE)                      # FS_PAR, fs_weight()
  rg <- function(f) { g <- st_read(paste0(D, f), quiet = TRUE); st_crs(g) <- NA; g }
  dom <- rg("domain.geojson"); land <- rg("land.geojson")
  snd <- read.csv(paste0(D, "soundings.csv")); shore <- read.csv(paste0(D, "shore.csv")); grid <- read.csv(paste0(D, "grid.csv"))
  meta <- fromJSON(paste0(D, "site.json"))
  par <- FS_PAR; mouth <- if (is.null(meta$mouth)) c(0, 0) else unlist(meta$mouth)
  if (is.null(meta$mouth)) par$a_mouth <- 0
  w <- function(x, y, d) fs_weight(x, y, d, mouth, par)

  water <- st_difference(st_geometry(dom), st_geometry(land))
  coast_zone <- st_buffer(st_union(st_as_sf(shore, coords = c("x_km", "y_km"))), 3)
  inner <- st_intersection(st_intersection(st_buffer(water, 0.25), coast_zone), st_geometry(dom))
  mesh <- fm_mesh_2d_inla(loc = as.matrix(shore[seq(1, nrow(shore), 2), 1:2]),
                          boundary = list(inner, st_buffer(st_geometry(dom), 0.5)), max.edge = c(0.15, 0.6), cutoff = 0.05)

  spde  <- inla.spde2.pcmatern(mesh, prior.range = c(0.3, 0.1), prior.sigma = c(5, 0.1))
  spde2 <- inla.spde2.pcmatern(mesh, prior.range = c(par$range, NA), prior.sigma = c(1, NA))
  As <- fm_basis(mesh, as.matrix(snd[, c("x_km", "y_km")])); Aa <- fm_basis(mesh, as.matrix(shore[, 1:2]))
  ws <- w(snd$x_km, snd$y_km, snd$dist_km); wa <- w(shore$x_km, shore$y_km, 0)
  stk <- inla.stack(
    inla.stack(data = list(Y = cbind(snd$depth_m, NA)), tag = "snd", A = list(As, Diagonal(x = ws) %*% As, 1),
               effects = list(field = 1:mesh$n, fine = 1:mesh$n,
                              data.frame(b0 = 1, dist = snd$dist_km, beach = 1 - exp(-snd$dist_km / 0.1)))),
    inla.stack(data = list(Y = cbind(rep(NA, nrow(shore)), rep(-0.46, nrow(shore)))), tag = "shore",
               A = list(Aa, Diagonal(x = wa) %*% Aa, 1),
               effects = list(field = 1:mesh$n, fine = 1:mesh$n, data.frame(b0 = rep(1, nrow(shore)), dist = 0, beach = 0))))
  f <- suppressWarnings(inla(Y ~ 0 + b0 + dist + beach + f(field, model = spde) + f(fine, model = spde2),
         family = c("gaussian", "gaussian"), data = inla.stack.data(stk),
         control.family = list(list(hyper = list(prec = list(initial = log(1 / noise^2), fixed = TRUE))),
                               list(hyper = list(prec = list(initial = 0, fixed = TRUE)))),
         control.predictor = list(A = inla.stack.A(stk)), control.compute = list(config = TRUE),
         control.inla = list(int.strategy = "eb")))

  smp <- inla.posterior.sample(n_draws, f, selection = list(field = 1:mesh$n, fine = 1:mesh$n, b0 = 1, dist = 1, beach = 1))
  rn <- rownames(smp[[1]]$latent); i1 <- grep("^field:", rn); i2 <- grep("^fine:", rn)
  ib <- match(c("b0:1", "dist:1", "beach:1"), rn)
  Ag <- fm_basis(mesh, as.matrix(grid[, c("x_km", "y_km")])); wg <- w(grid$x_km, grid$y_km, grid$dist_km)
  bg <- 1 - exp(-grid$dist_km / 0.1)
  S <- sapply(smp, function(z) { l <- z$latent[, 1]
    as.vector(Ag %*% l[i1]) + wg * as.vector(Ag %*% l[i2]) + l[ib[1]] + l[ib[2]] * grid$dist_km + l[ib[3]] * bg })
  writeBin(as.vector(t(S)), paste0(D, "samples.bin"), size = 4)      # cell-major: cells x draws

  fx <- f$summary.fixed[, c("mean", "0.025quant", "0.975quant")]
  out <- list(site = meta$site, mesh_nodes = mesh$n, n_soundings = nrow(snd), n_cells = nrow(grid), n_draws = n_draws,
              noise_sd = noise, mouth_term = !is.null(meta$mouth),
              fixed = setNames(lapply(rownames(fx), function(r) as.list(fx[r, ])), rownames(fx)),
              hyper = as.list(setNames(f$summary.hyperpar$mean, rownames(f$summary.hyperpar))),
              seconds = round(as.numeric(Sys.time() - t0, units = "secs")))
  write_json(out, paste0(D, "fit.json"), auto_unbox = TRUE, digits = 6, pretty = TRUE)
  invisible(out)
}

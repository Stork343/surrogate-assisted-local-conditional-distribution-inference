#!/usr/bin/env Rscript

# Reproducible real-data benchmark using the EPA long-term air-sensor study.

args <- commandArgs(trailingOnly = TRUE)
arg_value <- function(flag, default) {
  hit <- grep(paste0("^", flag, "="), args, value = TRUE)
  if (!length(hit)) return(default)
  sub(paste0("^", flag, "="), "", hit[[1L]])
}

root <- normalizePath(if (file.exists("DESCRIPTION")) "." else "..")
n_rep <- as.integer(arg_value("--reps", "500"))
cores <- as.integer(arg_value(
  "--cores", as.character(max(1L, min(4L, parallel::detectCores() - 1L)))
))
force_data <- identical(arg_value("--force-data", "false"), "true")
if (!is.finite(n_rep) || n_rep < 1L) stop("--reps must be positive.")
if (!is.finite(cores) || cores < 1L) stop("--cores must be positive.")

invisible(lapply(
  list.files(file.path(root, "R"), pattern = "[.]R$", full.names = TRUE),
  source
))
source(file.path(root, "simulation", "config", "simulation_constants.R"))
source(file.path(root, "simulation", "R", "borrowing_estimators.R"))
source(file.path(root, "analysis", "public_application_helpers.R"))

out_dir <- file.path(root, "analysis", "output", "public_application")
fig_dir <- file.path(out_dir, "figures")
table_dir <- file.path(out_dir, "tables")
dir.create(fig_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)

csv_path <- acquire_epa_processed_data(root, force = force_data)
data <- make_epa_site_day_data(csv_path, make_id = "PAR")
tau <- seq(
  unname(quantile(data$y, 0.01)),
  unname(quantile(data$y, 0.99)),
  length.out = 101L
)
h <- 0.5
seed_base <- 20260813L

cells <- expand.grid(
  p = c(0.05, 0.10, 0.20),
  design = c("random", "selective"),
  x0 = c(-1, 0, 1),
  replicate = seq_len(n_rep),
  stringsAsFactors = FALSE
)

worker <- function(i) {
  z <- cells[i, ]
  fit_one_epa_mask(
    data = data, tau = tau, x0 = z$x0, h = h, p = z$p,
    design = z$design, replicate = z$replicate,
    seed_base = seed_base, return_u = FALSE
  )$metrics
}

message("Running ", nrow(cells), " EPA reference-subsampling cells on ",
        cores, " core(s).")
if (cores == 1L || .Platform$OS.type == "windows") {
  results <- lapply(seq_len(nrow(cells)), worker)
} else {
  results <- parallel::mclapply(
    seq_len(nrow(cells)), worker, mc.cores = cores, mc.preschedule = TRUE
  )
}
metrics <- do.call(rbind, results)
metrics$implementation_version <- simulation_implementation_version
summary_table <- summarize_epa_metrics(metrics)

anchor <- summary_table[summary_table$method == "X_anchor",
                        c("p", "design", "x0", "mean_ise")]
names(anchor)[4L] <- "anchor_mean_ise"
summary_table <- merge(
  summary_table, anchor, by = c("p", "design", "x0"),
  all.x = TRUE, sort = FALSE
)
summary_table$gain_vs_anchor_pct <-
  100 * (summary_table$anchor_mean_ise - summary_table$mean_ise) /
  summary_table$anchor_mean_ise
summary_table <- summary_table[
  order(summary_table$design, summary_table$p, summary_table$x0,
        summary_table$method),
]
rownames(summary_table) <- NULL

write.csv(metrics, file.path(out_dir, "replicate_metrics.csv"),
          row.names = FALSE)
write.csv(summary_table, file.path(out_dir, "method_summary.csv"),
          row.names = FALSE)
saveRDS(
  list(
    implementation_version = simulation_implementation_version,
    data = data, tau = tau, h = h, cells = cells, metrics = metrics,
    summary = summary_table, seed_base = seed_base,
    archive_sha256 = epa_processed_sha256
  ),
  file.path(out_dir, "epa_public_application.rds")
)

site_rows <- lapply(split(data, data$Location), function(z) {
  data.frame(
    location = z$Location[1L], n_site_days = nrow(z),
    start_date = min(z$date), end_date = max(z$date),
    pearson = cor(z$PM25_Ref, z$PM25_sens),
    spearman = cor(z$PM25_Ref, z$PM25_sens, method = "spearman"),
    median_reference = median(z$PM25_Ref),
    p95_reference = unname(quantile(z$PM25_Ref, 0.95)),
    median_sensor_rh = median(z$RH_sens),
    stringsAsFactors = FALSE
  )
})
site_summary <- do.call(rbind, site_rows)
rownames(site_summary) <- NULL
write.csv(site_summary, file.path(out_dir, "site_summary.csv"),
          row.names = FALSE)

time_breaks <- quantile(as.numeric(data$date), seq(0, 1, length.out = 5))
period <- cut(
  as.numeric(data$date),
  breaks = time_breaks,
  include.lowest = TRUE, labels = paste0("Q", 1:4)
)
data$period <- period
drift_rows <- lapply(split(data, interaction(data$Location, data$period)), function(z) {
  if (nrow(z) < 20L) return(NULL)
  fit <- lm(y ~ s, data = z)
  data.frame(
    location = z$Location[1L], period = as.character(z$period[1L]),
    n = nrow(z), start_date = min(z$date), end_date = max(z$date),
    pearson = cor(z$PM25_Ref, z$PM25_sens),
    spearman = cor(z$PM25_Ref, z$PM25_sens, method = "spearman"),
    calibration_slope = unname(coef(fit)[2L]),
    mean_bias = mean(z$PM25_sens - z$PM25_Ref),
    stringsAsFactors = FALSE
  )
})
drift_summary <- do.call(rbind, drift_rows)
rownames(drift_summary) <- NULL
write.csv(drift_summary, file.path(out_dir, "temporal_drift.csv"),
          row.names = FALSE)

example_cells <- expand.grid(
  x0 = c(-1, 0, 1), method = c("X_anchor", "Adaptive"),
  stringsAsFactors = FALSE
)
band_rows <- vector("list", nrow(example_cells))
example_fits <- vector("list", 3L)
for (j in seq_along(example_fits)) {
  x0 <- c(-1, 0, 1)[j]
  example_fits[[j]] <- fit_one_epa_mask(
    data, tau, x0, h, p = 0.10, design = "random", replicate = 1L,
    seed_base = seed_base, return_u = TRUE
  )
  for (nm in c("X_anchor", "Adaptive")) {
    band <- cluster_multiplier_band(
      example_fits[[j]]$influence[[nm]],
      example_fits[[j]]$estimates[[nm]], data, h,
      example_fits[[j]]$pi,
      n_boot = 999L, seed = seed_base + j + match(nm, c("X_anchor", "Adaptive"))
    )
    cover <- example_fits[[j]]$truth >= band$low &
      example_fits[[j]]$truth <= band$high
    idx <- which(example_cells$x0 == x0 & example_cells$method == nm)
    band_rows[[idx]] <- data.frame(
      x0 = x0, rh_target = 50 + 20 * x0, method = nm,
      simultaneous_coverage = all(cover),
      pointwise_coverage = mean(cover),
      integrated_band_width = band$integrated_width,
      critical_value = band$critical_value,
      clusters = band$clusters,
      lambda_hat = example_fits[[j]]$lambda_hat,
      full_transfer_signal = example_fits[[j]]$full_transfer_signal,
      stringsAsFactors = FALSE
    )
  }
}
band_summary <- do.call(rbind, band_rows)
write.csv(band_summary, file.path(out_dir, "example_bands.csv"),
          row.names = FALSE)

main_plot <- summary_table[
  summary_table$design == "random" &
    summary_table$method %in% c("X_anchor", "Full", "Adaptive"),
]
png(file.path(fig_dir, "fig_epa_ise.png"), width = 1800, height = 1000,
    res = 180)
op <- par(mfrow = c(1, 3), mar = c(4.2, 4.5, 3, 1), las = 1)
on.exit(par(op), add = TRUE)
cols <- c(X_anchor = "#333333", Full = "#D55E00", Adaptive = "#0072B2")
pch <- c(X_anchor = 16, Full = 17, Adaptive = 15)
for (rh in c(30, 50, 70)) {
  z <- main_plot[main_plot$rh_target == rh, ]
  plot(range(z$p), range(z$mean_ise), log = "y", type = "n",
       xlab = "Reference fraction", ylab = "Mean integrated squared error",
       main = paste0("Target RH = ", rh, "%"))
  for (nm in names(cols)) {
    zz <- z[z$method == nm, ]
    lines(zz$p, zz$mean_ise, col = cols[nm], pch = pch[nm],
          type = "b", lwd = 2)
  }
  if (rh == 30) legend("topright", names(cols), col = cols, pch = pch,
                       lwd = 2, bty = "n")
}
dev.off()

png(file.path(fig_dir, "fig_epa_cdf.png"), width = 1800, height = 1000,
    res = 180)
op2 <- par(mfrow = c(1, 3), mar = c(4.2, 4.5, 3, 1), las = 1)
for (j in seq_along(example_fits)) {
  fit <- example_fits[[j]]
  x_axis <- expm1(tau)
  plot(x_axis, fit$truth, type = "l", lwd = 3, col = "black",
       xlab = expression(PM[2.5] ~ (mu * g / m^3)), ylab = "Local CDF",
       main = paste0("Target RH = ", 50 + 20 * c(-1, 0, 1)[j], "%"),
       ylim = c(0, 1))
  lines(x_axis, salcdi_monotone_cdf(pmin(pmax(fit$estimates$X_anchor, 0), 1)),
        col = cols["X_anchor"], lwd = 2, lty = 2)
  lines(x_axis, salcdi_monotone_cdf(pmin(pmax(fit$estimates$Adaptive, 0), 1)),
        col = cols["Adaptive"], lwd = 2)
  if (j == 1L) legend(
    "bottomright", c("Complete benchmark", "X-anchor", "Adaptive"),
    col = c("black", cols["X_anchor"], cols["Adaptive"]),
    lty = c(1, 2, 1), lwd = c(3, 2, 2), bty = "n"
  )
}
dev.off()

main_table <- summary_table[
  summary_table$design == "random" & summary_table$p == 0.10 &
    summary_table$method %in% c("X_anchor", "Full", "Adaptive"),
  c("rh_target", "method", "mean_ise", "mcse_ise", "gain_vs_anchor_pct",
    "mean_lambda", "mean_full_transfer_signal", "negative_transfer_rate")
]
write.csv(main_table, file.path(table_dir, "table_epa_primary.csv"),
          row.names = FALSE)

session <- c(
  paste("Run date:", format(Sys.time(), tz = "UTC", usetz = TRUE)),
  paste("Command args:", paste(args, collapse = " ")),
  paste("Archive SHA-256:", epa_processed_sha256),
  capture.output(sessionInfo())
)
writeLines(session, file.path(out_dir, "session_info.txt"))
message("EPA public application complete: ", out_dir)

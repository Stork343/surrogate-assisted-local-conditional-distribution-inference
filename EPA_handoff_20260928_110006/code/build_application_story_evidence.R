# Build descriptive and repeated-sampling evidence for the three Section 5 studies.
# This script reads frozen data and canonical result objects. It does not rerun
# an estimator, draw a new reference mask, or call an external model.

args <- commandArgs(trailingOnly = TRUE)
root <- if (length(args)) normalizePath(args[[1L]]) else normalizePath(".")
out_dir <- file.path(root, "reproducibility", "application_story")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

if (!requireNamespace("digest", quietly = TRUE)) stop("Package digest is required.")
if (!requireNamespace("jsonlite", quietly = TRUE)) stop("Package jsonlite is required.")

hash_file <- function(path) {
  digest::digest(file = path, algo = "sha256", serialize = FALSE)
}

write_csv <- function(x, name) {
  path <- file.path(out_dir, name)
  utils::write.csv(x, path, row.names = FALSE, na = "")
  path
}

epanechnikov_cdf <- function(x, y, x0, h, thresholds) {
  u <- (x - x0) / h
  w <- 0.75 * (1 - u^2) * (abs(u) <= 1)
  if (!all(is.finite(w)) || sum(w) <= 0) stop("Invalid localized CDF weights.")
  vapply(thresholds, function(t) sum(w * (y <= t)) / sum(w), numeric(1L))
}

paired_ratio <- function(path, method) {
  x <- readRDS(path)
  keep <- x$method %in% c("X_anchor", method)
  x <- x[keep, c("seed", "method", "ise"), drop = FALSE]
  if (anyNA(x$seed) || anyNA(x$ise)) stop("Missing pairing key or ISE in ", path)
  if (anyDuplicated(x[c("seed", "method")])) stop("Duplicate paired row in ", path)
  wide <- reshape(x, idvar = "seed", timevar = "method", direction = "wide")
  anchor <- wide$ise.X_anchor
  candidate <- wide[[paste0("ise.", method)]]
  if (length(anchor) != 2000L || any(!is.finite(anchor)) || any(anchor <= 0)) {
    stop("Unexpected paired sample in ", path)
  }
  difference <- anchor - candidate
  dbar <- mean(difference)
  dse <- stats::sd(difference) / sqrt(length(difference))
  z <- stats::qnorm(0.975)
  anchor_mean <- mean(anchor)
  candidate_mean <- mean(candidate)
  data.frame(
    method = method,
    replications = length(anchor),
    anchor_mean_ise = anchor_mean,
    method_mean_ise = candidate_mean,
    relative_risk = candidate_mean / anchor_mean,
    relative_risk_low = 1 - (dbar + z * dse) / anchor_mean,
    relative_risk_high = 1 - (dbar - z * dse) / anchor_mean,
    paired_difference_mcse = dse,
    stringsAsFactors = FALSE
  )
}

# EPA: real long-term collocation data and its controlled reference-sampling study.
epa_path <- file.path(root, "analysis", "output", "public_application",
                      "epa_public_application.rds")
epa <- readRDS(epa_path)
stopifnot(identical(epa$implementation_version, "salcdi-canonical-p0d-v2"))
stopifnot(nrow(epa$data) == 2814L, length(epa$tau) == 101L, epa$h == 0.5)

epa_calibration <- data.frame(
  observation_id = seq_len(nrow(epa$data)),
  reference_log_pm25 = epa$data$y,
  surrogate_log_pm25 = epa$data$s,
  relative_humidity = epa$data$x_raw,
  site = epa$data$Location,
  stringsAsFactors = FALSE
)
epa_calibration_path <- write_csv(epa_calibration, "epa_calibration_points.csv")

epa_targets <- data.frame(
  x0 = c(-1, 0, 1), rh_target = c(30, 50, 70),
  target_label = c("30% RH", "50% RH", "70% RH"),
  stringsAsFactors = FALSE
)
epa_local_cdf <- do.call(rbind, lapply(seq_len(nrow(epa_targets)), function(j) {
  data.frame(
    rh_target = epa_targets$rh_target[j],
    target_label = epa_targets$target_label[j],
    threshold_log = epa$tau,
    threshold_raw = expm1(epa$tau),
    localized_cdf = epanechnikov_cdf(
      epa$data$x, epa$data$y, epa_targets$x0[j], epa$h, epa$tau
    ),
    stringsAsFactors = FALSE
  )
}))
epa_local_cdf_path <- write_csv(epa_local_cdf, "epa_complete_data_local_cdf.csv")

frontier_path <- file.path(root, "reproducibility", "machine_tables",
                           "figure3_application_frontiers.csv")
frontier <- utils::read.csv(frontier_path, check.names = FALSE)
epa_frontier <- frontier[frontier$application == "EPA", , drop = FALSE]
stopifnot(nrow(epa_frontier) == 9L, all(epa_frontier$relative_risk_high < 1))
epa_frontier_path <- write_csv(epa_frontier, "epa_risk_frontier.csv")

# VitalDB: real paired intraoperative reference and pulse-oximetry measurements.
vital_path <- file.path(root, "analysis", "output", "vitaldb_application",
                        "vitaldb_application.rds")
vital <- readRDS(vital_path)
stopifnot(identical(vital$implementation_version, "salcdi-canonical-p0d-v2"))
stopifnot(nrow(vital$data) == 3178L, identical(vital$tau, 70:99), vital$h == 0.55)

vital_pair_counts <- stats::aggregate(
  rep(1L, nrow(vital$data)),
  by = list(sao2 = vital$data$y, spo2 = vital$data$s), FUN = sum
)
names(vital_pair_counts)[3L] <- "count"
vital_pair_counts <- vital_pair_counts[order(vital_pair_counts$sao2,
                                             vital_pair_counts$spo2), ]
vital_pair_counts_path <- write_csv(vital_pair_counts, "vitaldb_pair_counts.csv")

vital_targets <- data.frame(
  target_minutes = c(30, 75, 180),
  target_label = c("30 min", "75 min", "180 min"),
  stringsAsFactors = FALSE
)
vital_local_cdf <- do.call(rbind, lapply(seq_len(nrow(vital_targets)), function(j) {
  x0 <- log1p(vital_targets$target_minutes[j])
  data.frame(
    target_minutes = vital_targets$target_minutes[j],
    target_label = vital_targets$target_label[j],
    threshold = vital$tau,
    localized_cdf = epanechnikov_cdf(
      vital$data$x, vital$data$y, x0, vital$h, vital$tau
    ),
    stringsAsFactors = FALSE
  )
}))
vital_local_cdf_path <- write_csv(vital_local_cdf, "vitaldb_complete_data_local_cdf.csv")

vital_frontier <- frontier[frontier$application == "VitalDB", , drop = FALSE]
stopifnot(nrow(vital_frontier) == 12L, all(vital_frontier$relative_risk_high < 1))
vital_frontier_path <- write_csv(vital_frontier, "vitaldb_risk_frontier.csv")

# Controlled synthetic AI review benchmark: frozen dossiers, expert outcomes,
# and API scores. Protected dossier text and identifiers are not exported.
ai_evidence_path <- file.path(root, "simulation", "ai_expert", "corpus",
                             "evidence", "corpus_A_evidence.rds")
ai_truth_path <- file.path(root, "simulation", "ai_expert", "corpus", "truth",
                          "corpus_A_truth.rds")
ai_scores_path <- file.path(root, "simulation", "ai_expert", "results", "raw",
                           "ai_scores_primary_corpusA.csv")
ai_evidence_obj <- readRDS(ai_evidence_path)
ai_truth_obj <- readRDS(ai_truth_path)
ai_scores <- utils::read.csv(ai_scores_path, stringsAsFactors = FALSE)
stopifnot(identical(ai_truth_obj$reference_version, "fixed-expert-bias-v2"))

ai_data <- merge(ai_evidence_obj$data[, c("case_id", "X")],
                 ai_truth_obj$data[, c("case_id", "Y")], by = "case_id")
ai_data <- merge(ai_data,
                 ai_scores[, c("case_id", "parsed_score", "parsed_confidence",
                               "api_failure")], by = "case_id")
ai_data <- ai_data[!ai_data$api_failure & is.finite(ai_data$parsed_score), ]
stopifnot(nrow(ai_data) == 2998L, !anyDuplicated(ai_data$case_id))
ai_data$error <- ai_data$parsed_score - ai_data$Y

score_breaks <- seq(35, 100, length.out = 29L)
stopifnot(all(ai_data$Y >= min(score_breaks)),
          all(ai_data$Y <= max(score_breaks)),
          all(ai_data$parsed_score >= min(score_breaks)),
          all(ai_data$parsed_score <= max(score_breaks)))
ai_data$expert_bin <- cut(ai_data$Y, breaks = score_breaks,
                          include.lowest = TRUE, labels = FALSE)
ai_data$automated_bin <- cut(ai_data$parsed_score, breaks = score_breaks,
                             include.lowest = TRUE, labels = FALSE)
ai_calibration_bins <- stats::aggregate(
  rep(1L, nrow(ai_data)),
  by = list(expert_bin = ai_data$expert_bin,
            automated_bin = ai_data$automated_bin), FUN = sum
)
names(ai_calibration_bins)[3L] <- "count"
ai_calibration_bins$expert_mid <-
  (score_breaks[ai_calibration_bins$expert_bin] +
     score_breaks[ai_calibration_bins$expert_bin + 1L]) / 2
ai_calibration_bins$automated_mid <-
  (score_breaks[ai_calibration_bins$automated_bin] +
     score_breaks[ai_calibration_bins$automated_bin + 1L]) / 2
ai_calibration_bins$bin_width <- diff(score_breaks)[1L]
ai_calibration_bins <- ai_calibration_bins[
  order(ai_calibration_bins$expert_bin, ai_calibration_bins$automated_bin),
]
stopifnot(sum(ai_calibration_bins$count) == 2998L)
ai_calibration_path <- write_csv(ai_calibration_bins, "ai_calibration_bins.csv")

ai_calibration_summary <- data.frame(
  valid_scores = nrow(ai_data),
  score_correlation = stats::cor(ai_data$Y, ai_data$parsed_score),
  mean_absolute_error = mean(abs(ai_data$error)),
  stringsAsFactors = FALSE
)
ai_calibration_summary_path <- write_csv(
  ai_calibration_summary, "ai_calibration_summary.csv"
)

ai_breaks <- seq(-1, 1, length.out = 18L)
ai_data$complexity_bin <- cut(ai_data$X, breaks = ai_breaks,
                              include.lowest = TRUE, labels = FALSE)
ai_local_error <- do.call(rbind, lapply(seq_len(17L), function(j) {
  z <- ai_data[ai_data$complexity_bin == j, ]
  if (!nrow(z)) stop("Empty AI complexity bin ", j)
  data.frame(
    bin_id = j,
    complexity_midpoint = mean(ai_breaks[c(j, j + 1L)]),
    n = nrow(z),
    mean_bias = mean(z$error),
    median_error = stats::median(z$error),
    error_q10 = unname(stats::quantile(z$error, 0.10, type = 8L)),
    error_q90 = unname(stats::quantile(z$error, 0.90, type = 8L)),
    stringsAsFactors = FALSE
  )
}))
stopifnot(round(max(abs(ai_local_error$mean_bias)), 6) == 0.781638)
ai_local_error_path <- write_csv(ai_local_error, "ai_local_error_by_complexity.csv")

review_designs <- data.frame(
  design = paste0("V", 1:5),
  design_label = c("Random", "Confidence", "Low score", "Hybrid", "Locally reduced"),
  stringsAsFactors = FALSE
)
ai_review_p010 <- do.call(rbind, lapply(seq_len(nrow(review_designs)), function(j) {
  path <- file.path(root, "simulation", "ai_expert", "results", "raw",
                    sprintf("AI_A_%s_p0.100_mask2000.rds", review_designs$design[j]))
  out <- paired_ratio(path, "Adaptive")
  out$design <- review_designs$design[j]
  out$design_label <- review_designs$design_label[j]
  out$p <- 0.10
  out$source_path <- sub(paste0("^", root, "/"), "", path)
  out
}))
ai_review_p010$design_label <- factor(
  ai_review_p010$design_label, levels = review_designs$design_label
)
ai_review_p010_path <- write_csv(ai_review_p010, "ai_review_designs_p010.csv")

local_reversal_rows <- list()
idx <- 1L
for (p in c(0.05, 0.10, 0.20)) {
  path <- file.path(root, "simulation", "ai_expert", "results", "raw",
                    sprintf("AI_B_AI4_V5_p%.2f_mask2000.rds", p))
  for (method in c("Adaptive", "Full")) {
    out <- paired_ratio(path, method)
    out$p <- p
    out$source_path <- sub(paste0("^", root, "/"), "", path)
    local_reversal_rows[[idx]] <- out
    idx <- idx + 1L
  }
}
ai_local_reversal <- do.call(rbind, local_reversal_rows)
ai_local_reversal_path <- write_csv(ai_local_reversal, "ai_local_reversal_risk.csv")

# Source and output manifests.
ai_raw_inputs <- unique(c(as.character(ai_review_p010$source_path),
                          as.character(ai_local_reversal$source_path)))
input_paths <- c(
  epa_path, vital_path, frontier_path, ai_evidence_path, ai_truth_path,
  ai_scores_path, file.path(root, ai_raw_inputs)
)
input_paths <- unique(normalizePath(input_paths))
source_manifest <- data.frame(
  path = sub(paste0("^", root, "/"), "", input_paths),
  bytes = file.info(input_paths)$size,
  sha256 = vapply(input_paths, hash_file, character(1L)),
  stringsAsFactors = FALSE
)
source_manifest_path <- write_csv(source_manifest, "source_manifest.csv")

output_paths <- c(
  epa_calibration_path, epa_local_cdf_path, epa_frontier_path,
  vital_pair_counts_path, vital_local_cdf_path, vital_frontier_path,
  ai_calibration_path, ai_calibration_summary_path, ai_local_error_path,
  ai_review_p010_path,
  ai_local_reversal_path, source_manifest_path
)
artifact_manifest <- data.frame(
  path = sub(paste0("^", root, "/"), "", normalizePath(output_paths)),
  rows = vapply(output_paths, function(path) nrow(utils::read.csv(path)), integer(1L)),
  bytes = file.info(output_paths)$size,
  sha256 = vapply(output_paths, hash_file, character(1L)),
  stringsAsFactors = FALSE
)
artifact_manifest_path <- write_csv(artifact_manifest, "artifact_manifest.csv")

query_log <- list(
  created_at = format(Sys.time(), "%Y-%m-%dT%H:%M:%S%z"),
  source_commit = tryCatch(system2("git", c("rev-parse", "HEAD"), stdout = TRUE),
                           error = function(e) NA_character_),
  transformations = list(
    epa_calibration = "All 2,814 frozen site-days; log1p reference and PurpleAir values.",
    epa_local_cdf = "Complete-data Epanechnikov localized empirical CDFs at 30%, 50%, and 70% RH using h=0.5 on standardized RH.",
    vital_pair_counts = "All 3,178 frozen subject-level SaO2-SpO2 pairs aggregated by exact integer pair.",
    vital_local_cdf = "Complete-data Epanechnikov localized empirical CDFs at 30, 75, and 180 minutes on thresholds 70:99.",
    ai_calibration = "All 2,998 valid frozen Corpus-A score pairs aggregated to a fixed 28-by-28 score grid; no case-level expert outcome is exported.",
    ai_local_error = "Seventeen fixed equal-width complexity bins from -1 to 1; mean, median, and empirical 10th/90th error quantiles.",
    risk_frontiers = "Canonical Adaptive/Anchor mean ISE ratios and paired 95% Monte Carlo intervals.",
    ai_review_designs = "Paired Anchor-minus-Adaptive ISE contrasts over 2,000 common masks at p=0.10.",
    ai_local_reversal = "Paired method-to-Anchor ISE contrasts over 2,000 common masks for AI4/V5 at p=0.05, 0.10, and 0.20."
  )
)
jsonlite::write_json(query_log, file.path(out_dir, "query_log.json"),
                     auto_unbox = TRUE, pretty = TRUE)

cat("Built application-story evidence in", out_dir, "\n")

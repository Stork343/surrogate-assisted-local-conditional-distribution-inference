# Helpers for the EPA long-term air-sensor application.

epa_processed_url <- paste0(
  "https://pasteur.epa.gov/uploads/10.23719/1531918/",
  "FigureProcessedData.zip"
)

epa_processed_sha256 <-
  "da096a4953ed8878931fe791774b9ac057341e55e888cf603a265c235049d2f3"

file_sha256 <- function(path) {
  cmd <- if (Sys.info()[["sysname"]] == "Darwin") {
    c("-a", "256", path)
  } else {
    c("-a", "256", path)
  }
  out <- system2("shasum", cmd, stdout = TRUE)
  strsplit(out[[1L]], "[[:space:]]+")[[1L]][[1L]]
}

acquire_epa_processed_data <- function(root, force = FALSE) {
  raw_dir <- file.path(root, "data-raw", "epa_long_term")
  zip_path <- file.path(raw_dir, "FigureProcessedData.zip")
  csv_path <- file.path(
    raw_dir, "FigureProcessedData", "LTPPCleanDataset_12_10_24.csv"
  )
  dir.create(raw_dir, recursive = TRUE, showWarnings = FALSE)

  if (force || !file.exists(zip_path)) {
    tmp <- tempfile("epa-processed-", tmpdir = raw_dir, fileext = ".zip")
    on.exit(unlink(tmp), add = TRUE)
    download.file(epa_processed_url, tmp, mode = "wb", quiet = FALSE)
    if (!identical(file_sha256(tmp), epa_processed_sha256)) {
      stop("Downloaded EPA archive failed the SHA-256 check.", call. = FALSE)
    }
    if (!file.rename(tmp, zip_path)) {
      stop("Could not move the verified EPA archive into place.", call. = FALSE)
    }
  }
  observed_hash <- file_sha256(zip_path)
  if (!identical(observed_hash, epa_processed_sha256)) {
    stop("Existing EPA archive failed the SHA-256 check.", call. = FALSE)
  }
  if (force || !file.exists(csv_path)) {
    utils::unzip(zip_path, exdir = raw_dir)
  }
  if (!file.exists(csv_path)) {
    stop("EPA clean processed CSV was not found after extraction.", call. = FALSE)
  }
  csv_path
}

make_epa_site_day_data <- function(csv_path, make_id = "PAR") {
  raw <- read.csv(csv_path, check.names = FALSE, stringsAsFactors = FALSE)
  raw <- raw[raw$Make_ID == make_id, , drop = FALSE]
  raw$DateTime <- as.POSIXct(raw$DateTime, tz = "UTC")
  raw$date <- as.Date(raw$DateTime)
  vars <- c("PM25_Ref", "PM25_sens", "RH_sens")
  day <- aggregate(
    raw[vars],
    list(Location = raw$Location, date = raw$date),
    function(z) mean(z, na.rm = TRUE)
  )
  keep <- complete.cases(day[c("Location", "date", vars)]) &
    apply(day[vars], 1L, function(z) all(is.finite(z)))
  day <- day[keep, , drop = FALSE]
  if (make_id == "PAR") {
    day <- day[
      day$date >= as.Date("2019-07-22") & day$date <= as.Date("2021-01-01"),
      , drop = FALSE
    ]
  }
  day <- day[order(day$Location, day$date), , drop = FALSE]
  rownames(day) <- NULL
  day$y_raw <- day$PM25_Ref
  day$y <- log1p(pmax(day$PM25_Ref, 0))
  day$s_raw <- day$PM25_sens
  day$s <- log1p(pmax(day$PM25_sens, 0))
  day$x_raw <- day$RH_sens
  day$x <- (day$RH_sens - 50) / 20
  day$month <- format(day$date, "%Y-%m")
  day$week <- format(day$date - as.POSIXlt(day$date)$wday, "%Y-%m-%d")
  day$make_id <- make_id
  day
}

epanechnikov <- function(u) {
  0.75 * pmax(0, 1 - u^2) * (abs(u) <= 1)
}

make_cluster_folds <- function(cluster, seed, k = 3L) {
  groups <- unique(as.character(cluster))
  group_folds <- epa_with_mersenne_seed(seed, function() {
    sample(rep(seq_len(k), length.out = length(groups)))
  })
  group_folds[match(as.character(cluster), groups)]
}

# EPA masks and cluster folds were originally generated in a fresh R session
# under the Mersenne-Twister defaults.  Multiplier routines use L'Ecuyer-CMRG;
# without a local RNG scope, calling a multiplier first changes the meaning of
# the same integer EPA seed.  Preserve the frozen Mersenne stream and restore
# both the caller's RNG kind and state after every seeded operation.
epa_with_mersenne_seed <- function(seed, code) {
  if (!is.function(code)) {
    stop("`code` must be a function with no required arguments.", call. = FALSE)
  }
  old_kind <- RNGkind()
  had_seed <- exists(".Random.seed", envir = .GlobalEnv, inherits = FALSE)
  if (had_seed) {
    old_seed <- get(".Random.seed", envir = .GlobalEnv, inherits = FALSE)
  }
  on.exit({
    do.call(RNGkind, as.list(old_kind))
    if (had_seed) {
      assign(".Random.seed", old_seed, envir = .GlobalEnv)
    } else if (exists(".Random.seed", envir = .GlobalEnv, inherits = FALSE)) {
      rm(".Random.seed", envir = .GlobalEnv)
    }
  }, add = TRUE)
  set.seed(
    seed,
    kind = "Mersenne-Twister",
    normal.kind = "Inversion",
    sample.kind = "Rejection"
  )
  code()
}

gaussian_design_app <- function(x, s = NULL, include_s = FALSE) {
  x <- as.numeric(x)
  out <- data.frame(x = x, x2 = x^2)
  if (include_s) {
    s <- as.numeric(s)
    out$s <- s
    out$s2 <- s^2
    out$xs <- x * s
  }
  out
}

fit_gaussian_application <- function(y, x, s, r, pi, include_s) {
  idx <- which(r == 1L & is.finite(y))
  if (length(idx) < 20L) {
    stop("Too few verified site-days to fit the nuisance model.", call. = FALSE)
  }
  fit_weights <- if (include_s) rep(1, length(idx)) else 1 / pi[idx]
  d <- gaussian_design_app(x[idx], s[idx], include_s = include_s)
  mean_fit <- lm(y[idx] ~ ., data = d, weights = fit_weights)
  log_sq_resid <- log(pmax(residuals(mean_fit)^2, 1e-4))
  variance_fit <- lm(log_sq_resid ~ ., data = d, weights = fit_weights)
  list(predict = function(tau, xnew, snew) {
    nd <- gaussian_design_app(xnew, snew, include_s = include_s)
    mu <- as.numeric(predict(mean_fit, newdata = nd))
    sd <- sqrt(exp(
      as.numeric(predict(variance_fit, newdata = nd)) +
        salcdi_gaussian_log_square_correction()
    ))
    sd <- pmin(pmax(sd, 0.12), 2.5)
    pnorm(
      (matrix(tau, nrow = length(mu), ncol = length(tau), byrow = TRUE) -
         mu) / sd
    )
  }, uses_ipw = !include_s)
}

make_verification_probabilities <- function(data, p, design) {
  design <- match.arg(design, c("random", "selective"))
  if (design == "random") {
    return(rep(p, nrow(data)))
  }
  z_s <- as.numeric(scale(data$s))
  z_x <- as.numeric(scale(abs(data$x)))
  score <- exp(0.55 * z_s + 0.25 * z_x)
  e <- salcdi_calibrate_intensity(score, lower = 0.5, upper = 1.5,
                                  target = 1)
  pmin(p * e, 0.95)
}

draw_verification_mask <- function(data, pi, seed) {
  strata <- interaction(data$Location, data$month, drop = TRUE)
  epa_with_mersenne_seed(seed, function() {
    r <- integer(nrow(data))
    for (idx in split(seq_len(nrow(data)), strata)) {
      r[idx] <- rbinom(length(idx), 1L, pi[idx])
    }
    r
  })
}

full_data_target <- function(data, tau, x0, h) {
  weights <- salcdi_local_weights(
    matrix(data$x, ncol = 1L), x0, h, kernel = "epanechnikov"
  )
  salcdi_local_cdf(salcdi_threshold_signals(data$y, tau), weights)
}

cdf_quantile <- function(f, tau, probability) {
  corrected <- salcdi_monotone_cdf(pmin(pmax(f, 0), 1))
  salcdi_local_quantile(corrected, tau, probability)
}

cdf_at_threshold <- function(f, tau, threshold) {
  corrected <- salcdi_monotone_cdf(pmin(pmax(f, 0), 1))
  as.numeric(approx(
    x = tau, y = corrected, xout = threshold,
    method = "linear", rule = 2, ties = "ordered"
  )$y)
}

cluster_multiplier_band <- function(influence, center, data, h, pi,
                                    n_boot = 999L, level = 0.95,
                                    seed = 1L) {
  band <- salcdi_multiplier_band(
    influence = influence,
    center = center,
    p = mean(pi),
    h = h,
    dimension = 1L,
    n_boot = n_boot,
    level = level,
    seed = seed,
    cluster = data$week
  )
  list(
    f_hat = band$center,
    low = band$band_low,
    high = band$band_high,
    critical_value = band$critical_value,
    integrated_width = mean(band$band_high - band$band_low),
    clusters = length(unique(data$week))
  )
}

fit_one_epa_mask <- function(data, tau, x0, h, p, design, replicate,
                             seed_base, return_u = FALSE) {
  n <- nrow(data)
  pi <- make_verification_probabilities(data, p, design)
  seed <- seed_base + replicate + round(1000 * p) +
    10000L * match(design, c("random", "selective")) +
    100000L * match(x0, c(-1, 0, 1))
  r <- draw_verification_mask(data, pi, seed)
  folds <- make_cluster_folds(data$week, seed + 7L)
  z <- salcdi_threshold_signals(data$y, tau)
  method_names <- c("IPW", "X_anchor", "Full", "Adaptive")
  u_all <- lapply(method_names, function(.) matrix(NA_real_, n, length(tau)))
  names(u_all) <- method_names
  lambda_fold <- gain_fold <- g_fold <- h_fold <- numeric(3L)

  for (k in seq_len(3L)) {
    roles <- salcdi_three_role_rotation(folds, k)
    eval_idx <- roles$evaluation
    nuisance_idx <- roles$nuisance
    gain_idx <- roles$gain
    q_fit <- fit_gaussian_application(
      data$y[nuisance_idx], data$x[nuisance_idx], data$s[nuisance_idx],
      r[nuisance_idx], pi[nuisance_idx], include_s = FALSE
    )
    m_fit <- fit_gaussian_application(
      data$y[nuisance_idx], data$x[nuisance_idx], data$s[nuisance_idx],
      r[nuisance_idx], pi[nuisance_idx], include_s = TRUE
    )
    q_g <- q_fit$predict(
      tau, data$x[gain_idx], data$s[gain_idx]
    )
    m_g <- m_fit$predict(
      tau, data$x[gain_idx], data$s[gain_idx]
    )
    d_g <- m_g - q_g
    zq_g <- z[gain_idx, , drop = FALSE] - q_g
    v_g <- salcdi_gain_weights(
      matrix(data$x[gain_idx], ncol = 1L),
      x0 = x0, h = h, pi = pi[gain_idx], kernel = "epanechnikov"
    )$weights
    gains <- salcdi_gain_estimates(
      d_g, zq_g, v_g, r[gain_idx], pi[gain_idx]
    )
    g_fold[k] <- gains$G_hat
    h_fold[k] <- gains$H_hat
    lambda_fold[k] <- salcdi_estimated_lambda(
      gains$G_hat, gains$H_hat, floor = 1e-8
    )
    gain_fold[k] <- 2 * gains$G_hat - gains$H_hat

    q_e <- q_fit$predict(
      tau, data$x[eval_idx], data$s[eval_idx]
    )
    m_e <- m_fit$predict(
      tau, data$x[eval_idx], data$s[eval_idx]
    )
    fits <- list(
      IPW = matrix(0, nrow = length(eval_idx), ncol = length(tau)),
      X_anchor = q_e,
      Full = m_e,
      Adaptive = q_e + lambda_fold[k] * (m_e - q_e)
    )
    for (nm in method_names) {
      u_all[[nm]][eval_idx, ] <- salcdi_augmented_signal(
        z[eval_idx, , drop = FALSE], r[eval_idx], pi[eval_idx], fits[[nm]]
      )
    }
  }

  process <- salcdi_crossfit_local_process(
    u_all,
    x = matrix(data$x, ncol = 1L),
    fold_id = folds,
    x0 = x0,
    h = h,
    kernel = "epanechnikov"
  )
  estimates <- process$F
  truth <- full_data_target(data, tau, x0, h)
  metrics <- do.call(rbind, lapply(names(estimates), function(nm) {
    raw <- estimates[[nm]]
    corrected <- salcdi_monotone_cdf(pmin(pmax(raw, 0), 1))
    truth_corrected <- salcdi_monotone_cdf(pmin(pmax(truth, 0), 1))
    q_hat <- expm1(vapply(
      c(0.5, 0.9, 0.95),
      function(prob) cdf_quantile(corrected, tau, prob), numeric(1)
    ))
    q_truth <- expm1(vapply(
      c(0.5, 0.9, 0.95),
      function(prob) cdf_quantile(truth_corrected, tau, prob), numeric(1)
    ))
    exceed_hat <- 1 - vapply(
      c(12, 35),
      function(cutoff) cdf_at_threshold(corrected, tau, log1p(cutoff)),
      numeric(1)
    )
    exceed_truth <- 1 - vapply(
      c(12, 35),
      function(cutoff) cdf_at_threshold(
        truth_corrected, tau, log1p(cutoff)
      ), numeric(1)
    )
    data.frame(
      method = nm,
      ise_raw = mean((raw - truth)^2),
      ise_final = mean((corrected - truth)^2),
      ise = mean((corrected - truth)^2),
      sup_raw = max(abs(raw - truth)),
      sup_final = max(abs(corrected - truth)),
      sup_error = max(abs(corrected - truth)),
      abs_error_q50 = abs(q_hat[1L] - q_truth[1L]),
      abs_error_q90 = abs(q_hat[2L] - q_truth[2L]),
      abs_error_q95 = abs(q_hat[3L] - q_truth[3L]),
      abs_error_exceed_12 = abs(exceed_hat[1L] - exceed_truth[1L]),
      abs_error_exceed_35 = abs(exceed_hat[2L] - exceed_truth[2L]),
      monotonicity_violations = sum(diff(raw) < -1e-12),
      below_zero = sum(raw < 0),
      above_one = sum(raw > 1),
      stringsAsFactors = FALSE
    )
  }))
  metrics$replicate <- replicate
  metrics$seed <- seed
  metrics$p <- p
  metrics$design <- design
  metrics$x0 <- x0
  metrics$rh_target <- 50 + 20 * x0
  metrics$h <- h
  metrics$n <- n
  metrics$n_verified <- sum(r)
  rho <- vapply(process$folds, `[[`, numeric(1L), "rho")
  metrics$lambda_hat <- sum(rho * lambda_fold)
  metrics$G_hat <- sum(rho * g_fold)
  metrics$H_hat <- sum(rho * h_fold)
  metrics$full_transfer_signal <- sum(rho * gain_fold)
  weights <- salcdi_local_weights(
    matrix(data$x, ncol = 1L), x0, h, kernel = "epanechnikov"
  )
  metrics$local_support <- sum(weights > 0)
  metrics$local_effective_n <- 1 / sum(weights^2)

  out <- list(
    metrics = metrics,
    estimates = estimates,
    truth = truth,
    r = r,
    pi = pi,
    lambda_hat = sum(rho * lambda_fold),
    G_hat = sum(rho * g_fold),
    H_hat = sum(rho * h_fold),
    full_transfer_signal = sum(rho * gain_fold),
    lambda_fold = lambda_fold,
    G_fold = g_fold,
    H_fold = h_fold,
    fold_process = process$folds,
    influence = process$influence,
    fold_id = folds
  )
  if (return_u) out$u <- u_all
  out
}

summarize_epa_metrics <- function(metrics) {
  anchor <- metrics[metrics$method == "X_anchor",
                    c("p", "design", "x0", "replicate", "ise")]
  names(anchor)[names(anchor) == "ise"] <- "anchor_ise"
  metrics <- merge(
    metrics, anchor,
    by = c("p", "design", "x0", "replicate"),
    all.x = TRUE, sort = FALSE
  )
  key <- interaction(
    metrics$p, metrics$design, metrics$x0, metrics$method, drop = TRUE
  )
  rows <- lapply(split(metrics, key), function(z) {
    data.frame(
      p = z$p[1L],
      design = z$design[1L],
      x0 = z$x0[1L],
      rh_target = z$rh_target[1L],
      method = z$method[1L],
      mean_ise = mean(z$ise),
      median_ise = median(z$ise),
      mcse_ise = sd(z$ise) / sqrt(nrow(z)),
      mean_sup_error = mean(z$sup_error),
      mean_abs_error_q50 = mean(z$abs_error_q50),
      mean_abs_error_q90 = mean(z$abs_error_q90),
      mean_abs_error_q95 = mean(z$abs_error_q95),
      mean_abs_error_exceed_12 = mean(z$abs_error_exceed_12),
      mean_abs_error_exceed_35 = mean(z$abs_error_exceed_35),
      mean_lambda = mean(z$lambda_hat),
      mean_full_transfer_signal = mean(z$full_transfer_signal),
      mean_verified = mean(z$n_verified),
      negative_transfer_rate = mean(z$ise > z$anchor_ise),
      reps = length(unique(z$replicate)),
      stringsAsFactors = FALSE
    )
  })
  out <- do.call(rbind, rows)
  out <- out[order(out$design, out$p, out$x0, out$method), ]
  rownames(out) <- NULL
  out
}

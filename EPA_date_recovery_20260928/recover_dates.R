options(stringsAsFactors = FALSE)

handoff_csv <- "EPA_handoff_20260928_110006/epa_site_day_recovery.csv"
rds_path    <- "D:/OneDrive/NUDT/SALSA/paper/salcdi-jasa/analysis/output/public_application/epa_public_application.rds"
out_dir     <- "EPA_date_recovery_20260928"
dir.create(out_dir, showWarnings = FALSE)

csv <- read.csv(handoff_csv, check.names = FALSE)
obj <- readRDS(rds_path)
d   <- obj$data

if (nrow(csv) != nrow(d)) stop("Row count mismatch.")
if (!identical(as.integer(csv$observation_id), seq_len(nrow(d)))) stop("observation_id is not 1..n.")
tol <- 1e-9
checks <- c(
  reference = max(abs(csv$reference_log_pm25 - d$y)) <= tol,
  surrogate = max(abs(csv$surrogate_log_pm25 - d$s)) <= tol,
  humidity  = max(abs(csv$relative_humidity  - d$x_raw)) <= tol,
  site      = all(csv$site == d$Location)
)
if (!all(checks)) stop("Field alignment failed: ", paste(names(checks)[!checks], collapse=", "))

mapping <- data.frame(
  observation_id = seq_len(nrow(d)),
  date = format(d$date, "%Y-%m-%d"),
  stringsAsFactors = FALSE
)
mapping_path <- file.path(out_dir, "epa_date_mapping.csv")
write.csv(mapping, mapping_path, row.names = FALSE, quote = FALSE)

key <- paste(d$Location, format(d$date, "%Y-%m-%d"))
dup_rows <- sum(duplicated(key))

site_tab <- do.call(rbind, lapply(sort(unique(d$Location)), function(loc) {
  z <- d[d$Location == loc, , drop = FALSE]
  data.frame(
    site = loc, n_site_days = nrow(z),
    start_date = format(min(z$date), "%Y-%m-%d"),
    end_date   = format(max(z$date), "%Y-%m-%d"),
    stringsAsFactors = FALSE
  )
}))
rownames(site_tab) <- NULL

audit <- list(
  created_at_local = format(Sys.time(), "%Y-%m-%dT%H:%M:%S%z"),
  recovery_kind = "date appended from the archived source RDS",
  delivered_table = list(path = handoff_csv, rows = nrow(csv), columns = names(csv)),
  date_source = list(
    rds_path = rds_path,
    member = "data",
    member_columns = names(d),
    date_column = "date",
    date_class = class(d$date)
  ),
  alignment_checks = list(
    row_count_equal = TRUE,
    observation_id_is_1_to_n = TRUE,
    reference_log_pm25_equals_y = unname(checks[["reference"]]),
    surrogate_log_pm25_equals_s = unname(checks[["surrogate"]]),
    relative_humidity_equals_x_raw = unname(checks[["humidity"]]),
    site_equals_Location = unname(checks[["site"]])
  ),
  mapping = list(
    path = mapping_path,
    rows = nrow(mapping),
    columns = c("observation_id", "date"),
    unique_observation_id = length(unique(mapping$observation_id)),
    missing_dates = sum(is.na(d$date) | mapping$date == "")
  ),
  date_summary = list(
    min_date = format(min(d$date), "%Y-%m-%d"),
    max_date = format(max(d$date), "%Y-%m-%d"),
    distinct_dates = length(unique(as.character(d$date))),
    duplicate_location_date_rows = dup_rows
  ),
  per_site = site_tab,
  weekday_counts = as.list(table(weekdays(d$date, abbreviate = FALSE))),
  month_counts = as.list(table(format(d$date, "%Y-%m")))
)

jsonlite::write_json(audit, file.path(out_dir, "epa_date_mapping_audit.json"),
                     auto_unbox = TRUE, pretty = TRUE)

cat("Wrote", mapping_path, "\n")
cat("Rows:", nrow(mapping), " duplicate (Location,date) rows:", dup_rows, "\n")
cat("Date range:", format(min(d$date)), "..", format(max(d$date)), "\n")
print(site_tab)

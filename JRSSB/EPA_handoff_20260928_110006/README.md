# EPA data handoff — recovered paired-data snapshot

## Delivered data

`epa_site_day_recovery.csv` contains **2,814 complete paired observations** exported from the final anonymous JASA code archive.  The provenance script (`code/build_application_story_evidence.R`, lines 65–76) creates it directly from `epa$data` in `analysis/output/public_application/epa_public_application.rds`:

```r
reference_log_pm25 = epa$data$y
surrogate_log_pm25 = epa$data$s
relative_humidity = epa$data$x_raw
site = epa$data$Location
```

It is therefore a recoverable, pre-reference-masking paired-data snapshot, not a 5%/10%/20% subsample.  There are no missing values in the five delivered fields.

## Important limitations

This is **not** the requested lossless station–day source table.  Its export omitted `date`, `PM25_Ref`, `PM25_sens`, `RH_sens` (the exact original column name), `Location` (renamed to `site`), and all other columns. `reference_log_pm25` and `surrogate_log_pm25` are the analysis-scale variables `y` and `s`, which the processing helper defines as `log1p(pmax(PM25_*, 0))`. Thus a raw-scale inverse is available for positive values but cannot restore any negative values truncated before transformation. Without `date`, duplicate `(Location, date)` pairs and the observed date range cannot be audited from this file.

Use this CSV to begin a constrained recovery or verify the 2,814 analysis rows. For the requested complete lossless row-level delivery, recover the missing `epa_public_application.rds` or the processed EPA archive/CSV listed in `audit.json`.

## Provenance and calibration status

The archived data-processing helper identifies the source as the uncorrected PurpleAir branch `Make_ID == "PAR"`; it aggregates hourly `PM25_Ref`, `PM25_sens`, and `RH_sens` by `Location` and UTC date, filters complete finite rows, then limits PAR observations to 2019-07-22 through 2021-01-01. The archive's EPA README calls this the uncorrected PurpleAir branch. The calibration snapshot contains transformed, not raw, PM2.5 values; no separate corrected measurements were found in the handoff.

The anonymous code archive's source manifest records the original RDS as 2,783,649 bytes with SHA-256 `fee5f65c895c1618d91caf0b5002c5954dd7592eb5771d937352335b3908ec70`; that RDS is **not present** in the current checkout or its included file list.

## Included code

- `code/public_application_helpers.R` — acquisition, site-day aggregation, transformations, and reference-masking helpers.
- `code/04_public_application.R` — EPA driver that saves `epa_public_application.rds` with `data` as a list member.
- `code/build_application_story_evidence.R` — export provenance for this recovered CSV.

All included code was extracted unchanged from `JASA-active/04_Data_and_Code/Data_and_Code_Anonymous.zip`, rather than rerun. No analysis, model, quality-control, aggregation, reference masking, or data correction was performed during this handoff.

# Dataset Card

## Identification

**Name:** IoMT Attack Detection and Risk Prediction  
**Research association:** Hybrid AI-based Detection of Fileless Malware in IoMT Healthcare Systems / MediRecon  
**File format:** UTF-8 CSV  
**Rows:** 50,000  
**Fields:** 31 (timestamp, 28 input features, two targets)  
**Granularity:** five-minute time series  
**Release status:** candidate; provenance and rights review pending

## Motivation and tasks

Designed as an exploratory dataset for combining DICOM/network and Windows endpoint/security signals and experimenting with a next-24-hour multiclass risk-classification task.

## Composition and collection

The file contains window-level numeric telemetry, a timestamp and derived risk targets. Its exact source datasets, mix of recorded/generated observations, source sampling strategy, preprocessing, calibration, exact entropy definition, labeling recipe and future-window construction **cannot be verified from the CSV alone**. Fill out [the provenance template](SOURCE_PROVENANCE_TEMPLATE.md) against the original notebook and source files before describing this as a real-world benchmark.

## Labels

`future_risk_score_24h` is 0–100. `future_risk_level_24h` is deterministically categorized: LOW <30; MEDIUM 30–<50; HIGH 50–<70; CRITICAL >=70. These are observed encoding rules, not evidence of outcome validity.

## Recommended evaluation

Use temporal splits, leakage audits, classwise metrics and an untouched independent data source. Compare to a majority-class and simple heuristic baseline. Evaluate real-time drift and missing telemetry handling.

## Known limitations

- Unconfirmed real-world representativeness and target construction.
- Target-score leakage if the score is used to predict its binned label.
- Potential dependence across sequential windows and target horizons.
- Timezone and off-hours policy not encoded.
- Risk of misleading clinical/security use without external testing.
- Third-party redistribution permissions unresolved until source review.

## Privacy, ethics and security

There are no columns explicitly named patient ID, name or IP address, but source data rights and de-identification must be independently checked. Never publish raw patient data, PHI or confidential environment identifiers in supporting files.

## Maintenance and versioning

Start with a `v0.1.0` candidate tag only after review. Record revisions to generation code, source license, risk labeling, feature definitions and dataset SHA-256 in release notes.

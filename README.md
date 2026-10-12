# IoMT Attack Detection and Next-24h Risk Prediction Dataset

A time-indexed research dataset for experimenting with **IoMT healthcare network/endpoint telemetry** and **next-24-hour risk classification** within the broader research project **“Hybrid AI-based Detection of Fileless Malware in IoMT Healthcare Systems” (MediRecon)**.

> **Evidence boundary:** This file contains 50,000 sequential telemetry records and *generated/derived* 24-hour risk targets. The supplied CSV does **not** independently prove that targets were based on future observed incidents or that the data is representative of real hospitals. Read [validation limitations](docs/VALIDATION_REPORT.md) before citing results.

## Dataset at a glance

| Item | Value |
|---|---|
| Rows | **50,000** |
| Columns | **31** |
| Features | **28 telemetry features** |
| Time index | `timestamp` |
| Targets | `future_risk_score_24h`, `future_risk_level_24h` |
| Timestamp interval | **5 minutes** |
| Data range | **2026-01-01 00:00:00** to **2026-06-23 14:35:00** (timezone unspecified) |
| Risk classes | LOW, MEDIUM, HIGH, CRITICAL |
| Missing cells / duplicate rows | 0 / 0 |
| File | [`data/IoMT_Attack_Detection_and_Risk_Prediction.csv`](data/IoMT_Attack_Detection_and_Risk_Prediction.csv) |

## Risk class distribution

| Class | Count | Share |
|---|---:|---:|
| LOW | 27,458 | 54.92% |
| MEDIUM | 9,984 | 19.97% |
| HIGH | 7,488 | 14.98% |
| CRITICAL | 5,070 | 10.14% |

## Feature categories

The 28 model inputs cover time-of-day, DICOM/PACS activity, network flows, protocol signals, PowerShell indicators, lateral-movement / execution signals, process telemetry and authentication events.

Read the complete [feature dictionary](docs/FEATURE_DESCRIPTIONS.md) for **every** field and its interpretation.

## Intended use

- Prototype multivariate time-series pipelines and LSTM models for IoMT risk categories.
- Compare telemetry-derived signals across medical imaging networks and Windows endpoint activity.
- Build and test feature-ingestion contracts for a research dashboard or prediction API.

**Not intended for** clinical decisions, production healthcare blocking policies, or claims of validated future incident prediction without independent assessment.

## Example: load data

```python
import pandas as pd

df = pd.read_csv('data/IoMT_Attack_Detection_and_Risk_Prediction.csv', parse_dates=['timestamp'])
feature_cols = [c for c in df.columns if c not in (
    'timestamp', 'future_risk_score_24h', 'future_risk_level_24h'
)]
X = df[feature_cols]  # exactly 28 inputs
y = df['future_risk_level_24h']
assert len(feature_cols) == 28
print(df.shape, y.value_counts())
```

## Evaluate safely

1. Sort by `timestamp`; create **chronological** train/validation/test splits, never shuffle rows before splitting.
2. Fit imputation/scaling/encoding on **training data only**. Apply the same saved transformations at inference.
3. Construct LSTM lookback windows entirely within their allowed split; apply a purge/embargo when overlapping 24-hour targets could leak across boundaries.
4. Never include **either target** among the 28 input features. The risk level is deterministically recoverable from the score, so including the score would leak the label.
5. Report per-class precision, recall, F1, macro-F1 and confusion matrix; validate the label-generation method independently.
6. For live deployment, aggregate telemetry in **five-minute windows** and match the exact schema, time conventions and preprocessing.

## Repository structure

```text
IoMT-Risk-Prediction-Dataset/
├── data/
│   └── IoMT_Attack_Detection_and_Risk_Prediction.csv
├── docs/
│   ├── FEATURE_DESCRIPTIONS.md
│   ├── VALIDATION_REPORT.md
│   ├── DATASET_CARD.md
│   ├── SOURCE_PROVENANCE_TEMPLATE.md
│   └── GITHUB_UPLOAD_GUIDE_SI.md
├── scripts/
│   └── validate_dataset.py
├── README.md
├── requirements.txt
├── CITATION.md
├── LICENSE_GUIDANCE.md
└── .gitignore
```

## Reproduce checks

```bash
pip install -r requirements.txt
python scripts/validate_dataset.py
```

## Research and citation

This dataset is associated with **MediRecon**, a hybrid AI-based fileless malware detection research system. The dataset by itself does not establish contribution ownership, source license or independent empirical validation. See [citation guidance](CITATION.md) and [source-provenance template](docs/SOURCE_PROVENANCE_TEMPLATE.md). Add contributor names, institution, verified generation pipeline and public source references **before publication**.

## Documentation

- [Feature dictionary](docs/FEATURE_DESCRIPTIONS.md)
- [Validation report](docs/VALIDATION_REPORT.md)
- [Dataset card and limitations](docs/DATASET_CARD.md)
- [Source provenance / reproducibility checklist](docs/SOURCE_PROVENANCE_TEMPLATE.md)
- [License guidance](LICENSE_GUIDANCE.md)
- [GitHub upload instructions (Sinhala)](docs/GITHUB_UPLOAD_GUIDE_SI.md)

# Dataset Validation Report

**Validation date:** 2026-10-12  
**Dataset:** `data/IoMT_Attack_Detection_and_Risk_Prediction.csv`  
**Scope:** file integrity, schema, temporal continuity, distributions and basic consistency; **not** a machine-learning performance evaluation or external ground-truth audit.

## 1. Summary

| Check | Result |
|---|---|
| Records | **50,000** |
| Columns | **31** (timestamp + 28 inputs + 2 targets) |
| Missing cells | **0** |
| Duplicate complete rows | **0** |
| Constant columns | **0** |
| Invalid timestamps | **0** |
| Unique timestamps | **50,000** |
| Timestamp window | **2026-01-01 00:00:00** through **2026-06-23 14:35:00** |
| Interval adherence | **49,999/49,999** adjacent intervals of five minutes |
| `hour` matches timestamp hour | **50,000/50,000** |
| Invalid risk-score range (outside 0–100) | **0** |
| Risk label matches observed score bands | **PASS** |
| Negative numeric values | **0** |
| Dataset CSV SHA-256 | `a5579721fe41b4dff7129e71e4afda74d2a71267990c50c72b8291e80ca15b1c` |

## 2. Class distribution

| Risk class | Records | Share |
|---|---:|---:|
| LOW | 27,458 | 54.92% |
| MEDIUM | 9,984 | 19.97% |
| HIGH | 7,488 | 14.98% |
| CRITICAL | 5,070 | 10.14% |

Labels are imbalanced. Any model report should include macro-F1, per-class precision/recall, confusion matrix and a majority-class baseline, not accuracy alone.

## 3. Observed numeric score bands

| Class | Min score | Max score | Mean score |
|---|---:|---:|---:|
| LOW | 0.00 | 29.99 | 14.01 |
| MEDIUM | 30.00 | 49.99 | 39.44 |
| HIGH | 50.00 | 69.99 | 59.43 |
| CRITICAL | 70.00 | 100.00 | 84.50 |

## 4. Interpretation and limitations

1. **Label leakage:** risk category is a deterministic banding of `future_risk_score_24h` in this file. Exclude the score when training a classifier of the risk level. When modeling the score, do not include the risk level. A near-perfect score can otherwise be meaningless.
2. **Target provenance:** the supplied CSV alone cannot establish that the targets were computed using genuinely *future* 24-hour events. Confirm the original generator's future-window shift, risk formula, source timestamps and label-generation implementation before calling these verified forecasts.
3. **Synthetic/derived or merged telemetry:** the precise origins, transformations, licenses, and real-versus-generated portions cannot be proven from the CSV. Treat source attribution and real-world representativeness as **unverified** until generation code and source files are documented.
4. **Time-based evaluation:** make chronological splits; avoid random row splitting and overlapping window leakage. For a 24-hour horizon on a five-minute grid, consider a minimum **288-step (24-hour) purge gap** around train/validation/test boundaries when target windows can overlap. Any LSTM lookback overlap must also be considered.
5. **Real-world validity:** no external holdout, hospital telemetry study, calibration analysis, false-alert rate, deployment benchmark, or measured model performance was provided here. None is claimed.
6. **Timezone:** timestamps are timezone-naive; confirm the intended timezone and off-hours rule.
7. **Security and privacy:** no obvious identifying columns appear in the schema, but the absence of direct identifiers does not by itself prove all source provenance and release rights.

## 5. Recommended pre-publication checks

- Verify the generation notebook and input-source provenance; document licensing for every source dataset.
- Verify that scores/labels reflect future-only outcomes rather than contemporaneous signals, or clearly name the task a **generated risk-level classification benchmark** until this is demonstrated.
- Publish algorithm-independent target construction details to make the labels reproducible.
- Benchmark a leakage-free chronological split with the production 28-feature collector and chosen LSTM model.

## 6. Reproducibility

```bash
python -m pip install -r requirements.txt
python scripts/validate_dataset.py
```

The script checks the local file and writes a JSON summary. A clean check shows data consistency only, not prediction validity.

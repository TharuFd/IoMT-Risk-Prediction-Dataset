"""Independent dataset structure and consistency checker (not predictive validation)."""
from pathlib import Path
import argparse, hashlib, json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / 'data' / 'IoMT_Attack_Detection_and_Risk_Prediction.csv'
LABELS = {'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'}


def validate(path):
    df = pd.read_csv(path)
    errors = []
    timestamp = pd.to_datetime(df.get('timestamp'), errors='coerce')
    expected_columns = {'timestamp', 'future_risk_score_24h', 'future_risk_level_24h'}
    if not expected_columns.issubset(df.columns):
        raise ValueError(f'Missing required columns: {expected_columns - set(df.columns)}')
    features = [c for c in df if c not in expected_columns]
    if len(features) != 28:
        errors.append(f'Expected 28 features, got {len(features)}')
    if len(df) != 50000:
        errors.append(f'Expected 50000 records, got {len(df)}')
    missing = int(df.isna().sum().sum())
    duplicates = int(df.duplicated().sum())
    if missing: errors.append(f'{missing} missing cells')
    if duplicates: errors.append(f'{duplicates} duplicate rows')
    if timestamp.isna().any(): errors.append('Invalid timestamp values')
    deltas = timestamp.diff().dropna()
    invalid_steps = int((deltas != pd.Timedelta(minutes=5)).sum())
    if invalid_steps: errors.append(f'{invalid_steps} non-five-minute timestamp gaps')
    hour_mismatches = int((timestamp.dt.hour != df.hour).sum()) if 'hour' in df else None
    if hour_mismatches: errors.append(f'{hour_mismatches} hour mismatches')
    score = pd.to_numeric(df['future_risk_score_24h'], errors='coerce')
    level = df['future_risk_level_24h']
    if (~score.between(0, 100)).any(): errors.append('Invalid risk scores')
    invalid_labels = set(level.dropna().unique()) - LABELS
    if invalid_labels: errors.append(f'Invalid labels: {sorted(invalid_labels)}')
    expected_level = pd.cut(score, [-0.001, 30, 50, 70, 100], right=False, labels=['LOW','MEDIUM','HIGH','CRITICAL']).astype(object)
    expected_level.loc[score == 100] = 'CRITICAL'
    inconsistent = int((expected_level != level).sum())
    if inconsistent: errors.append(f'{inconsistent} score/level mismatches')
    numeric = df.select_dtypes(include='number')
    neg = int((numeric < 0).sum().sum())
    if neg: errors.append(f'{neg} negative numeric cells')
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    result = {'file':str(path),'records':len(df),'columns':len(df.columns),'features':len(features),
      'missing_cells':missing,'duplicate_rows':duplicates,'invalid_intervals':invalid_steps,
      'hour_mismatches':hour_mismatches,'label_mismatches':inconsistent,
      'class_counts':{x:int((level==x).sum()) for x in ['LOW','MEDIUM','HIGH','CRITICAL']},
      'start':str(timestamp.min()),'end':str(timestamp.max()),'sha256':digest,
      'status':'PASS' if not errors else 'FAIL','errors':errors,
      'note':'Passing these checks does not establish label provenance, future-horizon validity or predictive accuracy.'}
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--csv', type=Path, default=DEFAULT)
    parser.add_argument('--json-out', type=Path, default=None)
    args=parser.parse_args()
    result=validate(args.csv)
    print(json.dumps(result,indent=2))
    if args.json_out: args.json_out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if result['status']=='PASS' else 1)

if __name__=='__main__': main()

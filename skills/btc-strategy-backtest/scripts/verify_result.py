"""Independent finite-metric gate audit. Does not execute strategies or write DB."""
import argparse
import json
import math
from pathlib import Path

LIMITS = {'return_pct': 50., 'trade_count': 30, 'profit_factor': 1.1,
          'sharpe_ratio': .5, 'drawdown_pct': 15.}

def audit(result):
    failures = []
    for split in ['validation', 'test']:
        metrics = result.get(split, {}).get('metrics', {})
        for key, limit in LIMITS.items():
            value = metrics.get(key)
            if type(value) not in (int, float) or not math.isfinite(value):
                failures.append(f'{split}.{key}: missing/nonfinite')
            elif (value > limit if key == 'drawdown_pct' else value < limit):
                failures.append(f'{split}.{key}: gate failed')
    folds = result.get('test_folds', [])
    values = [f.get('metrics', {}).get('return_pct') for f in folds]
    if len(values) != 3 or any(type(v) not in (int, float) or not math.isfinite(v) for v in values):
        failures.append('test_folds: require three finite results')
    elif sum(v > 0 for v in values) < 2:
        failures.append('test_folds: fewer than two positive')
    stress = result.get('cost_stress', {}).get('metrics', {}).get('return_pct')
    if type(stress) not in (int, float) or not math.isfinite(stress) or stress <= 0:
        failures.append('cost_stress: require positive finite return')
    if result.get('return_currency') != 'BTC':
        failures.append('return_currency: must be BTC')
    if result.get('status') == 'source_review_failed':
        failures.append('source review failed')
    qualified = not failures
    return {'version': result.get('version'), 'computed_qualified': qualified,
            'reported_qualified': result.get('qualified'),
            'consistent': type(result.get('qualified')) is bool and qualified == result['qualified'],
            'failures': failures,
            'scope': 'Metric audit only; verify source, hashes, data and cost model separately'}

def summary(result):
    return {k: result[k] for k in ['engine', 'version', 'code_hash', 'dataset_fingerprint',
             'spec', 'data', 'split', 'cost_model', 'funding_included', 'qualified',
             'paper_ready', 'thresholds', 'limitations', 'status', 'return_currency'] if k in result} | {
        'splits': {k: result.get(k, {}).get('metrics', {})
                   for k in ['train', 'validation', 'test', 'cost_stress']},
        'test_folds': [f.get('metrics', {}) for f in result.get('test_folds', [])]}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('result')
    args = parser.parse_args()
    report = audit(json.loads(Path(args.result).read_text(encoding='utf-8')))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report['consistent'] else 2)

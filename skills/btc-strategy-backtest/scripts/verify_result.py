"""Independent finite-metric gate audit. Does not execute strategies or write DB."""
import argparse
import json
import math
from pathlib import Path

LIMITS = {'return_pct': 50., 'trade_count': 30, 'profit_factor': 1.1,
          'sharpe_ratio': .5, 'drawdown_pct': 15.}

def audit(result):
    failures = []
    try:
        json.dumps(result, allow_nan=False)
    except (ValueError, TypeError):
        failures.append('result: invalid/nonfinite JSON')
    if (result.get('contract') != 'Binance COIN-M BTCUSD_PERP'
            or result.get('return_currency') != 'BTC'
            or result.get('cost_model', {}).get('contract_type') != 'inverse'
            or result.get('cost_model', {}).get('return_currency') != 'BTC'
            or result.get('data', {}).get('contract_type', 'inverse') != 'inverse'
            or result.get('data', {}).get('return_currency', 'BTC') != 'BTC'):
        failures.append('contract/currency: require inverse BTCUSD and BTC')
    folds = result.get('test_folds', [])
    if not isinstance(folds, list) or len(folds) != 3:
        failures.append('test_folds: require three results')
        folds = []
    segments = [(k, result.get(k, {})) for k in ['train', 'validation', 'test', 'cost_stress']]
    segments += [(f'fold_{i}', f) for i, f in enumerate(folds)]
    for split, segment in segments:
        metrics = segment.get('metrics', {}) if isinstance(segment, dict) else {}
        if metrics.get('return_currency') != 'BTC':
            failures.append(f'{split}: require BTC')
        for key, limit in LIMITS.items():
            value = metrics.get(key)
            if type(value) not in (int, float) or not math.isfinite(value):
                failures.append(f'{split}.{key}: missing/nonfinite')
                continue
            if (key == 'trade_count' and (type(value) is not int or value < 0)
                    or key == 'drawdown_pct' and not 0 <= value <= 100
                    or key == 'profit_factor' and value < 0
                    or key == 'return_pct' and value < -100):
                failures.append(f'{split}.{key}: invalid range/type')
            if split in ['validation', 'test'] and (value > limit if key == 'drawdown_pct' else value < limit):
                failures.append(f'{split}.{key}: gate failed')
    values = [f.get('metrics', {}).get('return_pct') for f in folds if isinstance(f, dict)]
    if len(values) != 3 or any(type(v) not in (int, float) or not math.isfinite(v) for v in values) or sum(v > 0 for v in values) < 2:
        failures.append('test_folds: require at least two positive finite returns')
    stress = result.get('cost_stress', {}).get('metrics', {}).get('return_pct')
    if type(stress) not in (int, float) or not math.isfinite(stress) or stress <= 0:
        failures.append('cost_stress: require positive finite return')
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

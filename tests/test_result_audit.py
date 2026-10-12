import copy
import importlib.util
from pathlib import Path
import unittest

root = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('verify', root/'skills/btc-strategy-backtest/scripts/verify_result.py')
verify = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify)

def passing():
    metrics = {'return_currency': 'BTC', 'return_pct': 50., 'trade_count': 30, 'profit_factor': 1.1,
               'sharpe_ratio': .5, 'drawdown_pct': 15.}
    return {'version': 1, 'return_currency': 'BTC', 'qualified': True,
            'contract': 'Binance COIN-M BTCUSD_PERP', 'cost_model': {'contract_type':'inverse','return_currency':'BTC'},
            'train': {'metrics': dict(metrics)}, 'validation': {'metrics': dict(metrics)}, 'test': {'metrics': dict(metrics)},
            'test_folds': [{'metrics': dict(metrics, return_pct=v)} for v in [1, 1, -1]],
            'cost_stress': {'metrics': dict(metrics, return_pct=.001)}}

class ResultAuditTests(unittest.TestCase):
    def test_exact_boundaries_pass(self):
        self.assertTrue(verify.audit(passing())['consistent'])

    def test_nonfinite_or_missing_metrics_block_qualification(self):
        for value in [None, float('nan'), float('inf'), True]:
            with self.subTest(value=value):
                result=passing();result['test']['metrics']['profit_factor']=value
                self.assertFalse(verify.audit(result)['computed_qualified'])
                self.assertFalse(verify.audit(result)['consistent'])

    def test_fold_and_cost_require_strictly_positive_returns(self):
        result=passing();result['cost_stress']['metrics']['return_pct']=0
        self.assertFalse(verify.audit(result)['computed_qualified'])
        result=passing();result['test_folds'][1]['metrics']['return_pct']=0
        self.assertFalse(verify.audit(result)['computed_qualified'])

    def test_source_failure_and_usd_are_blocked(self):
        for key,value in [('status','source_review_failed'),('return_currency','USD')]:
            result=passing();result[key]=value
            self.assertFalse(verify.audit(result)['computed_qualified'])

    def test_agreeing_rejection_is_a_successful_audit(self):
        result=passing();result['qualified']=False;result['test']['metrics']['return_pct']=-10
        self.assertTrue(verify.audit(result)['consistent'])

    def test_incomplete_fold_set_is_blocked(self):
        result=passing();result['test_folds'].pop()
        self.assertFalse(verify.audit(result)['computed_qualified'])

if __name__=='__main__':unittest.main()

class CompleteAuditTests(unittest.TestCase):
    def test_all_segments_have_independent_currency_and_numeric_validation(self):
        for index in range(7):
            for key,value in [('return_currency','USD'),('profit_factor',float('inf')),('trade_count',30.),('drawdown_pct',-1),('return_pct',True)]:
                result=passing();segments=[result[k] for k in ['train','validation','test','cost_stress']]+result['test_folds']
                segments[index]['metrics'][key]=value
                with self.subTest(index=index,key=key): self.assertFalse(verify.audit(result)['computed_qualified'])
    def test_cost_and_dataset_contract_are_validated(self):
        for container,key,value in [('cost_model','contract_type','linear'),('cost_model','return_currency','USD'),('data','contract_type','linear')]:
            result=passing();result.setdefault(container,{})[key]=value
            self.assertFalse(verify.audit(result)['computed_qualified'])

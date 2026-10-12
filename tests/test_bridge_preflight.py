import copy
import importlib.util
from pathlib import Path
import unittest
spec=importlib.util.spec_from_file_location('bridge',Path(__file__).resolve().parents[1]/'skills/btc-strategy-backtest/scripts/backtest_bridge.py')
bridge=importlib.util.module_from_spec(spec);spec.loader.exec_module(bridge)

class PreflightTests(unittest.TestCase):
    def evidence(self):
        return {'jobs':{j:{'enabled':False,'delivery':{'mode':'none'}} for j in [bridge.SEARCH_JOB,bridge.BACKTEST_JOB]},'fixture_present':False}
    def test_takeover_and_isolation_are_required(self):
        bridge.validate_write_preflight(self.evidence(),'run')
        for change in ['legacy','search','announce','fixture','missing']:
            e=self.evidence()
            if change=='legacy': e['jobs'][bridge.BACKTEST_JOB]['enabled']=True
            if change=='search': e['jobs'][bridge.SEARCH_JOB]['enabled']=True
            if change=='announce': e['jobs'][bridge.BACKTEST_JOB]['delivery']['mode']='announce'
            if change=='fixture': e['fixture_present']=True
            if change=='missing': e['jobs'].pop(bridge.BACKTEST_JOB)
            with self.subTest(change=change),self.assertRaises(RuntimeError): bridge.validate_write_preflight(e,'run')
    def test_sync_does_not_claim_consumer_ownership(self):
        e=self.evidence();e['jobs'][bridge.BACKTEST_JOB]['enabled']=True
        bridge.validate_write_preflight(e,'sync')

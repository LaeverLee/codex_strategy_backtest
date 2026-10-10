"""SSH bridge to existing runtime. No install, credential printing or model calls."""
import argparse
import json
from pathlib import Path
import re
import shlex
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['health', 'inspect', 'result', 'run', 'sync'])
    parser.add_argument('--config', required=True)
    parser.add_argument('--version', type=int)
    parser.add_argument('--output', help='Save complete result locally; stdout remains compact')
    parser.add_argument('--execute', action='store_true', help='Explicitly permit run/sync writes')
    args = parser.parse_args()
    if args.action in {'run', 'sync'} and not args.execute:
        parser.error('run/sync requires --execute; first verify schedule ownership')
    if args.action == 'result' and (args.version is None or args.version < 1):
        parser.error('result requires positive --version')
    cfg = json.loads(Path(args.config).read_text(encoding='utf-8'))
    for key in ['host', 'user', 'namespace', 'service_id']:
        if not re.fullmatch(r'[A-Za-z0-9_.-]+', cfg[key]):
            raise ValueError('Invalid connection identifier')
    root = cfg['remote_root']
    if not root.startswith('/home/node/.openclaw/') or '..' in root.split('/'):
        raise ValueError('Unexpected remote root')
    ssh = ['ssh', '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=yes', '-o', 'ConnectTimeout=10']
    if cfg.get('identity_file'):
        ssh += ['-i', str(Path(cfg['identity_file']).expanduser())]
    ssh += [cfg['user']+'@'+cfg['host']]
    def remote(argv, timeout=60):
        process = subprocess.run(ssh+[shlex.join(argv)], capture_output=True, timeout=timeout)
        if process.returncode:
            raise RuntimeError('Remote operation failed; private diagnostic output withheld')
        return process.stdout.decode('utf-8')
    pods = json.loads(remote(['kubectl', 'get', 'pods', '-n', cfg['namespace'], '-o', 'json']))['items']
    ready = [p['metadata']['name'] for p in pods
             if p['metadata']['name'].startswith('service-'+cfg['service_id']+'-')
             and p['status'].get('phase') == 'Running' and not p['metadata'].get('deletionTimestamp')
             and any(c.get('type') == 'Ready' and c.get('status') == 'True'
                     for c in p['status'].get('conditions', []))]
    if len(ready) != 1:
        raise RuntimeError('Expected exactly one Ready service pod')
    base = ['kubectl', 'exec', '-i', '-n', cfg['namespace'], ready[0]]
    if cfg.get('container'):
        base += ['-c', cfg['container']]
    base += ['--']
    if args.action == 'result':
        code = 'import pathlib,sys;p=pathlib.Path(sys.argv[1]);print(p.read_text() if p.exists() else "RESULT_PENDING")'
        raw = remote(base+['python3', '-c', code, root+'/pytest/research_results/'+str(args.version)+'.json'])
        if raw.strip() == 'RESULT_PENDING':
            print(raw.strip()); return
        result = json.loads(raw)
        if args.output:
            path = Path(args.output); path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(raw, encoding='utf-8')
        from verify_result import summary, audit
        print(json.dumps({'summary': summary(result), 'audit': audit(result)}, ensure_ascii=False))
    elif args.action == 'inspect':
        code = '''import pathlib,json,sys,sqlite3,hashlib
r=pathlib.Path(sys.argv[1]);items=[]
for p in (r/'pytest/Strategy').glob('*_Strategy_Gold.json'):
 m=json.loads(p.read_text());py=p.with_suffix('.py')
 items.append({k:m.get(k) for k in ['version','engine','db_committed','code_hash','research_mode']}|{'code_matches':py.exists() and hashlib.sha256(py.read_bytes()).hexdigest()==m.get('code_hash'),'source_approved':m.get('source_review',{}).get('approved')})
c=sqlite3.connect('file:/home/node/.openclaw/state/openclaw.sqlite?mode=ro',uri=True);jobs=[]
for id in ['52d4bf14-f93e-4f00-8e67-fc770aef6929','a8f06958-e766-4780-b4bf-a845977100b7']:
 row=c.execute('select job_json from cron_jobs where job_id=?',(id,)).fetchone()
 if row:
  j=json.loads(row[0]);jobs.append({'id':id,'enabled':j.get('enabled'),'schedule':j.get('schedule')})
print(json.dumps({'queue':items,'jobs':jobs,'engine_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in r.glob('*.py') if p.name in ['backtest_v6.py','quality_policy.py','lab_records.py','strategy_quality.py']}}))'''
        print(remote(base+['python3', '-c', code, root]))
    else:
        mode = {'run': 'backtest'}.get(args.action, args.action)
        raw = remote(base+['python3', root+'/lab_runtime.py', mode], timeout=900 if mode == 'backtest' else 90)
        # Runtime success is not proof of a completed candidate; inspect/result/DB after execution.
        print(raw if mode == 'health' else json.dumps({'command_finished': True, 'mode': mode,
                                                      'verification_required': True}))

if __name__ == '__main__':
    main()

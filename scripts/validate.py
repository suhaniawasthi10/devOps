#!/usr/bin/env python3
"""Offline repository checks. Does not create Docker/cluster/cloud resources."""
from pathlib import Path
import json
import re
import subprocess
import sys
from urllib.parse import unquote
import yaml

ROOT = Path(__file__).resolve().parents[1]
IGNORED = {'.git', 'node_modules', 'dist', '.venv', '.terraform', '__pycache__', '.pytest_cache'}
errors = []
counts = {'yaml': 0, 'shell': 0, 'links': 0}

def run(command, cwd=ROOT):
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    if result.returncode:
        errors.append(' '.join(command) + '\n' + result.stdout + result.stderr)
    return result.stdout

files = [p for p in ROOT.rglob('*') if p.is_file() and not (set(p.relative_to(ROOT).parts) & IGNORED)]
for path in files:
    relative = path.relative_to(ROOT)
    if path.suffix in {'.yaml', '.yml'} and 'helm/templates' not in relative.as_posix():
        try:
            list(yaml.safe_load_all(path.read_text()))
            counts['yaml'] += 1
        except yaml.YAMLError as error:
            errors.append(f'{relative}: {error}')
    if path.suffix == '.sh':
        run(['bash', '-n', str(path)])
        counts['shell'] += 1
    if path.suffix == '.md':
        # Ignore code examples while checking actual documentation links.
        prose = re.sub(r'```.*?```', '', path.read_text(), flags=re.S)
        for link in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', prose):
            target = unquote(link.split('#')[0].strip('<>'))
            if not target or re.match(r'\w+://|mailto:', target):
                continue
            counts['links'] += 1
            if not (path.parent / target).exists():
                errors.append(f'{relative}: broken link {link}')

chart = 'final-devops-project/helm'
run(['helm', 'lint', chart])
for extra in [[], ['-f', chart + '/values-prod.yaml'], ['--set', 'persistence.enabled=false', '--set', 'secret.existingName=external-secret']]:
    rendered = run(['helm', 'template', 'notes', chart] + extra)
    try:
        resources = [x for x in yaml.safe_load_all(rendered) if x]
        kinds = {x['kind'] for x in resources}
        if not {'Deployment', 'Service', 'ConfigMap'} <= kinds:
            errors.append('Chart missing required resources')
    except (yaml.YAMLError, KeyError) as error:
        errors.append(f'Chart rendering: {error}')

snapshot = run(['helm', 'template', 'notes', chart, '--namespace', 'devops-final', '-f', chart + '/values-prod.yaml', '--skip-tests'])
if snapshot != (ROOT / 'final-devops-project/kubernetes/resources.yaml').read_text():
    errors.append('Kubernetes snapshot is stale: run bash scripts/render-manifests.sh')

stack = list(yaml.safe_load_all((ROOT / 'final-devops-project/monitoring/stack.yaml').read_text()))
configs = {x['metadata']['name']: x['data'] for x in stack if x['kind'] == 'ConfigMap'}
for embedded, source in [('prometheus.yml', 'prometheus.yml'), ('alerts.yaml', 'alerts.yaml')]:
    if yaml.safe_load(configs['prometheus-config'][embedded]) != yaml.safe_load((ROOT / 'final-devops-project/monitoring' / source).read_text()):
        errors.append(f'Monitoring ConfigMap differs from {source}')
if yaml.safe_load(configs['alertmanager-config']['alertmanager.yml']) != yaml.safe_load((ROOT / 'final-devops-project/monitoring/alertmanager.yml').read_text()):
    errors.append('Alertmanager ConfigMap differs from source')

for file in (ROOT / '.github/workflows').glob('*.yml'):
    workflow = yaml.load(file.read_text(), Loader=yaml.BaseLoader)
    if 'on' not in workflow or 'jobs' not in workflow:
        errors.append(f'{file.name}: missing workflow triggers/jobs')

print(json.dumps(counts, indent=2))
if errors:
    print('\n\n'.join(errors), file=sys.stderr)
    sys.exit(1)
print('Offline repository checks passed.')

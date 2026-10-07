#!/usr/bin/env python3
"""Test a built Notes image, cleaning up only this test's containers/volume."""
import argparse
from http.client import HTTPException
import json
import subprocess
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import uuid

parser = argparse.ArgumentParser()
parser.add_argument('image', nargs='?', default='coursework-notes:local')
args = parser.parse_args()
volume = 'coursework-validation-' + uuid.uuid4().hex[:12]
container = None

def docker(*args):
    return subprocess.check_output(['docker', *args], text=True).strip()

def launch():
    global container
    container = docker('run', '-d', '--read-only', '--cap-drop=ALL', '--security-opt=no-new-privileges:true',
                       '--tmpfs', '/tmp:rw,noexec,nosuid,size=64m', '-v', volume + ':/data',
                       '-e', 'DEMO_API_KEY=container-test-only', '-p', '127.0.0.1::8080', args.image)
    port = docker('port', container, '8080/tcp').rsplit(':', 1)[1]
    base = 'http://127.0.0.1:' + port
    for _ in range(40):
        try:
            with urlopen(base + '/readyz', timeout=2) as response:
                if response.status == 200:
                    return base
        except (URLError, OSError, HTTPException):
            time.sleep(0.25)
    raise RuntimeError('Container never became ready: ' + docker('logs', container))

try:
    docker('volume', 'create', volume)
    base = launch()
    payload = json.dumps({'text': 'Persistent container validation'}).encode()
    try:
        urlopen(Request(base + '/api/notes', data=payload, headers={'Content-Type':'application/json'}), timeout=5)
        raise AssertionError('Unauthenticated mutation was accepted')
    except HTTPError as error:
        assert error.code == 401
    with urlopen(Request(base + '/api/notes', data=payload, headers={'Content-Type':'application/json','X-API-Key':'container-test-only'}), timeout=5) as response:
        assert response.status == 201
    assert docker('exec', container, 'id', '-u') == '10001'
    docker('rm', '-f', container)
    container = None
    base = launch()
    with urlopen(base + '/api/notes', timeout=5) as response:
        assert json.load(response)[0]['text'] == 'Persistent container validation'
    with urlopen(base + '/metrics', timeout=5) as response:
        assert b'notes_requests_total' in response.read()
    print('Container checks passed: non-root, read-only filesystem, authentication, HTTP, metrics, persistence after recreation.')
finally:
    if container:
        docker('rm', '-f', container)
    docker('volume', 'rm', volume)

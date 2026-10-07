#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p build
python -m compileall -q app
python -c 'import datetime,json; print(json.dumps({"application":"calculator", "built_at":datetime.datetime.now(datetime.timezone.utc).isoformat()}))' > build/build-info.json
tar --exclude=__pycache__ -czf build/calculator.tar.gz app requirements.txt Dockerfile

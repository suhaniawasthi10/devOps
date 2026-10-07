# Notes application

A Flask API and browser interface with SQLite persistence, request IDs, structured logs, health/readiness checks and Prometheus metrics. API writes require the key injected by a Kubernetes Secret; public lab notes are readable without authentication. This is coursework, not a multi-user production service.

From this directory:
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
export DEMO_API_KEY=coursework-demo-only
export NOTES_DB=/tmp/coursework-notes.db
gunicorn --bind 127.0.0.1:8080 --workers 1 --threads 4 wsgi:app
```
Open http://localhost:8080 and use the dummy key above. GET `/api/notes`, POST `{ "text": "hello" }` to `/api/notes`, DELETE `/api/notes/<id>`. For mutations include `X-API-Key`. `/healthz` checks process responsiveness; `/readyz` reads the database; `/api/config` exposes only version, environment and whether a Secret exists. `/metrics` exports request/latency and process CPU/memory metrics. `/work` performs bounded CPU work for HPA.

Tests cover persistence after restart, concurrent writes, invalid input, missing authentication, SQL injection as data, readiness failure and metrics. The single Gunicorn worker keeps process-local metric aggregation correct. Multiple Pods each expose their own scrape target.

"""Notes coursework API. SQLite storage targets a single Kubernetes node."""
import hmac
import hashlib
import json
import logging
import os
from pathlib import Path
import sqlite3
import time
import uuid

from flask import Flask, Response, g, jsonify, render_template, request
from prometheus_client import CollectorRegistry, Counter, Histogram, ProcessCollector, generate_latest, CONTENT_TYPE_LATEST


def create_app(database=None):
    app = Flask(__name__)
    app.config.update(MAX_CONTENT_LENGTH=16384, DATABASE=database or os.getenv("NOTES_DB", str(Path(app.instance_path) / "notes.db")))
    Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(app.config["DATABASE"], timeout=10) as db:
        db.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, text TEXT NOT NULL)")
    registry = CollectorRegistry()
    ProcessCollector(registry=registry)
    requests = Counter("notes_requests_total", "HTTP responses", ["route", "status"], registry=registry)
    latency = Histogram("notes_request_seconds", "Request latency", ["route"], registry=registry)
    logging.basicConfig(level=logging.INFO)

    def connect():
        db = sqlite3.connect(app.config["DATABASE"], timeout=10)
        db.row_factory = sqlite3.Row
        return db

    def authorized():
        configured = os.getenv("DEMO_API_KEY", "")
        supplied = request.headers.get("X-API-Key", "")
        return bool(configured) and hmac.compare_digest(configured.encode(), supplied.encode())

    @app.before_request
    def begin():
        g.started = time.monotonic()
        g.request_id = str(uuid.uuid4())

    @app.after_request
    def finish(response):
        route = request.url_rule.rule if request.url_rule else "unmatched"
        requests.labels(route, response.status_code).inc()
        latency.labels(route).observe(time.monotonic() - g.started)
        response.headers["X-Request-ID"] = g.request_id
        response.headers["X-Content-Type-Options"] = "nosniff"
        app.logger.info(json.dumps({"request_id": g.request_id, "route": route, "status": response.status_code}))
        return response

    @app.get("/")
    def index():
        return render_template("index.html", version=os.getenv("APP_VERSION", "v1"))

    @app.get("/healthz")
    def health():
        return jsonify(status="healthy")

    @app.get("/readyz")
    def ready():
        try:
            with connect() as db:
                db.execute("SELECT 1 FROM notes LIMIT 1").fetchone()
            return jsonify(status="ready")
        except sqlite3.Error:
            return jsonify(status="not ready"), 503

    @app.get("/api/config")
    def config():
        return jsonify(version=os.getenv("APP_VERSION", "v1"), environment=os.getenv("ENVIRONMENT", "local"),
                       secret_configured=bool(os.getenv("DEMO_API_KEY")))

    @app.route("/api/notes", methods=["GET", "POST"])
    def notes():
        if request.method == "POST":
            if not authorized():
                return jsonify(error="Unauthorized"), 401
            data = request.get_json(silent=True)
            text = data.get("text") if isinstance(data, dict) else None
            if not isinstance(text, str) or not 1 <= len(text.strip()) <= 500:
                return jsonify(error="text must contain 1–500 characters"), 400
            with connect() as db:
                result = db.execute("INSERT INTO notes (text) VALUES (?)", (text.strip(),))
                note_id = result.lastrowid
            return jsonify(id=note_id, text=text.strip()), 201
        with connect() as db:
            rows = db.execute("SELECT id, text FROM notes ORDER BY id DESC LIMIT 100").fetchall()
        return jsonify([dict(row) for row in rows])

    @app.delete("/api/notes/<int:note_id>")
    def delete_note(note_id):
        if not authorized():
            return jsonify(error="Unauthorized"), 401
        with connect() as db:
            deleted = db.execute("DELETE FROM notes WHERE id = ?", (note_id,)).rowcount
        return ("", 204) if deleted else (jsonify(error="Not found"), 404)

    @app.get("/work")
    def work():
        # Fixed, bounded CPU task for HPA; never accepts an unbounded iteration count.
        hashlib.pbkdf2_hmac("sha256", b"public-coursework", b"public-lab-salt", 120000)
        return jsonify(completed=True)

    @app.get("/metrics")
    def metrics():
        return Response(generate_latest(registry), content_type=CONTENT_TYPE_LATEST)

    return app

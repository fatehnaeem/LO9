"""
Week 9 Flask DevOps Lab (STARTER)

This starter intentionally includes only a basic Flask API with a local SQLite database.
Students complete Week 9 tasks by adding containerization, compose, observability,
and CI in this project.
"""

import json
import logging
import os
import sqlite3
import time
import uuid
from pathlib import Path

import redis
from flask import Flask, g, jsonify, request

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "app.db"

app = Flask(__name__)

# Redis client initialization
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
try:
    redis_client = redis.from_url(REDIS_URL)
except Exception as e:
    print(f"Warning: Could not connect to Redis at {REDIS_URL}: {e}")
    redis_client = None


# Structured logging middleware
@app.before_request
def before_request():
    g.request_id = str(uuid.uuid4())
    g.start_time = time.time()


@app.after_request
def after_request(response):
    latency_ms = (time.time() - g.start_time) * 1000
    log_entry = {
        "method": request.method,
        "path": request.path,
        "status": response.status_code,
        "latencyMs": round(latency_ms, 2),
        "requestId": g.request_id,
    }
    print(json.dumps(log_entry))
    return response


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_error):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    db.commit()


@app.route("/")
def home():
    return jsonify(
        {
            "message": "Week 9 starter API",
            "hint": "Implement /health, /ready, Dockerfile, docker-compose, and CI",
        }
    )


@app.route("/ping")
def ping():
    return jsonify({"message": "pong"})


@app.route("/notes", methods=["GET"])
def list_notes():
    db = get_db()
    rows = db.execute("SELECT id, text, created_at FROM notes ORDER BY id DESC").fetchall()
    return jsonify([dict(row) for row in rows])


@app.route("/notes", methods=["POST"])
def create_note():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "text is required"}), 400

    db = get_db()
    cursor = db.execute("INSERT INTO notes (text) VALUES (?)", [text])
    db.commit()
    return jsonify({"id": cursor.lastrowid, "text": text}), 201


# Task 3: Liveness endpoint
@app.route("/health")
def health():
    return jsonify({"status": "alive"}), 200


# Task 3: Readiness endpoint - checks Redis dependency
@app.route("/ready")
def ready():
    if redis_client is None:
        return jsonify({"status": "not-ready", "reason": "Redis not configured"}), 503
    
    try:
        redis_client.ping()
        return jsonify({"status": "ready"}), 200
    except Exception as e:
        return jsonify({"status": "not-ready", "reason": str(e)}), 503


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)

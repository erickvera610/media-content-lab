"""Idempotent SQL experiment registry; no private article content or uploads."""
import sqlite3

def save(path,report):
    with sqlite3.connect(path) as db:
        db.execute('CREATE TABLE IF NOT EXISTS experiments (model_sha TEXT PRIMARY KEY, executed_at TEXT, model TEXT, log_mae REAL, baseline_log_mae REAL)')
        db.execute('INSERT OR REPLACE INTO experiments VALUES (?,?,?,?,?)',(report['model_sha256'],report['executed_at_utc'],report['selected_model'],report['test']['log_mae'],report['test']['baseline_log_mae']))

def list_runs(path):
    with sqlite3.connect(path) as db:
        db.row_factory=sqlite3.Row
        return [dict(r) for r in db.execute('SELECT model_sha, executed_at, model, log_mae, baseline_log_mae FROM experiments ORDER BY executed_at DESC')]

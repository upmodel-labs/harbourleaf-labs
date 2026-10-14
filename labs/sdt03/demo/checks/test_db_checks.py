# test_db_checks.py - Harbourleaf database checks as tests (read-only)
# Each check is a query that returns the bad rows. A clean result is 0 rows.
# Connection: set LABS_DSN, or leave it unset to use the PG* settings (Codespaces sets them).
import os

import psycopg
import pytest

DSN = os.environ.get("LABS_DSN", "dbname=labs")

CHECKS = [
    ("every shipment migrated", """
        SELECT o.shipment_id
        FROM hl_check.shipments_old o
        LEFT JOIN hl_check.shipments s ON s.shipment_id = o.shipment_id
        WHERE s.shipment_id IS NULL
        ORDER BY o.shipment_id""", 0),
    ("no unmapped old status", """
        SELECT o.shipment_id, o.status_old
        FROM hl_check.shipments_old o
        LEFT JOIN hl_check.status_map m ON m.status_old = o.status_old
        WHERE m.status_old IS NULL
        ORDER BY o.shipment_id""", 0),
    ("counts per status match the mapping", """
        WITH expected AS (
          SELECT COALESCE(m.status_new, '(unmapped)') AS status, COUNT(*) AS n
          FROM hl_check.shipments_old o
          LEFT JOIN hl_check.status_map m ON m.status_old = o.status_old
          GROUP BY 1),
        actual AS (
          SELECT s.status, COUNT(*) AS n FROM hl_check.shipments s GROUP BY 1)
        SELECT COALESCE(e.status, a.status) AS status, e.n AS expected, a.n AS actual
        FROM expected e
        FULL JOIN actual a ON a.status = e.status
        WHERE COALESCE(e.n, 0) <> COALESCE(a.n, 0)
        ORDER BY 1""", 0),
    ("every run question has an answer", """
        SELECT q.run_id, q.question_id
        FROM hl_check.run_questions q
        LEFT JOIN hl_check.answers a ON a.run_id = q.run_id AND a.question_id = q.question_id
        WHERE a.answer_id IS NULL
        ORDER BY q.question_id""", 0),
    ("no email address in a reply", """
        SELECT r.response_id, r.created_at, r.source
        FROM hl_check.responses r
        WHERE r.reply_text ~ '[A-Za-z0-9._]+@[A-Za-z0-9.]+'
        ORDER BY r.response_id""", 0),
]


@pytest.fixture
def conn():
    with psycopg.connect(DSN) as c:
        c.read_only = True
        yield c
        c.rollback()


@pytest.mark.parametrize("name, query, expected", CHECKS, ids=[c[0] for c in CHECKS])
def test_check(conn, name, query, expected):
    rows = conn.execute(query).fetchall()
    assert len(rows) == expected, f"{name}: {len(rows)} bad rows, first ones: {rows[:3]}"

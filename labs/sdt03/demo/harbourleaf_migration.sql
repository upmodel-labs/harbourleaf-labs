-- harbourleaf_migration.sql · Harbourleaf practice data for "Database Testing in Practice"
-- Fictional training data. Safe to run again: it drops and rebuilds the schema hl_check.
-- Run in pgAdmin (Query Tool, F5) or: psql -d labs -f harbourleaf_migration.sql

DROP SCHEMA IF EXISTS hl_check CASCADE;
CREATE SCHEMA hl_check;

-- ---------- The courier-status migration ----------
CREATE TABLE hl_check.shipments_old (
  shipment_id INTEGER PRIMARY KEY,
  order_id    INTEGER NOT NULL,
  status_old  TEXT NOT NULL,
  updated_at  TIMESTAMP NOT NULL
);
INSERT INTO hl_check.shipments_old (shipment_id, order_id, status_old, updated_at)
SELECT n, 70000 + n,
       CASE
         WHEN n % 337 = 0 THEN 'DELIVERED_PARTIAL'
         WHEN n % 10 IN (0, 1, 2, 3, 4) THEN 'DELIVERED'
         WHEN n % 10 IN (5, 6) THEN 'IN_TRANSIT'
         WHEN n % 10 = 7 THEN 'OUT_FOR_DELIVERY'
         WHEN n % 10 = 8 THEN 'PICKED_UP'
         ELSE 'RETURNED'
       END,
       TIMESTAMP '2026-10-05 08:00' + (n % 500) * INTERVAL '7 minutes'
FROM generate_series(1, 12480) AS n;

-- The mapping table the migration used
CREATE TABLE hl_check.status_map (
  status_old TEXT PRIMARY KEY,
  status_new TEXT NOT NULL
);
INSERT INTO hl_check.status_map (status_old, status_new) VALUES
  ('DELIVERED', 'DELIVERED'),
  ('IN_TRANSIT', 'IN_TRANSIT'),
  ('OUT_FOR_DELIVERY', 'OUT_FOR_DELIVERY'),
  ('PICKED_UP', 'COLLECTED'),
  ('RETURNED', 'RETURNED');

-- After the migration
CREATE TABLE hl_check.shipments (
  shipment_id INTEGER PRIMARY KEY,
  order_id    INTEGER NOT NULL,
  status      TEXT NOT NULL DEFAULT 'IN_TRANSIT',
  updated_at  TIMESTAMP NOT NULL
);
INSERT INTO hl_check.shipments (shipment_id, order_id, status, updated_at)
SELECT o.shipment_id, o.order_id, COALESCE(m.status_new, 'IN_TRANSIT'), o.updated_at
FROM hl_check.shipments_old o
LEFT JOIN hl_check.status_map m ON m.status_old = o.status_old;

-- ---------- An evaluation run ----------
CREATE TABLE hl_check.eval_runs (
  run_id       TEXT PRIMARY KEY,
  slice        TEXT NOT NULL,
  scored_count INTEGER NOT NULL,
  correct      INTEGER NOT NULL
);
INSERT INTO hl_check.eval_runs VALUES ('R-1011', 'regression', 240, 222);

CREATE TABLE hl_check.run_questions (
  run_id      TEXT NOT NULL REFERENCES hl_check.eval_runs (run_id),
  question_id INTEGER NOT NULL,
  PRIMARY KEY (run_id, question_id)
);
INSERT INTO hl_check.run_questions SELECT 'R-1011', 3000 + n FROM generate_series(1, 240) AS n;

CREATE TABLE hl_check.answers (
  answer_id   INTEGER PRIMARY KEY,
  run_id      TEXT NOT NULL,
  question_id INTEGER NOT NULL,
  score       SMALLINT NOT NULL
);
INSERT INTO hl_check.answers (answer_id, run_id, question_id, score)
SELECT n, 'R-1011', 3000 + n, CASE WHEN n % 16 = 0 THEN 0 ELSE 1 END
FROM generate_series(1, 240) AS n
WHERE n NOT IN (58, 131, 207);

-- The translation question set
CREATE TABLE hl_check.translation_questions (
  question_id INTEGER PRIMARY KEY,
  language    TEXT NOT NULL,
  question    TEXT NOT NULL,
  version     TEXT NOT NULL
);
INSERT INTO hl_check.translation_questions
SELECT n, CASE WHEN n % 4 = 0 THEN 'fr-CA' ELSE 'en' END, 'Regression question ' || (n - (n > 118)::INT * 2), 'v4'
FROM generate_series(1, 120) AS n;
UPDATE hl_check.translation_questions SET language = 'EN' WHERE question_id IN (33, 77);

-- ---------- Attack runs and the reply log ----------
CREATE TABLE hl_check.attack_runs (
  run_id      TEXT PRIMARY KEY,
  started_at  TIMESTAMP NOT NULL,
  finished_at TIMESTAMP
);
INSERT INTO hl_check.attack_runs VALUES
  ('A-1001', '2026-10-01 22:00', '2026-10-01 23:40'),
  ('A-1002', '2026-10-02 22:00', NULL),
  ('A-1003', '2026-10-03 22:00', '2026-10-04 00:10'),
  ('A-1004', '2026-10-04 22:00', NULL),
  ('A-1005', '2026-10-06 22:00', NULL);

CREATE TABLE hl_check.responses (
  response_id INTEGER PRIMARY KEY,
  created_at  TIMESTAMP NOT NULL,
  source      TEXT NOT NULL,
  reply_text  TEXT NOT NULL
);
INSERT INTO hl_check.responses (response_id, created_at, source, reply_text)
SELECT n,
       TIMESTAMP '2026-10-05 09:00' + n * INTERVAL '20 minutes',
       CASE WHEN TIMESTAMP '2026-10-05 09:00' + n * INTERVAL '20 minutes' >= TIMESTAMP '2026-10-06 14:00' THEN 'assistant_v8' ELSE 'assistant_v7' END,
       'Your order ' || (61000 + n) || ' is on its way.'
FROM generate_series(1, 288) AS n;
UPDATE hl_check.responses
SET reply_text = 'I have updated the contact for order ' || (61000 + response_id) || ' to buyer' || response_id || '@mailbox.com.'
WHERE response_id IN (92, 101, 117, 125, 140, 151, 166, 178, 190, 203, 219, 236, 255, 281);

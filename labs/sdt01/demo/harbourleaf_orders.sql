-- harbourleaf_orders.sql · Harbourleaf practice data for "SQL Queries & Joins for Testers"
-- Fictional training data. Safe to run again: it drops and rebuilds its own three schemas.
-- Run in pgAdmin (Query Tool, F5) or: psql -d labs -f harbourleaf_orders.sql

DROP SCHEMA IF EXISTS harbourleaf CASCADE;
DROP SCHEMA IF EXISTS eval CASCADE;
DROP SCHEMA IF EXISTS redteam CASCADE;
CREATE SCHEMA harbourleaf;
CREATE SCHEMA eval;
CREATE SCHEMA redteam;

-- ---------- Orders ----------
CREATE TABLE harbourleaf.customers (
  customer_id INTEGER PRIMARY KEY,
  full_name   TEXT NOT NULL,
  city        TEXT,
  country     TEXT NOT NULL
);
INSERT INTO harbourleaf.customers (customer_id, full_name, city, country)
SELECT n,
       'Customer ' || n,
       (ARRAY['Bengaluru','Pune','Delhi','Mumbai','Chennai','Toronto','Montreal','Vancouver'])[1 + n % 8],
       CASE WHEN n % 8 >= 5 THEN 'CA' ELSE 'IN' END
FROM generate_series(1, 400) AS n;

CREATE TABLE harbourleaf.products (
  product_id INTEGER PRIMARY KEY,
  name       TEXT NOT NULL,
  category   TEXT NOT NULL,
  price      NUMERIC(10,2) NOT NULL
);
INSERT INTO harbourleaf.products (product_id, name, category, price)
SELECT n,
       (ARRAY['Lamp','Cushion','Rug','Vase','Throw','Mirror'])[1 + n % 6] || ' ' || n,
       (ARRAY['lighting','textiles','textiles','decor','textiles','decor'])[1 + n % 6],
       (400 + (n * 137) % 2600)::NUMERIC(10,2)
FROM generate_series(1, 30) AS n;

-- Seven days of orders, 2026-09-28 to 2026-10-04
CREATE TABLE harbourleaf.orders (
  order_id       INTEGER PRIMARY KEY,
  customer_id    INTEGER NOT NULL REFERENCES harbourleaf.customers (customer_id),
  order_date     DATE NOT NULL,
  status         TEXT NOT NULL,
  delivery_phone TEXT,
  total          NUMERIC(10,2) NOT NULL DEFAULT 0
);
WITH days AS (
  SELECT d, day_count,
         SUM(day_count) OVER (ORDER BY d) - day_count AS before
  FROM (VALUES (1, 1910), (2, 1985), (3, 2030), (4, 1876), (5, 2240), (6, 2380), (7, 2140)) AS v(d, day_count)
)
INSERT INTO harbourleaf.orders (order_id, customer_id, order_date, status, delivery_phone)
SELECT 50000 + before + k,
       1 + ((before + k) * 7) % 400,
       DATE '2026-09-27' + d,
       'delivered',
       CASE WHEN (1 + ((before + k) * 7) % 400) % 8 >= 5
            THEN '+1 416 ' || lpad(((before + k) * 7919 % 10000000)::TEXT, 7, '0')
            ELSE '+91 98' || lpad(((before + k) * 7919 % 100000000)::TEXT, 8, '0') END
FROM days, generate_series(1, day_count) AS k;

-- Statuses for 2026-10-04
WITH y AS (
  SELECT order_id, ROW_NUMBER() OVER (ORDER BY order_id) AS rn
  FROM harbourleaf.orders WHERE order_date = DATE '2026-10-04'
)
UPDATE harbourleaf.orders o
SET status = CASE WHEN y.rn <= 1860 THEN 'shipped'
                  WHEN y.rn <= 2040 THEN 'packed'
                  WHEN y.rn <= 2110 THEN 'placed'
                  ELSE 'cancelled' END
FROM y WHERE o.order_id = y.order_id;

UPDATE harbourleaf.orders SET delivery_phone = NULL
WHERE order_id IN (SELECT order_id FROM harbourleaf.orders WHERE order_date = DATE '2026-10-04' ORDER BY order_id OFFSET 101 LIMIT 6);
UPDATE harbourleaf.orders SET delivery_phone = ''
WHERE order_id IN (SELECT order_id FROM harbourleaf.orders WHERE order_date = DATE '2026-10-04' ORDER BY order_id OFFSET 1501 LIMIT 2);

-- One to three items per order; the order total is the sum of its items
CREATE TABLE harbourleaf.order_items (
  item_id    INTEGER PRIMARY KEY,
  order_id   INTEGER NOT NULL REFERENCES harbourleaf.orders (order_id),
  product_id INTEGER NOT NULL REFERENCES harbourleaf.products (product_id),
  quantity   INTEGER NOT NULL,
  unit_price NUMERIC(10,2) NOT NULL
);
INSERT INTO harbourleaf.order_items (item_id, order_id, product_id, quantity, unit_price)
SELECT ROW_NUMBER() OVER (ORDER BY o.order_id, i),
       o.order_id,
       p.product_id,
       1 + (o.order_id * i) % 3,
       p.price + (o.order_id * i) % 97
FROM harbourleaf.orders o
CROSS JOIN generate_series(1, 3) AS i
JOIN harbourleaf.products p ON p.product_id = 1 + (o.order_id * 7 + i * 13) % 30
WHERE i <= 1 + o.order_id % 3;
UPDATE harbourleaf.orders o
SET total = t.sum_items
FROM (SELECT order_id, SUM(quantity * unit_price) AS sum_items FROM harbourleaf.order_items GROUP BY order_id) t
WHERE o.order_id = t.order_id;

-- Courier scans
CREATE TABLE harbourleaf.shipments (
  shipment_id INTEGER PRIMARY KEY,
  order_id    INTEGER NOT NULL REFERENCES harbourleaf.orders (order_id),
  courier     TEXT NOT NULL,
  scanned_at  TIMESTAMP NOT NULL
);
INSERT INTO harbourleaf.shipments (shipment_id, order_id, courier, scanned_at)
SELECT ROW_NUMBER() OVER (ORDER BY o.order_id),
       o.order_id,
       (ARRAY['BlueDart','Delhivery','Canada Post'])[1 + o.order_id % 3],
       o.order_date + TIME '18:00' + (o.order_id % 300) * INTERVAL '1 minute'
FROM harbourleaf.orders o
WHERE o.status IN ('shipped', 'delivered')
  AND o.order_id NOT IN (
    SELECT order_id FROM harbourleaf.orders
    WHERE order_date = DATE '2026-10-04' AND status = 'shipped'
    ORDER BY order_id OFFSET 400 LIMIT 23);

-- ---------- Model answers ----------
-- score: 1 = correct, 0 = wrong, NULL = not scored yet
CREATE TABLE eval.answers (
  answer_id   INTEGER PRIMARY KEY,
  run_id      TEXT NOT NULL,
  language    TEXT NOT NULL,
  question_id INTEGER NOT NULL,
  score       SMALLINT
);
INSERT INTO eval.answers (answer_id, run_id, language, question_id, score)
SELECT n, 'E-0921', 'en', 1000 + n,
       CASE WHEN n <= 100 THEN 1 WHEN n <= 108 THEN 0 ELSE NULL END
FROM generate_series(1, 120) AS n;
INSERT INTO eval.answers (answer_id, run_id, language, question_id, score)
SELECT 200 + n, 'E-0922',
       CASE WHEN n <= 60 THEN 'fr-CA' ELSE 'hi' END,
       2000 + n,
       CASE WHEN n % 10 = 0 THEN 0 ELSE 1 END
FROM generate_series(1, 108) AS n;

-- ---------- Attack logs ----------
-- mentioned_order_id = the order id a reply talks about, if any
CREATE TABLE redteam.attacks (
  attack_id INTEGER PRIMARY KEY,
  category  TEXT NOT NULL
);
INSERT INTO redteam.attacks (attack_id, category)
SELECT n, (ARRAY['order lookup','prompt injection','refund abuse','data probe'])[1 + n % 4]
FROM generate_series(1, 36) AS n;

CREATE TABLE redteam.responses (
  response_id         INTEGER PRIMARY KEY,
  attack_id           INTEGER NOT NULL REFERENCES redteam.attacks (attack_id),
  session_customer_id INTEGER NOT NULL,
  mentioned_order_id  INTEGER
);
INSERT INTO redteam.responses (response_id, attack_id, session_customer_id, mentioned_order_id)
SELECT a.attack_id,
       a.attack_id,
       c.customer_id,
       (SELECT MAX(o.order_id) FROM harbourleaf.orders o WHERE o.customer_id = c.customer_id)
FROM redteam.attacks a
JOIN harbourleaf.customers c ON c.customer_id = 10 + a.attack_id * 3;
INSERT INTO redteam.responses (response_id, attack_id, session_customer_id, mentioned_order_id)
SELECT 100 + a.attack_id, a.attack_id, 10 + a.attack_id * 3, NULL
FROM redteam.attacks a WHERE a.attack_id % 3 = 0 AND a.attack_id <= 33;
UPDATE redteam.responses r
SET mentioned_order_id = (SELECT MAX(o.order_id) FROM harbourleaf.orders o WHERE o.customer_id = r.session_customer_id + 1)
WHERE r.response_id IN (5, 17, 29);
UPDATE redteam.responses SET mentioned_order_id = 99104 WHERE response_id = 8;
UPDATE redteam.responses SET mentioned_order_id = 99377 WHERE response_id = 23;

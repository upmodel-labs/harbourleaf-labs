#!/usr/bin/env python3
"""The practice bookshop's web shop, for the test-automation-python-stack labs (HLF-P61 to HLF-P65).

A tiny web shop made only for these labs. It holds no real data and is not connected to anything.
It is the practice bookshop, separate from Harbourleaf. Run it only inside your own Codespace or laptop.

Standard library only (Python 3.10 or newer). Start it with:
    python webshop/server.py                 web shop v1 on http://localhost:8000
    python webshop/server.py --version v2    web shop v2 (chapter 3: renamed button, moved search box)
    python webshop/server.py --slow          every answer takes 1.5 to 3 seconds (shows why fixed sleeps fail)

Pages:  /  (search)  /book.html?id=b1  /basket.html  /help.html  /orders.html
API:    GET  /health                 answers at once
        GET  /api/books?q=word       search titles and authors (answers after a short delay)
        GET  /api/books/<id>         one book
        GET  /api/help?order=BK-1001 the order help box reply (one of several wordings, chosen at random)
        GET  /api/orders             every order placed since the server started (one shared list)
        POST /api/orders             place an order; body {"lines": [{"id": "b1", "qty": 2}]}
        POST /api/reset              empty the shared order list

Options:
    --port 8000     the port to listen on
    --version v1    which version of the pages to serve (v1 or v2)
    --slow          slow answers on purpose
    --seed N        fix the random wording and delays, so a run can be repeated
"""
import argparse
import json
import random
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

HERE = Path(__file__).resolve().parent
BOOKS = json.loads((HERE / "data" / "books.json").read_text(encoding="utf-8"))
ORDERS = json.loads((HERE / "data" / "orders.json").read_text(encoding="utf-8"))
YOU = ORDERS["you"]
HELP_ORDERS = {o["id"]: o for o in ORDERS["orders"]}

DELAY = {"normal": (0.2, 0.8), "slow": (1.5, 3.0)}   # seconds an API answer takes
ECHO_MAX = 40                                         # the help box repeats at most this many characters

REPLY_OWN = [
    "Order {id} is {status}.",
    "Good news: your order {id} is {status}.",
    "I checked order {id} for you. Its status is {status}.",
    "Your order {id}: {status}. I'll update you here if that changes.",
]
REPLY_UNKNOWN = [
    "I can't find order {id}. Please check the number and try again.",
    "There is no order {id} on your account. Could you check the number?",
    "I couldn't find {id}. Order numbers look like BK-1001.",
]
REPLY_OTHER = [
    "I can't share details of order {id}.",
    "Order {id} isn't on your account, so I can't share anything about it.",
]
REPLY_EMPTY = ["Please type your order number, for example BK-1001."]

TYPES = {".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
         ".js": "text/javascript; charset=utf-8", ".json": "application/json; charset=utf-8"}

args = None
rng = random.Random()
lock = threading.Lock()
placed = []          # the shared order list (one per server, on purpose)
next_number = [2001]


def pause():
    low, high = DELAY["slow" if args.slow else "normal"]
    with lock:
        seconds = rng.uniform(low, high)
    time.sleep(seconds)


def pick(options):
    with lock:
        return rng.choice(options)


def help_reply(raw):
    order_id = (raw or "").strip()
    shown = order_id if len(order_id) <= ECHO_MAX else order_id[:ECHO_MAX] + "..."
    if not order_id:
        return {"reply": pick(REPLY_EMPTY), "kind": "empty"}
    order = HELP_ORDERS.get(order_id.upper())
    if order is None:
        return {"reply": pick(REPLY_UNKNOWN).format(id=shown), "kind": "unknown"}
    if order["customer"] != YOU:
        return {"reply": pick(REPLY_OTHER).format(id=order["id"]), "kind": "other"}
    return {"reply": pick(REPLY_OWN).format(id=order["id"], status=order["status"]), "kind": "own"}


class Shop(BaseHTTPRequestHandler):
    server_version = "PracticeWebShop/1.0"

    def log_message(self, fmt, *a):
        pass   # keep the terminal quiet; tests print their own output

    def send(self, code, body, ctype="application/json; charset=utf-8"):
        data = body if isinstance(body, bytes) else json.dumps(body).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        url = urlparse(self.path)
        q = parse_qs(url.query)
        p = url.path
        if p == "/health":
            return self.send(200, {"ok": True, "version": args.version, "slow": args.slow})
        if p == "/api/books":
            pause()
            word = (q.get("q", [""])[0]).strip().lower()
            hits = [b for b in BOOKS if word and (word in b["title"].lower() or word in b["author"].lower())]
            return self.send(200, {"query": word, "results": hits})
        if p.startswith("/api/books/"):
            pause()
            book = next((b for b in BOOKS if b["id"] == p.rsplit("/", 1)[1]), None)
            return self.send(200, book) if book else self.send(404, {"error": "no such book"})
        if p == "/api/help":
            pause()
            return self.send(200, help_reply(q.get("order", [""])[0]))
        if p == "/api/orders":
            with lock:
                return self.send(200, {"orders": list(placed)})
        return self.static(p)

    def do_POST(self):
        p = urlparse(self.path).path
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b"{}"
        if p == "/api/reset":
            with lock:
                placed.clear()
            return self.send(200, {"ok": True})
        if p == "/api/orders":
            try:
                lines = json.loads(raw or b"{}").get("lines", [])
            except (ValueError, AttributeError):
                return self.send(400, {"error": "body must be JSON"})
            prices = {b["id"]: b["price"] for b in BOOKS}
            clean = [{"id": l["id"], "qty": int(l["qty"])} for l in lines
                     if isinstance(l, dict) and l.get("id") in prices and 1 <= int(l.get("qty", 0)) <= 10]
            if not clean:
                return self.send(400, {"error": "the basket is empty"})
            pause()
            with lock:
                order = {"number": f"BK-{next_number[0]}", "lines": clean,
                         "total": round(sum(prices[l["id"]] * l["qty"] for l in clean), 2)}
                next_number[0] += 1
                placed.append(order)
            return self.send(201, order)
        return self.send(404, {"error": "not found"})

    def static(self, p):
        if p in ("", "/"):
            p = "/index.html"
        if p.startswith("/static/"):
            base, rel = HERE / "static", p[len("/static/"):]
        else:
            base, rel = HERE / args.version, p.lstrip("/")
        target = (base / rel).resolve()
        if base.resolve() not in target.parents or not target.is_file():
            return self.send(404, b"<h1>Not found</h1>", "text/html; charset=utf-8")
        return self.send(200, target.read_bytes(), TYPES.get(target.suffix, "application/octet-stream"))


class QuietServer(ThreadingHTTPServer):
    """A browser that closes a connection mid-answer is normal. Do not print a traceback for it."""

    def handle_error(self, request, client_address):
        if isinstance(sys.exc_info()[1], (BrokenPipeError, ConnectionResetError, ConnectionAbortedError)):
            return
        super().handle_error(request, client_address)


def main():
    global args
    ap = argparse.ArgumentParser(description="The practice bookshop's web shop (labs only).")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--version", choices=["v1", "v2"], default="v1")
    ap.add_argument("--slow", action="store_true")
    ap.add_argument("--seed", type=int)
    args = ap.parse_args()
    if args.seed is not None:
        rng.seed(args.seed)
    httpd = QuietServer(("0.0.0.0", args.port), Shop)
    print(f"Practice web shop {args.version}{' (slow)' if args.slow else ''} on http://localhost:{args.port}  (Ctrl+C to stop)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()

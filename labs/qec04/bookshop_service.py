#!/usr/bin/env python3
"""The practice online bookshop service for lab qec04 (HLF-P54).

A tiny web service made only for this lab. It holds no data and is not connected to anything. It has a known
limit on purpose: ONE worker, so it handles one request at a time. When requests arrive faster than the worker
can finish them, they queue and the response time climbs. A request that waits more than 4 seconds gets a
503 reply instead.

Only load-test this service, which you run yourself. Never point a load test at a site you do not own.

Standard library only. Start it with:    python bookshop_service.py
Then check it:                           curl http://localhost:8080/health   (in Codespaces use the Ports tab for a browser)

Endpoints
    GET  /health     answers at once, never queues (use it to see that the service is up)
    GET  /books      browse: a short list of books
    POST /basket     add the Bundle & Save offer to the basket; the reply holds the saving and a cart message
                     body (JSON, optional): {"items": 2, "note": "a gift note"}
    POST /checkout   pay for the basket

Options (all optional)
    --port 8080      the port to listen on
    --workers 1      how many requests are handled at once (1 is the lab setting)
    --no-saving      leave the saving out of the basket reply, so you can prove your response check catches it
"""
import argparse
import json
import math
import random
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SERVICE_MS = {"browse": 250, "basket": 450, "checkout": 900}   # average time to do the work, in milliseconds
JITTER = 0.25                                                  # how much that time varies from request to request
QUEUE_TIMEOUT = 4.0                                            # seconds a request waits for the worker, then 503
NOTE_SECONDS_PER_CHAR = 1 / 4000                               # the cart note has no limit on purpose (Attack logs track)
NOTE_MAX_CHARS = 20000

BOOKS = [
    {"id": "b1", "title": "Learning to Test", "price": 18},
    {"id": "b2", "title": "The Slow Page", "price": 14},
    {"id": "b3", "title": "Queues and Lines", "price": 21},
    {"id": "b4", "title": "A Small Guide to Percentiles", "price": 12},
]

args = None
worker = None
rng = random.Random()


def do_work(kind, extra_seconds=0.0):
    """Wait for the worker, 'work' for a moment, give the worker back. Returns False if the wait ran out."""
    if not worker.acquire(timeout=QUEUE_TIMEOUT):
        return False
    try:
        spread = math.exp(rng.gauss(0, JITTER) - JITTER ** 2 / 2)
        time.sleep(SERVICE_MS[kind] / 1000 * spread + extra_seconds)
    finally:
        worker.release()
    return True


def cart_message(items):
    """A plain template. In the story a model writes this line; here nothing needs a model."""
    word = "book" if items == 1 else "books"
    return f"You have {items} {word} in your basket, and the Bundle & Save offer is applied."


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *a):   # keep the terminal quiet while the load runs
        pass

    def send_json(self, status, body):
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def read_json(self):
        n = int(self.headers.get("Content-Length") or 0)
        if not n:
            return {}
        try:
            return json.loads(self.rfile.read(n) or b"{}")
        except ValueError:
            return {}

    def busy(self):
        self.send_json(503, {"error": "busy, try again"})

    def do_GET(self):
        if self.path == "/health":
            self.send_json(200, {"status": "up", "workers": args.workers})
        elif self.path == "/books":
            self.send_json(200, {"books": BOOKS}) if do_work("browse") else self.busy()
        else:
            self.send_json(404, {"error": "not found"})

    def do_POST(self):
        body = self.read_json()
        if self.path == "/basket":
            items = body.get("items", 1)
            items = items if isinstance(items, int) and items > 0 else 1
            note = str(body.get("note", ""))[:NOTE_MAX_CHARS]
            if not do_work("basket", len(note) * NOTE_SECONDS_PER_CHAR):
                return self.busy()
            reply = {"items": items, "message": cart_message(items)}
            if not args.no_saving:
                reply["saving_percent"] = 10
            self.send_json(200, reply)
        elif self.path == "/checkout":
            self.send_json(200, {"status": "paid"}) if do_work("checkout") else self.busy()
        else:
            self.send_json(404, {"error": "not found"})


def main():
    global args, worker
    p = argparse.ArgumentParser(description="Practice bookshop service for lab qec04")
    p.add_argument("--port", type=int, default=8080)
    p.add_argument("--workers", type=int, default=1)
    p.add_argument("--no-saving", action="store_true")
    args = p.parse_args()
    worker = threading.Semaphore(args.workers)
    server = ThreadingHTTPServer(("0.0.0.0", args.port), Handler)
    server.daemon_threads = True
    server.request_queue_size = 128
    print(f"Practice bookshop running on http://localhost:{args.port} with {args.workers} worker(s). Stop it with Ctrl+C.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopped.")


if __name__ == "__main__":
    main()

"""Starter locustfile for lab qec04, step 3 (HLF-P54: the Bundle & Save second-run load test).

Your job in this file:
  1. Fill in the five values below from your workload model (step 2).
  2. In the basket task, add a response check: mark the reply as failed when a normal (200) reply is missing the saving.

Run it (service already started in the other terminal):
    locust -f locustfile.py --host http://localhost:8080
Then open the Locust page (port 8089), set 1 user, and start.

Locust documentation: https://docs.locust.io/en/stable/
Only ever run this against the practice service on your own machine or Codespace.
"""
import random

from locust import HttpUser, between, task

# ---- Step 3, part 1: fill in these five values from your step 2 table.
WEIGHT_BROWSE = None
WEIGHT_BASKET = None
WEIGHT_CHECKOUT = None
THINK_MIN_SECONDS = None
THINK_MAX_SECONDS = None

_missing = [name for name, value in [
    ("WEIGHT_BROWSE", WEIGHT_BROWSE), ("WEIGHT_BASKET", WEIGHT_BASKET), ("WEIGHT_CHECKOUT", WEIGHT_CHECKOUT),
    ("THINK_MIN_SECONDS", THINK_MIN_SECONDS), ("THINK_MAX_SECONDS", THINK_MAX_SECONDS)] if value is None]
if _missing:
    raise ValueError("Step 3 is not finished yet. Fill in these values at the top of locustfile.py: " + ", ".join(_missing))


class Shopper(HttpUser):
    """One virtual user: a shopper who pauses, then does one thing, then pauses again."""

    wait_time = between(THINK_MIN_SECONDS, THINK_MAX_SECONDS)

    @task(WEIGHT_BROWSE)
    def browse(self):
        self.client.get("/books", name="browse")

    @task(WEIGHT_BASKET)
    def add_bundle_to_basket(self):
        with self.client.post("/basket", json={"items": random.randint(1, 3)}, name="basket", catch_response=True) as reply:
            # ---- Step 3, part 2: add the response check here.
            # The reply body is JSON: reply.json() gives you a dictionary. The saving is the field "saving_percent".
            # Check the saving ONLY when reply.status_code == 200. A 503 "busy" reply has no saving either, but that is a
            # different fault (the queue limit), and Locust already reports it as its own failed request.
            # When a 200 reply is missing the saving, call reply.failure("...") with a short message. Otherwise do nothing.
            pass

    @task(WEIGHT_CHECKOUT)
    def checkout(self):
        self.client.post("/checkout", json={}, name="checkout")

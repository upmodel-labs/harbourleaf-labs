"""A fake Harbourleaf booking assistant for the demos: deterministic, no model.

respond(request) returns {"reply": text, "decision": {"action", "slot_id", "visit_date"}}.
Flags switch the demo's defects on: "bad_replies" makes two of the 112 requests
return replies that still contain the word "visit" but are wrong.
"""
PRODUCTS = ["Oakmere 4-shelf unit", "Halden 2-door wardrobe", "Tarn wall shelf", "Oakmere 4-shelf unit"]
SLOTS = ["S-201", "S-202", "S-203", "S-204"]
WHEN = ["Monday at 09:00", "Tuesday at 11:00", "Wednesday at 14:00", "Thursday at 16:00"]


def make_requests():
    """112 requests: 7 postal codes x 4 slots x 4 products."""
    codes = ["HB1 1AA", "HB2 2BB", "HB3 3CC", "HB4 4DD", "900001", "900002", "900003"]
    out = []
    n = 0
    for code in codes:
        for s in range(4):
            for p in range(4):
                n += 1
                out.append({"id": n, "postal_code": code, "product": PRODUCTS[p], "slot_id": SLOTS[s], "when": WHEN[s]})
    return out


class FakeBookingAssistant:
    def __init__(self, flags=()):
        self.flags = tuple(flags)

    def respond(self, request):
        rid = request["id"]
        if "bad_replies" in self.flags and rid == 41:
            return {"reply": "Sorry, I couldn't get that visit booked.",
                    "decision": {"action": "ask", "slot_id": None, "visit_date": None}}
        if "bad_replies" in self.flags and rid == 87:
            return {"reply": "Your visit is booked. Call the fitter direct on 07700 900123.",
                    "decision": {"action": "book", "slot_id": request["slot_id"], "visit_date": None}}
        return {"reply": "Your %s visit is booked for %s." % (request["product"], request["when"]),
                "decision": {"action": "book", "slot_id": request["slot_id"], "visit_date": None}}

"""The guard (demo): a repeated book_visit for the same slot and product does not reach the tool twice."""


class GuardedVisitTools:
    def __init__(self, inner):
        self.inner = inner
        self.seen = set()

    @property
    def trace(self):
        return self.inner.trace

    @property
    def visits(self):
        return self.inner.visits

    def check_area(self, postal_code):
        return self.inner.check_area(postal_code)

    def list_slots(self, product):
        return self.inner.list_slots(product)

    def cancel_visit(self, slot_id):
        return self.inner.cancel_visit(slot_id)

    def hand_over(self, reason):
        return self.inner.hand_over(reason)

    def book_visit(self, slot_id, product):
        key = (slot_id, product)
        if key in self.seen:
            return {"status": "ok", "duplicate_ignored": True}
        self.seen.add(key)
        return self.inner.book_visit(slot_id, product)

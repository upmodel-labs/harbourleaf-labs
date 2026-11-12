"""Step 6: a guard in the tool wrapper. It sits between the assistant and the tools.

A repeated add_followup (same member_key, text and due_date) must not reach the tool a second time.
Write add_followup below. The other methods pass straight through (given).
"""


class GuardedTools:
    def __init__(self, inner):
        self.inner = inner
        self.seen = {}

    @property
    def trace(self):
        return self.inner.trace

    @property
    def followups(self):
        return self.inner.followups

    def find_member(self, name):
        return self.inner.find_member(name)

    def post_summary(self, text):
        return self.inner.post_summary(text)

    def remove_member(self, member_key):
        return self.inner.remove_member(member_key)

    def add_followup(self, member_key, text, due_date):
        raise NotImplementedError("Step 6: write the guard here")

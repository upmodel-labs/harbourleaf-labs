"""Fake tools and fake agents for the agent behaviour labs (lov03).

No model is called and nothing waits: slowness is a simulated clock. Standard
library only. Practice data only. A seed makes a run repeatable; a different seed
can expose a different path.

Two worlds live here, kept apart:
  * Reading Group Notes (the Task):  FakeTools + ReadingGroupAgent
  * Harbourleaf assembly booking (the demo):  FakeVisitTools + VisitAgent
"""
import hashlib
import re
from dataclasses import dataclass, field


class SimClock:
    """A clock that only moves when told to. Tests never really wait."""

    def __init__(self):
        self.now = 0.0

    def sleep(self, seconds):
        self.now += seconds


# ---------------------------------------------------------------- seeded delay
FAST_DELAY_S = 1.0
SLOW_DELAY_S = 4.0
WAIT_LIMIT_S = 3.0          # the agent gives up waiting after this many simulated seconds
STEP_LIMIT = 6              # the agent stops with a reply after this many tool calls


def is_slow(seed, salt, percent):
    """Deterministic rule: the same seed always gives the same answer."""
    return (seed * 37 + salt) % 100 < percent


TASK_SALT, TASK_SLOW_PERCENT = 5, 30    # Reading Group Notes: add_followup
DEMO_SALT, DEMO_SLOW_PERCENT = 7, 20    # Harbourleaf: book_visit


def member_key(name, copy=0):
    """An opaque, stable key. Tests must not depend on how it is built."""
    return "mem-" + hashlib.sha1(("%s/%d" % (name, copy)).encode()).hexdigest()[:6]


DIRECTORY = [{"key": member_key(n), "name": n} for n in ["Sam", "Ines", "Tomas", "Wren", "Odile", "Kofi"]]
TWO_SAMS = [{"key": member_key("Sam", 1), "name": "Sam"}, {"key": member_key("Sam", 2), "name": "Sam"}]

_MONTHS = {m: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July",
                                       "August", "September", "October", "November", "December"], start=1)}
_TASK = re.compile(r"^(?P<name>[A-Z][a-z]+) to (?P<what>.+?) by (?P<day>\d{1,2}) (?P<month>[A-Za-z]+)\.$")
_LEAVING = re.compile(r"^(?P<name>[A-Z][a-z]+) is leaving the group(?: after (?P<day>\d{1,2}) (?P<month>[A-Za-z]+))?\.$")


class StepLimitReached(Exception):
    pass


@dataclass
class AgentResult:
    reply: str
    calls: list = field(default_factory=list)
    outcome: str = "done"          # done, asked, stopped

    def as_trace(self):
        return {"calls": self.calls, "reply": self.reply}


# ---------------------------------------------------------------- Reading Group Notes (Task)
class FakeTools:
    """find_member, add_followup, post_summary and remove_member, with a recorded trace.

    The assistant never calls remove_member: it is here so a test can assert it is absent.
    The first add_followup of a run is slow when the seed says so; the follow-up is still
    created, but the agent sees a timeout.
    """

    def __init__(self, seed=0, directory=None):
        self.seed = seed
        self.directory = [dict(m) for m in (directory or DIRECTORY)]
        self.clock = SimClock()
        self.trace = []
        self.followups = []
        self.summaries = []
        self.removed = []

    def _log(self, tool, args, result):
        self.trace.append({"tool": tool, "args": args, "result": result})
        return result

    def find_member(self, name):
        found = [dict(m) for m in self.directory if m["name"] == name]
        return self._log("find_member", {"name": name}, {"members": found})["members"]

    def add_followup(self, member_key, text, due_date):
        args = {"member_key": member_key, "text": text, "due_date": due_date}
        first = not self.followups
        slow = first and is_slow(self.seed, TASK_SALT, TASK_SLOW_PERCENT)
        self.clock.sleep(min(SLOW_DELAY_S if slow else FAST_DELAY_S, WAIT_LIMIT_S))
        self.followups.append(dict(args))
        if slow:
            return self._log("add_followup", args, {"status": "timeout"})
        return self._log("add_followup", args, {"status": "ok"})

    def post_summary(self, text):
        self.summaries.append(text)
        return self._log("post_summary", {"text": text}, {"status": "ok"})

    def remove_member(self, member_key):
        self.removed.append(member_key)
        return self._log("remove_member", {"member_key": member_key}, {"status": "ok"})


class ReadingGroupAgent:
    """Turns meeting notes into follow-ups. Flags switch defects on:
    guess_first_member  picks the first match when a name is ambiguous
    remove_leaving      calls remove_member for a member the notes say is leaving
    """

    def __init__(self, tools, flags=()):
        self.tools = tools
        self.flags = tuple(flags)
        self.steps = 0

    def _call(self, fn, *args):
        if self.steps >= STEP_LIMIT:
            raise StepLimitReached()
        self.steps += 1
        return fn(*args)

    def handle(self, notes):
        added = []
        try:
            for raw in (notes or "").splitlines():
                line = raw.strip()
                task = _TASK.match(line)
                leaving = _LEAVING.match(line)
                if task:
                    found = self._call(self.tools.find_member, task.group("name"))
                    if not found:
                        return self._finish("Who is %s?" % task.group("name"), "asked")
                    if len(found) > 1 and "guess_first_member" not in self.flags:
                        return self._finish("Which %s do you mean?" % task.group("name"), "asked")
                    due = "2026-%02d-%02d" % (_MONTHS[task.group("month")], int(task.group("day")))
                    res = self._call(self.tools.add_followup, found[0]["key"], task.group("what"), due)
                    if res.get("status") == "timeout":
                        self._call(self.tools.add_followup, found[0]["key"], task.group("what"), due)
                    added.append("%s: %s, due %s" % (task.group("name"), task.group("what"), due))
                elif leaving and "remove_leaving" in self.flags:
                    found = self._call(self.tools.find_member, leaving.group("name"))
                    if found:
                        self._call(self.tools.remove_member, found[0]["key"])
            summary = "%d follow-up%s: %s" % (len(added), "" if len(added) == 1 else "s", "; ".join(added)) \
                if added else "No follow-ups from these notes."
            self._call(self.tools.post_summary, summary)
            return self._finish("Done. " + summary, "done")
        except StepLimitReached:
            return self._finish("I stopped: too many tool calls.", "stopped")

    def _finish(self, reply, outcome):
        return AgentResult(reply=reply, calls=[dict(c) for c in self.tools.trace], outcome=outcome)


# ---------------------------------------------------------------- Harbourleaf assembly booking (demo)
SERVICE_AREA = {"HB1 1AA", "HB2 2BB", "HB3 3CC", "HB4 4DD", "900001", "900002", "900003"}
SATURDAY_SLOT = "S-301"
SLOTS = [{"slot_id": SATURDAY_SLOT, "day": "Saturday"}, {"slot_id": "S-302", "day": "Sunday"}]


class FakeVisitTools:
    """check_area, list_slots, book_visit, cancel_visit and hand_over, with a recorded trace.

    book_visit is slow on the first call when the seed says so: the visit is still booked,
    but the agent sees a timeout. The delay is a simulated clock; nothing really waits.
    """

    def __init__(self, seed=0):
        self.seed = seed
        self.clock = SimClock()
        self.trace = []
        self.visits = []

    def _log(self, tool, args, result):
        self.trace.append({"tool": tool, "args": args, "result": result})
        return result

    def check_area(self, postal_code):
        return self._log("check_area", {"postal_code": postal_code}, {"in_area": postal_code in SERVICE_AREA})

    def list_slots(self, product):
        return self._log("list_slots", {"product": product}, {"slots": [dict(s) for s in SLOTS]})

    def book_visit(self, slot_id, product):
        args = {"slot_id": slot_id, "product": product}
        slow = not self.visits and is_slow(self.seed, DEMO_SALT, DEMO_SLOW_PERCENT)
        self.clock.sleep(min(SLOW_DELAY_S if slow else FAST_DELAY_S, WAIT_LIMIT_S))
        self.visits.append(dict(args))
        return self._log("book_visit", args, {"status": "timeout" if slow else "ok"})

    def cancel_visit(self, slot_id):
        return self._log("cancel_visit", {"slot_id": slot_id}, {"status": "ok"})

    def hand_over(self, reason):
        return self._log("hand_over", {"reason": reason}, {"status": "ok"})


class VisitAgent:
    """Books an assembly visit. Every reply to a booked customer reads the same, which is the point:
    a reply-only test cannot tell a single booking from a double one."""

    def __init__(self, tools):
        self.tools = tools
        self.steps = 0

    def _call(self, fn, *args):
        if self.steps >= STEP_LIMIT:
            raise StepLimitReached()
        self.steps += 1
        return fn(*args)

    def handle(self, request):
        try:
            area = self._call(self.tools.check_area, request["postal_code"])
            if not area["in_area"]:
                return self._finish("Sorry, we do not cover that area yet.", "declined")
            slots = self._call(self.tools.list_slots, request["product"])["slots"]
            slot = next(s for s in slots if s["day"] == request["day"])
            res = self._call(self.tools.book_visit, slot["slot_id"], request["product"])
            if res["status"] == "timeout":
                self._call(self.tools.book_visit, slot["slot_id"], request["product"])
            return self._finish("You're booked for %s." % request["day"], "done")
        except StepLimitReached:
            return self._finish("I stopped: too many tool calls.", "stopped")

    def _finish(self, reply, outcome):
        return AgentResult(reply=reply, calls=[dict(c) for c in self.tools.trace], outcome=outcome)

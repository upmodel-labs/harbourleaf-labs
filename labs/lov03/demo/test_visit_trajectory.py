"""The demo's trajectory tests (Harbourleaf assembly booking). Run: python -m pytest -q"""
import pytest

from lovkit import trajectory as T
from run_thirty import thirty_runs
from visit_demo import OUTSIDE_AREA, SCENARIOS, run_visit
from visit_guard import GuardedVisitTools

STEP_LIMIT = 6
HAPPY = SCENARIOS[0][1]


def booked_trace(seed=1, request=HAPPY, guard=None):
    tools, result = run_visit(request, seed, guard)
    return result.as_trace()


# 1:30 · a fake slow tool, swapped in with monkeypatch
def test_a_slow_book_visit_makes_the_agent_book_again(monkeypatch):
    from lovkit.agent_tools import FakeVisitTools
    real = FakeVisitTools.book_visit

    def slow_first_call(self, slot_id, product):
        result = real(self, slot_id, product)
        return {"status": "timeout"} if len(self.visits) == 1 else result

    monkeypatch.setattr(FakeVisitTools, "book_visit", slow_first_call)
    trace = booked_trace()
    assert T.names(trace).count("book_visit") == 2


# 2:30 · the six assertions, and the trace printed on failure
def test_the_six_assertions_on_the_happy_path():
    trace = booked_trace()
    T.must(T.called(trace, "check_area"), trace)
    T.must(T.not_called(trace, "cancel_visit"), trace)
    T.must(T.order(trace, "check_area", "book_visit"), trace)
    T.must(T.count(trace, "book_visit", 1), trace)
    T.must(T.argument(trace, "book_visit", "slot_id", "S-301"), trace)
    T.must(T.terminates(trace, STEP_LIMIT), trace)


def test_the_trace_is_printed_when_an_assertion_fails():
    trace = booked_trace(seed=0)                      # a slow seed
    with pytest.raises(AssertionError) as error:
        T.must(T.count(trace, "book_visit", 1), trace)
    assert "book_visit" in str(error.value) and "trace (" in str(error.value)


# 2:00 · the deliberate error: run once and call it passing
def test_run_once_and_call_it_passing():
    trace = booked_trace(seed=1)
    assert "booked" in trace["reply"]                 # the reply-only view
    assert T.count(trace, "book_visit", 1).ok         # one run, one fast seed


def test_thirty_runs_expose_the_duplicate_call():
    rows = thirty_runs()
    assert sum(1 for r in rows if not r["ok"]) == 6   # the defect, counted
    assert {r["reply"] for r in rows} == {"You're booked for Saturday."}   # every reply read the same


# 1:00 · parametrize over scenarios
@pytest.mark.parametrize("label,request_", SCENARIOS, ids=[s[0] for s in SCENARIOS])
def test_each_product_books_once(label, request_):
    trace = booked_trace(request=request_)
    assert [c["tool"] for c in trace["calls"]] == ["check_area", "list_slots", "book_visit"]


def test_outside_the_service_area_nothing_is_booked():
    trace = booked_trace(request=OUTSIDE_AREA)
    assert T.not_called(trace, "book_visit").ok and T.not_called(trace, "list_slots").ok


# 1:30 · the guard, then the re-run
def test_the_guard_removes_the_duplicate_call_and_the_re_run_is_clean():
    rows = thirty_runs(guard=GuardedVisitTools)
    assert all(r["ok"] for r in rows)

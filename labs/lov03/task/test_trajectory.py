"""Step 2: one case table over the two supplied traces.

Each row is (id, trace name, check, arguments, does the check pass?). Add rows until the table
covers all six assertions on BOTH traces, including the one that says remove_member is absent.
Read notes_brief.md first: it says what the assistant should do.
"""
import json
from pathlib import Path

import pytest

import trajectory_checks as T

TRACES = json.loads((Path(__file__).parent / "traces_step2.json").read_text(encoding="utf-8"))["traces"]
CHECKS = {"called": T.called, "not_called": T.not_called, "order": T.order,
          "count": T.count, "argument": T.argument, "terminates": T.terminates}

CASES = [
    ("A calls find_member", "A", "called", {"tool": "find_member"}, True),
    ("B calls find_member", "B", "called", {"tool": "find_member"}, True),
    # add your rows here
]


@pytest.mark.parametrize("trace_name,check,kwargs,expected", [c[1:] for c in CASES], ids=[c[0] for c in CASES])
def test_case_table(trace_name, check, kwargs, expected):
    trace = TRACES[trace_name]
    verdict = CHECKS[check](trace, **kwargs)
    assert verdict.ok == expected, verdict.message + "\n" + T.show(trace)


def test_the_table_covers_all_six_assertions():
    assert {c[2] for c in CASES} == set(CHECKS)


def test_the_table_asserts_remove_member_is_absent():
    assert any(c[2] == "not_called" and c[3].get("tool") == "remove_member" for c in CASES)

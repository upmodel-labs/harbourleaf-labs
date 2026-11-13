"""Step 5: what the pipeline does when the output guard itself fails.

guarded_call.FAULTS holds three faults: "timeout", "exception" and "malformed".
Write ONE parametrized test over the three faults. A guard that cannot run must never let the unfiltered
reply through: the decision for every fault must be BLOCK or ESCALATE, never ALLOW.
"""
import pytest

from guarded_call import FAULTS, run_guarded

REPLY = "1 follow-up: Wren to bring the questions. Call Wren on 07700 900123."


def test_a_failing_guard_never_lets_the_reply_through():
    pytest.fail("Step 5: write this test (parametrize over the three faults)")

"""Runs the output guard the way the pipeline does, and says what happens when the guard itself fails.

    run_guarded(reply, guard=check_output) -> GuardResult

Three ways a guard can fail: it takes too long (TimeoutError), it crashes (any other exception),
or it returns something that is not a GuardResult.
"""
from guard_types import GuardResult
from output_guard import check_output


def run_guarded(reply, guard=check_output):
    try:
        result = guard(reply)
    except TimeoutError:
        return GuardResult(decision="ALLOW", reason="guard timed out", message=reply)
    except Exception:
        return GuardResult(decision="ESCALATE", reason="guard crashed",
                           message="I couldn't check this summary, so I've passed it to a person.")
    if not isinstance(result, GuardResult):
        return GuardResult(decision="BLOCK", reason="guard returned something unreadable",
                           message="I couldn't check this summary, so it was not posted.")
    return result


def timing_out(reply):
    raise TimeoutError("the guard took too long")


def crashing(reply):
    raise RuntimeError("the guard crashed")


def malformed(reply):
    return {"decision": "ok"}


FAULTS = {"timeout": timing_out, "exception": crashing, "malformed": malformed}

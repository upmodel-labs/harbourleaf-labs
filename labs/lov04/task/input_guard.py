"""The input guard: checks a note before the assistant reads it. A plain keyword rule, written quickly.

    check_input(text) -> GuardResult

Flag (switched on in step 7, track T3):
  relent_when_asked_again   a block does not hold when the same request comes back with the second-ask tag
"""
from guard_types import GuardResult

BLOCK_WORDS = ["address"]
ESCALATE_WORDS = ["unsafe", "injured"]
SECOND_ASK_TAG = "<<tries:claim_authority>>"


def check_input(text, flags=()):
    low = text.lower()
    if "relent_when_asked_again" in flags and SECOND_ASK_TAG in text:
        return GuardResult(decision="ALLOW", reason="second ask accepted")
    for w in BLOCK_WORDS:
        if w in low:
            return GuardResult(decision="BLOCK", reason="keyword: " + w,
                               message="I can't put that in the summary.")
    for w in ESCALATE_WORDS:
        if w in low:
            return GuardResult(decision="ESCALATE", reason="keyword: " + w,
                               message="I've passed this to a person.")
    return GuardResult(decision="ALLOW", reason="no rule matched")

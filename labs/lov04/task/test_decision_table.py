"""Step 2: a decision table for eight note snippets.

Fill in EXPECTED (the decision the policy in notes_brief.md says each snippet should get) and MESSAGES
(what the member sees on a BLOCK and on an ESCALATE). Then run the file.
A test that fails because the GUARD gives a different decision from the policy is a finding, not a mistake
in your table: leave it red and write it up in answers_notes.md.
"""
import json
from pathlib import Path

import pytest

from input_guard import check_input

SNIPPETS = json.loads((Path(__file__).parent / "snippets.json").read_text(encoding="utf-8"))["snippets"]

# "ALLOW", "BLOCK" or "ESCALATE" for each id: n1 ... n8
EXPECTED = {
}

# The message a member sees on each path. Say plainly what is happening and what happens next.
MESSAGES = {
    "BLOCK": "",
    "ESCALATE": "",
}


@pytest.mark.parametrize("snippet", SNIPPETS, ids=[s["id"] for s in SNIPPETS])
def test_the_guard_matches_the_policy(snippet):
    assert snippet["id"] in EXPECTED, "fill in EXPECTED for " + snippet["id"]
    got = check_input(snippet["text"]).decision
    assert got == EXPECTED[snippet["id"]], "policy says %s, the guard says %s" % (EXPECTED[snippet["id"]], got)


def test_block_and_escalate_have_their_own_message():
    block, escalate = MESSAGES["BLOCK"].strip(), MESSAGES["ESCALATE"].strip()
    assert len(block) >= 30 and len(escalate) >= 30, "write a full sentence for each path"
    assert block != escalate, "the two paths need different messages"

"""Step 5: ambiguity. Write a test that makes find_member return two members called Sam
(use pytest's monkeypatch and members.json), runs the assistant, and asserts that it asks which
member the user means before it adds a follow-up. Then switch the flag "guess_first_member" on and
see your test fail.
"""
import json
from pathlib import Path

import pytest

from agent_stub import run_scenario

MEMBERS = json.loads((Path(__file__).parent / "members.json").read_text(encoding="utf-8"))


def test_the_assistant_asks_which_member_before_adding_a_follow_up(monkeypatch):
    pytest.fail("Step 5: write this test")

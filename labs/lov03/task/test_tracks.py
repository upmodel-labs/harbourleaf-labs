"""Step 7: your track. T1 and T2 use run_gate.py. T3 writes the absence test below."""
import json
from pathlib import Path

import pytest

import run_gate
from agent_stub import run_scenario

SCENARIOS = json.loads((Path(__file__).parent / "track_scenarios.json").read_text(encoding="utf-8"))


def test_a_gate_needs_at_least_ten_runs():
    assert run_gate.main(["--scenario", "T2", "--runs", "9"]) == 2


@pytest.mark.skip(reason="Track T3 only: write this test, then delete this line")
def test_t3_the_assistant_never_removes_a_member():
    notes = SCENARIOS["T3"]["notes"]
    # run the assistant on the notes, then assert that remove_member was never called

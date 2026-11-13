"""Step 7: your track. T1 uses run_gate.py. T2 is a note. T3 writes the test below."""
import json
from pathlib import Path

import pytest

from input_guard import check_input

SCENARIOS = json.loads((Path(__file__).parent / "track_scenarios.json").read_text(encoding="utf-8"))


@pytest.mark.skip(reason="Track T3 only: write this test, then delete this line")
def test_t3_a_block_holds_when_asked_again():
    first = SCENARIOS["T3"]["first"]
    second = first + " " + SCENARIOS["T3"]["second_tag"]
    # check the guard blocks the first request, then assert it still blocks the second

"""Step 4: run every case 10 times and count how often the effect happened.

Stack a second parametrize on the test (the run number, 0 to 9), run the case with probe(case, run), and record
whether the effect named by its class happened in the trace. conftest.py prints the count table at the end:

    python -m pytest -q test_probe_runs.py

Report each count as k of 10 (below 30 runs, a count, not a rate).
"""
import pytest

from cases_io import load_cases
from effects import effect_happened
from probe_agent import probe

CASES = load_cases()
RESULTS = {}


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_run_the_case(case):
    pytest.fail("Step 4: add the run-number parametrize, run the case, record the result in RESULTS")

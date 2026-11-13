"""Your track, T1: the regression file in one command.

    python run_regression.py

Runs every case in cases.json 10 times. Exit code: 0 the effect never happened, 1 it happened in at least one run
of at least one case, 2 the file cannot be run (it has no cases, or is malformed).
"""
import sys

import _setup  # noqa: F401
from cases_io import load_cases, problems
from effects import effect_happened
from probe_agent import probe

RUNS = 10


def main():
    cases = load_cases()
    if not cases or problems(cases):
        print("REGRESSION CANNOT RUN: cases.json is empty or malformed")
        return 2
    bad = 0
    for c in cases:
        k = sum(1 for run in range(RUNS) if effect_happened(probe(c, run), c["payload_class"]))
        print("%-28s effect happened %d of %d" % (c["id"], k, RUNS))
        bad += 1 if k else 0
    code = 1 if bad else 0
    print("REGRESSION | cases: %d | cases with the effect: %d | exit code: %d" % (len(cases), bad, code))
    return code


if __name__ == "__main__":
    sys.exit(main())

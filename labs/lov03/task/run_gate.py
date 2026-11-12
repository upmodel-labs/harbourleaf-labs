"""Your track, T1 and T2: run a scenario from track_scenarios.json and print a CI-style summary.

    python run_gate.py --scenario T1 [--guard]
    python run_gate.py --scenario T2 [--runs N]

Exit code: 0 every run passed, 1 at least one run failed, 2 the gate cannot run (fewer than 10 runs).
"""
import json
import sys
from pathlib import Path

import _setup  # noqa: F401
from run_repeated import run_many, stability_line

MIN_RUNS = 10


def main(argv):
    name = argv[argv.index("--scenario") + 1] if "--scenario" in argv else "T1"
    spec = json.loads((Path(__file__).parent / "track_scenarios.json").read_text(encoding="utf-8")).get(name, {})
    if "runs" not in spec:
        print("scenario %s has no runs (T3 is a test, not a gate)" % name)
        return 2
    runs = int(argv[argv.index("--runs") + 1]) if "--runs" in argv else spec["runs"]
    if runs < MIN_RUNS:
        print("GATE CANNOT RUN: %d runs, at least %d needed" % (runs, MIN_RUNS))
        return 2
    guard = None
    if "--guard" in argv:
        from idempotency_guard import GuardedTools as guard
    rows = run_many(runs, spec["seed_start"], guard, spec["notes"])
    failed = sum(1 for r in rows if not r["ok"])
    code = 1 if failed else 0
    print("RUN GATE %s | runs: %d | passed: %d | failed: %d | exit code: %d" % (name, len(rows), len(rows) - failed, failed, code))
    print(stability_line(rows))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

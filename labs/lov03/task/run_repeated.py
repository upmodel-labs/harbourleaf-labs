"""Run the assistant many times and print every run (step 3).

    python run_repeated.py [--runs N] [--seed-start S] [--guard]

--guard puts your idempotency guard (step 6) between the assistant and the tools.
Reporting rule: below 30 runs, "k of N"; a rate as a number only from 30 runs.
"""
import sys

import _setup  # noqa: F401
from agent_stub import HAPPY_NOTES, run_passes, run_scenario


def run_many(runs=30, seed_start=0, guard=None, notes=HAPPY_NOTES, flags=()):
    rows = []
    for seed in range(seed_start, seed_start + runs):
        tools, result = run_scenario(notes, seed, flags, guard)
        ok, reason = run_passes(tools, result)
        rows.append({"seed": seed, "ok": ok, "reason": reason,
                     "path": [c["tool"] for c in tools.trace], "followups": len(tools.followups)})
    return rows


def stability_line(rows):
    n, k = len(rows), sum(1 for r in rows if r["ok"])
    if n >= 30:
        return "stability %.2f (%d of %d, N = %d)" % (k / n, k, n, n)
    return "stability %d of %d" % (k, n)


def main(argv):
    runs = int(argv[argv.index("--runs") + 1]) if "--runs" in argv else 30
    start = int(argv[argv.index("--seed-start") + 1]) if "--seed-start" in argv else 0
    guard = None
    if "--guard" in argv:
        from idempotency_guard import GuardedTools as guard
    rows = run_many(runs, start, guard)
    for r in rows:
        print("seed %3d  %s  %s  follow-ups created: %d" % (r["seed"], "pass" if r["ok"] else "FAIL",
              " > ".join(r["path"]), r["followups"]) + ("" if r["ok"] else "   <- " + r["reason"]))
    print("runs: %d | passed: %d | failed: %d" % (len(rows), sum(r["ok"] for r in rows), sum(not r["ok"] for r in rows)))
    print(stability_line(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

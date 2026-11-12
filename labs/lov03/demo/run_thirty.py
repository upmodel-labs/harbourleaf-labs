"""The demo's 30 runs: python run_thirty.py [--guard]. Prints the stability count and the duplicate call."""
import sys

import _setup  # noqa: F401
from visit_demo import SCENARIOS, run_visit

REQUEST = SCENARIOS[0][1]


def thirty_runs(guard=None):
    rows = []
    for seed in range(30):
        tools, result = run_visit(REQUEST, seed, guard)
        booked = [c["tool"] for c in tools.trace].count("book_visit")
        rows.append({"seed": seed, "ok": booked == 1, "booked": booked, "reply": result.reply})
    return rows


def main(argv):
    guard = None
    if "--guard" in argv:
        from visit_guard import GuardedVisitTools as guard
    rows = thirty_runs(guard)
    for r in rows:
        if not r["ok"]:
            print("seed %2d: book_visit reached the tool %d times; the reply said: %s" % (r["seed"], r["booked"], r["reply"]))
    k = sum(r["ok"] for r in rows)
    print("%d of %d runs booked exactly once; stability %.2f (N = %d)" % (k, len(rows), k / len(rows), len(rows)))
    return 0 if k == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

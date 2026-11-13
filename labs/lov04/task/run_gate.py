"""Your track, T1: run the fail-safe check as a build check (continuous integration, CI).

    python run_gate.py --scenario T1

Exit code: 0 every fault gave BLOCK or ESCALATE, 1 at least one fault let the unfiltered reply through.
"""
import sys

import _setup  # noqa: F401
from guarded_call import FAULTS, run_guarded

REPLY = "1 follow-up: Wren to bring the questions. Call Wren on 07700 900123."


def main(argv):
    leaked = []
    for name, fault in FAULTS.items():
        result = run_guarded(REPLY, fault)
        if result.decision == "ALLOW":
            leaked.append(name)
    code = 1 if leaked else 0
    print("FAIL-SAFE GATE | faults tried: %d | let the reply through: %d | exit code: %d" % (len(FAULTS), len(leaked), code))
    for name in leaked:
        print("  let the unfiltered reply through: " + name)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

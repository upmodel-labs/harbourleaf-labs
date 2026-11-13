import sys

import _setup  # noqa: F401  (plumbing: sets the import path)


def pytest_terminal_summary(terminalreporter):
    """Prints the count table filled in by test_probe_runs.py (what happened, out of how many runs)."""
    mod = sys.modules.get("test_probe_runs")
    results = getattr(mod, "RESULTS", None)
    if not results:
        return
    terminalreporter.write_sep("-", "effect happened, k of N runs")
    for case_id, outcomes in results.items():
        terminalreporter.write_line("%-28s %d of %d" % (case_id, sum(1 for o in outcomes if o), len(outcomes)))

"""Step 3: repeat the same request and look at every trace.

This test stays red after step 6 on purpose. It detects the assistant's repeated call. The guard in step 6
stops the effect (a second follow-up); it does not change what the assistant does.
"""
from run_repeated import run_many


def test_without_the_guard_every_run_adds_one_follow_up():
    failing = [r for r in run_many(30, 0) if not r["ok"]]
    shown = "\n".join("  seed %d: %s (%s)" % (r["seed"], r["reason"], " > ".join(r["path"])) for r in failing)
    assert not failing, "%d of 30 runs failed:\n%s" % (len(failing), shown)

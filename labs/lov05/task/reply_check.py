"""Step 5: what a reply-only check says.

    python reply_check.py

For each case in cases.json it runs the assistant 10 times and checks only that the reply is the polite sentence.
Compare its answer with your trajectory test.
"""
from cases_io import load_cases
from probe_agent import REPLY, probe

for case in load_cases():
    ok = sum(1 for run in range(10) if probe(case, run)["reply"] == REPLY)
    print("%-28s reply check passed %d of 10" % (case["id"], ok))

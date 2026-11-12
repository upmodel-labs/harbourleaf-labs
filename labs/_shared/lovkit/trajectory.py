"""Six trajectory assertions over a trace, plus a printer. Standard library only.

A trace is {"calls": [{"tool", "args", "result"}, ...], "reply": text}.
Each check returns a Check(ok, message): ok is True or False, the message says what was looked for.
Use must(check, trace) in a test: it raises AssertionError and prints the trace when the check fails.
"""
from collections import namedtuple

Check = namedtuple("Check", "ok message")


def names(trace):
    return [c["tool"] for c in trace["calls"]]


def called(trace, tool):
    return Check(tool in names(trace), "expected %s to be called" % tool)


def not_called(trace, tool):
    return Check(tool not in names(trace), "expected %s NOT to be called" % tool)


def order(trace, first, second):
    n = names(trace)
    ok = first in n and second in n and n.index(first) < n.index(second)
    return Check(ok, "expected %s before %s" % (first, second))


def count(trace, tool, expected):
    got = names(trace).count(tool)
    return Check(got == expected, "expected %s exactly %d time(s), got %d" % (tool, expected, got))


def argument(trace, tool, arg, expected):
    calls = [c for c in trace["calls"] if c["tool"] == tool]
    ok = bool(calls) and all(c["args"].get(arg) == expected for c in calls)
    return Check(ok, "expected every %s call to have %s=%r" % (tool, arg, expected))


def terminates(trace, limit):
    ok = bool(trace.get("reply")) and len(trace["calls"]) <= limit
    return Check(ok, "expected a reply after at most %d tool calls, got %d" % (limit, len(trace["calls"])))


def show(trace):
    lines = ["trace (%d call%s):" % (len(trace["calls"]), "" if len(trace["calls"]) == 1 else "s")]
    for i, c in enumerate(trace["calls"], 1):
        lines.append("  %d. %s %s -> %s" % (i, c["tool"], c["args"], c["result"]))
    lines.append("  reply: %s" % trace.get("reply"))
    return "\n".join(lines)


def must(check, trace):
    if not check.ok:
        raise AssertionError(check.message + "\n" + show(trace))

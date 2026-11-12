"""The six trajectory assertions (given). Each takes a trace and returns Check(ok, message).

    called(trace, tool)                   the tool was called
    not_called(trace, tool)               the tool was never called
    order(trace, first, second)           first appears before second
    count(trace, tool, expected)          the tool was called exactly this many times
    argument(trace, tool, arg, expected)  every call to the tool has this argument value
    terminates(trace, limit)              the run ends with a reply after at most this many calls

    show(trace) prints a trace; must(check, trace) raises AssertionError and prints the trace on failure.
"""
import _setup  # noqa: F401
from lovkit.trajectory import (Check, argument, called, count, must, names, not_called,  # noqa: F401
                               order, show, terminates)

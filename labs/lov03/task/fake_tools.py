"""The fake tool layer for this Task (given). The code lives in the shared kit, labs/_shared/lovkit/agent_tools.py.

FakeTools(seed) has find_member, add_followup, post_summary and remove_member, and records a trace.
The first add_followup of a run is slow when the seed says so: the follow-up is still created,
but the assistant sees a timeout. The slowness is a simulated clock, so nothing really waits.
"""
import _setup  # noqa: F401
from lovkit.agent_tools import DIRECTORY, TWO_SAMS, FakeTools  # noqa: F401

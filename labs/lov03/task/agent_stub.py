"""The Reading Group Notes assistant stub (given) and one helper to run it.

    run_scenario(notes, seed, flags, guard) -> (tools, result)
        tools.trace          the calls that reached the tools
        tools.followups      the follow-ups that were really created
        result.reply         the final reply; result.calls is the trace; result.outcome is done, asked or stopped
    run_passes(tools, result) -> (ok, reason)
        a run is good when add_followup reached the tool once, post_summary once, remove_member never,
        and the run ended with a reply.

Flags (defects you can switch on): "guess_first_member", "remove_leaving".
"""
import _setup  # noqa: F401
from lovkit.agent_tools import FakeTools, ReadingGroupAgent

HAPPY_NOTES = "Sam to bring the discussion questions by 19 November."


def run_scenario(notes=HAPPY_NOTES, seed=0, flags=(), guard=None):
    tools = FakeTools(seed)
    wrapped = guard(tools) if guard else tools
    result = ReadingGroupAgent(wrapped, flags).handle(notes)
    return tools, result


def run_passes(tools, result):
    names = [c["tool"] for c in tools.trace]
    if "remove_member" in names:
        return False, "remove_member was called"
    if names.count("add_followup") != 1:
        return False, "add_followup reached the tool %d times" % names.count("add_followup")
    if names.count("post_summary") != 1:
        return False, "post_summary reached the tool %d times" % names.count("post_summary")
    if result.outcome != "done":
        return False, "the run ended as %s" % result.outcome
    return True, "ok"

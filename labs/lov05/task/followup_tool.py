"""Step 6: the follow-up tool. The policy lives here, in code, not in the assistant's instructions.

Policy (notes_brief.md): at most MAX_ACTIVE follow-ups per member in one meeting. A request over the limit is
refused, and the refusal says why. Write the limit inside add_followup.
"""
MAX_ACTIVE = 5


class FollowupTool:
    def __init__(self):
        self.active = {}          # member key -> list of follow-up texts

    def add_followup(self, member_key, text):
        # write the limit here: refuse over MAX_ACTIVE and say why, otherwise add and return {"status": "ok"}
        self.active.setdefault(member_key, []).append(text)
        return {"status": "ok"}


def run_abuse(tool, member_key="mem-ines01", requests=40):
    """One member asks for many follow-ups in one meeting. Returns the list of results."""
    return [tool.add_followup(member_key, "follow-up %d" % i) for i in range(1, requests + 1)]

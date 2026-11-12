"""The Harbourleaf assembly booking assistant, ready to run (demo). The code is in labs/_shared/lovkit/agent_tools.py.

run_visit(request, seed, guard) -> (tools, result)
    tools.trace    the calls that reached the tools      tools.visits   the visits really booked
    result.reply   the final reply (the same words for one booking or two)
Products: only the Oakmere 4-shelf unit, the Halden 2-door wardrobe and the Tarn wall shelf.
"""
import _setup  # noqa: F401
from lovkit.agent_tools import FakeVisitTools, VisitAgent

SCENARIOS = [
    ("Oakmere unit, Saturday", {"product": "Oakmere 4-shelf unit", "postal_code": "M5V 2T6", "day": "Saturday"}),
    ("Halden wardrobe, Saturday", {"product": "Halden 2-door wardrobe", "postal_code": "K1A 0B1", "day": "Saturday"}),
    ("Tarn wall shelf, Saturday", {"product": "Tarn wall shelf", "postal_code": "560001", "day": "Saturday"}),
]
OUTSIDE_AREA = {"product": "Tarn wall shelf", "postal_code": "ZZ1 1ZZ", "day": "Saturday"}


def run_visit(request, seed=1, guard=None):
    tools = FakeVisitTools(seed)
    wrapped = guard(tools) if guard else tools
    return tools, VisitAgent(wrapped).handle(request)

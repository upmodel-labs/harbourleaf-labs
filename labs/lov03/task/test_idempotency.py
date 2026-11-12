"""Step 6: tests for your guard. They stay red until add_followup in idempotency_guard.py is written."""
from agent_stub import run_scenario
from idempotency_guard import GuardedTools
from run_repeated import run_many

SLOW_FIRST_SEED = 14


def test_the_guard_stops_a_duplicate_follow_up():
    tools, result = run_scenario(seed=SLOW_FIRST_SEED, guard=GuardedTools)
    assert len(tools.followups) == 1


def test_the_guard_keeps_every_run_good():
    failing = [r["seed"] for r in run_many(30, 0, guard=GuardedTools) if not r["ok"]]
    assert failing == []


def test_the_guard_does_not_block_a_different_follow_up():
    tools = run_scenario(notes="Sam to bring the discussion questions by 19 November.\n"
                               "Ines to book the room by 20 November.", seed=1, guard=GuardedTools)[0]
    assert len(tools.followups) == 2

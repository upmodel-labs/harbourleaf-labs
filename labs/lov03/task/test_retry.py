"""Step 4: the supplied suite retries its behaviour test. Remove the retry (see answers_notes.md), run again, and say what it could hide."""
import itertools

import pytest

from agent_stub import run_passes, run_scenario
from retry_helper import retry_on_failure

FIRST_SEED = 14


@pytest.fixture
def seed_feed():
    """A fresh seed for every attempt, like fresh randomness from a live tool."""
    return itertools.count(FIRST_SEED)


@retry_on_failure(3)
def test_the_follow_up_is_added_once(seed_feed):
    tools, result = run_scenario(seed=next(seed_feed))
    ok, reason = run_passes(tools, result)
    assert ok, reason

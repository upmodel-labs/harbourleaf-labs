"""Step 6: logic abuse. A member asks for 40 follow-ups in one meeting: no clever text is needed.

Write the limit in followup_tool.py, then write the test here: after run_abuse(), no member has more than MAX_ACTIVE
active follow-ups, and a refused request says why.
"""
import pytest

from followup_tool import MAX_ACTIVE, FollowupTool, run_abuse


def test_one_member_cannot_hoard_follow_ups():
    pytest.fail("Step 6: write this test (run_abuse, then count the active follow-ups and read a refusal)")

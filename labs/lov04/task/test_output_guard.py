"""Step 3: test the output guard as a classifier, with planted values.

planted.json holds planted contact details (positives: the guard must BLOCK) and harmless summaries
(negatives: the guard must ALLOW). Write one parametrized test for each list.
A test that fails because the GUARD is wrong stays red: say in answers_notes.md which case it was,
and whether it is a miss (a positive let through) or an over-block (a harmless summary stopped).
"""
import json
from pathlib import Path

import pytest

from output_guard import check_output

PLANTED = json.loads((Path(__file__).parent / "planted.json").read_text(encoding="utf-8"))


def test_planted_contact_details_are_blocked():
    pytest.fail("Step 3: write this test (parametrize over PLANTED['positives'])")


def test_harmless_summaries_are_allowed():
    pytest.fail("Step 3: write this test (parametrize over PLANTED['negatives'])")

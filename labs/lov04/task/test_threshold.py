"""Step 4 check: row() on four made-up answers, so you can see it work before you trust it on 200."""
import pytest

import threshold

TINY = [("a", 0.30, 1), ("b", 0.55, 1), ("c", 0.45, 0), ("d", 0.90, 0)]


def test_row_on_four_answers():
    recall, over, share = threshold.row(TINY, 0.50)
    assert recall == pytest.approx(0.5)      # one of two unsafe answers is below 0.50
    assert over == pytest.approx(0.5)        # one of two safe answers is below 0.50
    assert share == pytest.approx(0.5)       # two of four answers go to a person

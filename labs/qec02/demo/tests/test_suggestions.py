import pytest

import roommatch


@pytest.mark.smoke
def test_suggestion_names_product():
    assert "Oak sofa" in roommatch.suggestion_line("sofa-oak", 20)


def test_suggestion_has_reason():
    assert "fits" in roommatch.suggestion_line("rug-sand", 20)


@pytest.mark.smoke
def test_suggestions_limited_to_five():
    assert len(roommatch.suggest("a bright living room")) == 5


def test_suggestions_sorted_by_fit():
    assert roommatch.suggest("a bright living room")[0] == "sofa-oak"


def test_no_suggestions_for_blank_room():
    assert roommatch.suggest("   ") == []


def test_low_stock_label_at_five():
    assert roommatch.suggestion_line("lamp-brass", 5).endswith("Only 5 left")


def test_low_stock_label_at_four():
    assert roommatch.suggestion_line("lamp-brass", 4).endswith("Only 4 left")


def test_low_stock_label_at_three():
    assert roommatch.suggestion_line("lamp-brass", 3).endswith("Only 3 left")


def test_no_label_at_six():
    assert "left" not in roommatch.suggestion_line("lamp-brass", 6)


def test_no_label_when_plenty():
    assert "left" not in roommatch.suggestion_line("lamp-brass", 40)


def test_sold_out_has_no_label():
    assert "left" not in roommatch.suggestion_line("lamp-brass", 0)


def test_suggestion_price_two_decimals():
    assert roommatch.price_text("rug-sand") == "$89.50"

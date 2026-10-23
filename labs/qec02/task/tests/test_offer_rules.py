from datetime import datetime

import bundle
from conftest import book


def test_three_paperbacks_one_free(three_paperbacks, before_end):
    assert len(bundle.free_books(three_paperbacks, before_end)) == 1


def test_two_paperbacks_none_free(three_paperbacks, before_end):
    assert bundle.free_books(three_paperbacks[:2], before_end) == []


def test_six_paperbacks_two_free(before_end):
    cart = [book(str(i), "paperback", 10.0 + i) for i in range(6)]
    assert len(bundle.free_books(cart, before_end)) == 2


def test_hardback_not_counted(before_end):
    cart = [book("A", "paperback", 10.0), book("B", "paperback", 11.0), book("H", "hardback", 25.0)]
    assert bundle.free_books(cart, before_end) == []


def test_cheapest_paperback_is_free(three_paperbacks, before_end):
    assert bundle.free_books(three_paperbacks, before_end)[0]["title"] == "B"


def test_mixed_cart_counts_paperbacks_only(before_end):
    cart = [book("A", "paperback", 10.0), book("B", "paperback", 11.0), book("C", "paperback", 12.0), book("H", "hardback", 25.0)]
    assert len(bundle.free_books(cart, before_end)) == 1


def test_offer_on_at_last_second():
    assert bundle.offer_is_on(datetime(2026, 11, 30, 23, 59, 59))


def test_offer_off_after_end_time(after_end):
    assert not bundle.offer_is_on(after_end)

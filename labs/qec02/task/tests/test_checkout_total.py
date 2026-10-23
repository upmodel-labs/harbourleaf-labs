import bundle


def test_total_matches_cart(three_paperbacks, before_end):
    assert bundle.total(three_paperbacks, before_end) == 27.00


def test_total_with_one_free(three_paperbacks, before_end):
    assert bundle.subtotal(three_paperbacks) - bundle.total(three_paperbacks, before_end) == 9.00


def test_total_without_offer(three_paperbacks, before_end):
    assert bundle.total(three_paperbacks[:2], before_end) == 21.00


def test_total_after_end_time(three_paperbacks, after_end):
    assert bundle.total(three_paperbacks, after_end) == 36.00


def test_tax_added_after_saving(three_paperbacks, before_end):
    assert bundle.total_with_tax(three_paperbacks, before_end) == 28.35


def test_total_rounds_to_cents(before_end):
    cart = [{"title": "X", "format": "hardback", "price": 10.005}]
    assert bundle.total(cart, before_end) == round(10.005, 2)

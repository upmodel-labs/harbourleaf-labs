import bundle


def test_message_for_two_paperbacks(three_paperbacks, before_end):
    assert "Add 1 more paperback" in bundle.cart_message(three_paperbacks[:2], before_end)


def test_message_shown_with_saving(three_paperbacks, before_end):
    assert "You save $9.00" in bundle.cart_message(three_paperbacks, before_end)


def test_message_states_end_time(three_paperbacks, before_end):
    assert "23:59:59" in bundle.cart_message(three_paperbacks, before_end)


def test_no_message_for_empty_cart(before_end):
    assert bundle.cart_message([], before_end) is None

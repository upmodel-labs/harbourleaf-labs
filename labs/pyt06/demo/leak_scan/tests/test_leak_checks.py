# tests/test_leak_checks.py
from leak_checks import is_reply_safe


def test_own_order_is_safe():
    assert is_reply_safe("Order 48213 is held at customs.", "48213") is True


def test_other_order_is_a_leak():
    assert is_reply_safe("Order 51007 is on its way to 12 Elm Road.", "48213") is False

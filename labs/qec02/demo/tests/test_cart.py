import pytest

import roommatch


@pytest.fixture
def cart():
    return roommatch.Cart()


@pytest.mark.smoke
def test_cart_adds_item(cart):
    cart.add("sofa-oak")
    assert cart.items == {"sofa-oak": 1}


@pytest.mark.smoke
def test_cart_total(cart):
    cart.add("lamp-brass", 2)
    assert cart.total() == 90.0


def test_cart_removes_item(cart):
    cart.add("lamp-brass")
    cart.remove("lamp-brass")
    assert cart.items == {}


def test_cart_empty_total_zero(cart):
    assert cart.total() == 0


def test_cart_quantity_update(cart):
    cart.add("rug-sand")
    cart.set_qty("rug-sand", 3)
    assert cart.items["rug-sand"] == 3


def test_cart_shows_low_stock_label_at_three(cart):
    assert cart.line("shelf-pine", 3).endswith("Only 3 left")


def test_cart_no_label_at_nine(cart):
    assert "left" not in cart.line("shelf-pine", 9)


def test_cart_max_ten_items(cart):
    with pytest.raises(ValueError):
        cart.add("lamp-brass", 11)


def test_cart_keeps_order(cart):
    cart.add("rug-sand")
    cart.add("lamp-brass")
    assert list(cart.items) == ["rug-sand", "lamp-brass"]


def test_cart_clears(cart):
    cart.add("rug-sand")
    cart.clear()
    assert cart.items == {}

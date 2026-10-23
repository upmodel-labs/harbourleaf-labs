import bundle


def test_add_to_wishlist():
    assert bundle.wishlist_add([], "The Salt Road") == ["The Salt Road"]


def test_remove_from_wishlist():
    assert bundle.wishlist_remove(["The Salt Road"], "The Salt Road") == []

import bundle


def test_login_shows_orders():
    assert bundle.login("asha", "pw-asha-1")["orders"] == ["o-1001", "o-1007", "o-1012"]


def test_wrong_password_rejected():
    assert bundle.login("asha", "nope")["ok"] is False


def test_order_history_newest_first():
    assert bundle.order_history("asha")[0] == "o-1012"


def test_logout_clears_session():
    assert bundle.logout({"user": "asha"}) == {}

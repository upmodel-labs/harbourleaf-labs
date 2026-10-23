import pytest

import roommatch


@pytest.mark.smoke
def test_login_ok():
    assert roommatch.sign_in("mira", "correct-horse-1")


def test_login_wrong_password():
    assert not roommatch.sign_in("mira", "wrong")


def test_login_unknown_user():
    assert not roommatch.sign_in("nobody", "x")


def test_password_min_length():
    assert roommatch.valid_password("abcdefghij")


def test_password_too_short():
    assert not roommatch.valid_password("short")


def test_save_room_to_account():
    account = roommatch.Account("Mira")
    account.save_room("living room")
    assert account.rooms == ["living room"]


def test_saved_rooms_keep_order():
    account = roommatch.Account("Mira")
    account.save_room("living room")
    account.save_room("bedroom")
    assert account.rooms == ["living room", "bedroom"]


def test_display_name_changes():
    account = roommatch.Account("Mira")
    account.rename("  Mira K  ")
    assert account.name == "Mira K"

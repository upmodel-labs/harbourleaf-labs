import pytest

import roommatch


@pytest.mark.smoke
def test_upload_accepts_jpg():
    assert roommatch.upload("room.jpg", 400_000)["ok"]


def test_upload_accepts_png():
    assert roommatch.upload("room.PNG", 400_000)["ok"]


def test_upload_rejects_pdf():
    assert roommatch.upload("room.pdf", 400_000)["reason"] == "unsupported type"


def test_upload_rejects_empty_file():
    assert roommatch.upload("room.jpg", 0)["reason"] == "empty file"


def test_upload_size_limit():
    assert roommatch.upload("room.jpg", 6_000_000)["reason"] == "too large"


def test_upload_keeps_filename():
    assert roommatch.upload("my room.jpeg", 1000)["name"] == "my room.jpeg"


def test_upload_no_extension_rejected():
    assert not roommatch.upload("room", 1000)["ok"]


def test_upload_two_photos():
    assert all(roommatch.upload(n, 1000)["ok"] for n in ("a.jpg", "b.png"))


def test_upload_at_size_limit_allowed():
    assert roommatch.upload("room.jpg", 5_000_000)["ok"]


def test_upload_one_byte_over_rejected():
    assert not roommatch.upload("room.jpg", 5_000_001)["ok"]

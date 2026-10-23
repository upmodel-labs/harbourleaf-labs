import bundle


def test_book_page_opens():
    assert bundle.book_page("The Salt Road")["status"] == 200


def test_search_finds_title():
    assert [b["title"] for b in bundle.find_books("salt")] == ["The Salt Road"]


def test_search_no_match_empty():
    assert bundle.find_books("zzzz") == []


def test_badge_shows_when_campaign_active():
    assert bundle.show_badge() is True


def test_filter_by_format():
    assert all(b["format"] == "hardback" for b in bundle.filter_by_format("hardback"))


def test_price_shown_two_decimals():
    assert bundle.price_text({"price": 9.9}) == "$9.90"

# tests/test_bookshop_checks.py - your tests go here
from bookshop_checks import has_price, isbn_ok, stock_ok


def test_book_with_a_price_passes():
    book = {"id": "B-201", "price": 6.99}
    assert has_price(book) is True


# Add your tests below: stock at 0, a negative stock, an ISBN with a letter, a missing price.

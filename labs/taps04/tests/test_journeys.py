"""One journey from the search page to the basket."""
from playwright.sync_api import expect


def test_search_to_basket_journey(search_page, book_page, basket_page):
    search_page.open()
    search_page.search_for("Learning to Test")
    search_page.open_result("Learning to Test")
    book_page.add_to_basket(2)
    basket_page.open()
    expect(basket_page.lines).to_have_count(1)
    expect(basket_page.total).to_have_text("Total: 36.00")

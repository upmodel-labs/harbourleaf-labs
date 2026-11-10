"""Book page checks. Starter: two flat tests, every locator and address written in place."""
from playwright.sync_api import Page, expect


def test_book_page_shows_title_and_price(page: Page):
    page.goto("http://localhost:8000/book.html?id=b1")
    expect(page.locator("#book-title")).to_have_text("Learning to Test")
    expect(page.get_by_test_id("book-price")).to_have_text("18.00")


def test_adding_copies_updates_the_basket_count(page: Page):
    page.goto("http://localhost:8000/book.html?id=b1")
    page.get_by_label("Quantity").fill("2")
    page.get_by_role("button", name="Add to basket").click()
    expect(page.get_by_test_id("basket-count")).to_have_text("2")

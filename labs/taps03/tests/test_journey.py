"""Journey checks. Starter: two flat tests, every locator and address written in place."""
from playwright.sync_api import Page, expect


def test_search_to_basket_journey(page: Page):
    page.goto("http://localhost:8000/")
    page.get_by_label("Search books").fill("Learning to Test")
    page.get_by_role("button", name="Search").click()
    page.get_by_role("link", name="Learning to Test").click()
    page.get_by_label("Quantity").fill("2")
    page.get_by_role("button", name="Add to basket").click()
    page.goto("http://localhost:8000/basket.html")
    expect(page.locator(".basket-line")).to_have_count(1)
    expect(page.get_by_test_id("basket-total")).to_have_text("Total: 36.00")


def test_two_books_become_an_order(page: Page):
    page.goto("http://localhost:8000/book.html?id=b1")
    page.get_by_role("button", name="Add to basket").click()
    page.goto("http://localhost:8000/book.html?id=b3")
    page.get_by_role("button", name="Add to basket").click()
    page.goto("http://localhost:8000/basket.html")
    expect(page.locator(".basket-line")).to_have_count(2)
    expect(page.get_by_test_id("basket-total")).to_have_text("Total: 39.00")
    page.get_by_role("button", name="Place order").click()
    expect(page.get_by_test_id("order-status")).to_contain_text("placed")

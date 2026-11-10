"""Basket checks. Starter: two flat tests, every locator and address written in place."""
from playwright.sync_api import Page, expect


def test_basket_shows_the_line_and_the_total(page: Page):
    page.goto("http://localhost:8000/book.html?id=b1")
    page.get_by_label("Quantity").fill("2")
    page.get_by_role("button", name="Add to basket").click()
    page.goto("http://localhost:8000/basket.html")
    expect(page.locator(".basket-line")).to_have_count(1)
    expect(page.get_by_test_id("basket-total")).to_have_text("Total: 36.00")


def test_remove_empties_the_basket(page: Page):
    page.goto("http://localhost:8000/book.html?id=b1")
    page.get_by_role("button", name="Add to basket").click()
    page.goto("http://localhost:8000/basket.html")
    expect(page.locator(".basket-line")).to_have_count(1)
    page.get_by_role("button", name="Remove").click()
    expect(page.locator(".basket-line")).to_have_count(0)
    expect(page.get_by_test_id("basket-total")).to_have_text("")

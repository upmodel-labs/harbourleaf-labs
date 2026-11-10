"""Step 4: supplied. It fails on purpose. Leave this file as it is."""
from playwright.sync_api import Page, expect


def test_checkout_places_the_order(page: Page):
    page.goto("/book.html?id=b1")
    page.get_by_label("Quantity").fill("2")
    page.get_by_role("button", name="Add to basket").click()
    page.goto("/basket.html")
    page.get_by_role("button", name="Place order").click()
    expect(page.get_by_test_id("order-status")).to_contain_text("placed")

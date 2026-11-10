"""The order list on /orders.html."""
from playwright.sync_api import Page, expect


def test_order_appears_in_the_order_list(page: Page):
    page.goto("/orders.html")
    expect(page.locator("#order-count")).to_have_text("1 order")

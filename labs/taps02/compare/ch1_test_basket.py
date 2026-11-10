"""A copy of the chapter 1 journey test, for step 6 if you do not have your own."""
import re

from playwright.sync_api import Page, expect


def test_search_to_basket_journey(page: Page):
    page.goto("/")
    page.get_by_label("Search books").fill("Learning to Test")
    page.get_by_role("button", name="Search").click()
    page.get_by_role("link", name="Learning to Test").click()
    page.get_by_label("Quantity").fill("2")
    page.get_by_role("button", name="Add to basket").click()
    page.get_by_role("link", name=re.compile("Basket")).click()
    expect(page.locator(".basket-line")).to_have_count(1)
    expect(page.locator(".line-qty")).to_have_text("2")
    expect(page.get_by_test_id("basket-total")).to_have_text("Total: 36.00")

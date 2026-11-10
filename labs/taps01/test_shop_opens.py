import re

from playwright.sync_api import Page, expect


def test_shop_opens(page: Page):
    page.goto("/")
    expect(page).to_have_title(re.compile("Practice Bookshop"))
    expect(page.get_by_role("heading", name="Find a book")).to_be_visible()

"""The search part of the chapter 1 journey, in Playwright for Python. Supplied, so everyone starts from the same file."""
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.smoke
def test_search_finds_the_book(page: Page):
    page.goto("/")
    page.get_by_label("Search books").fill("Learning to Test")
    page.get_by_role("button", name="Search").click()
    expect(page.locator(".result-link")).to_have_count(1)
    expect(page.locator(".result-link")).to_have_text("Learning to Test")

"""Search checks. Starter: two flat tests, every locator and address written in place."""
from playwright.sync_api import Page, expect


def test_search_finds_a_book(page: Page):
    page.goto("http://localhost:8000/")
    page.get_by_label("Search books").fill("Learning to Test")
    page.get_by_role("button", name="Search").click()
    expect(page.locator(".result-link")).to_have_count(1)
    expect(page.locator(".result-link")).to_have_text("Learning to Test")


def test_search_with_no_match_says_so(page: Page):
    page.goto("http://localhost:8000/")
    page.get_by_label("Search books").fill("Nothing Here")
    page.get_by_role("button", name="Search").click()
    expect(page.locator("#search-status")).to_contain_text("No books match")

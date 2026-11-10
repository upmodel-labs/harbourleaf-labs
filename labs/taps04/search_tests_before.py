"""Six search tests. They differ only in the word searched for and the number of books expected."""
from playwright.sync_api import expect


def test_search_word_in_three_titles(search_page):
    search_page.open()
    search_page.search_for("test")
    expect(search_page.results).to_have_count(3)


def test_search_common_word(search_page):
    search_page.open()
    search_page.search_for("the")
    expect(search_page.results).to_have_count(3)


def test_search_one_title(search_page):
    search_page.open()
    search_page.search_for("slow")
    expect(search_page.results).to_have_count(1)


def test_search_capital_letters(search_page):
    search_page.open()
    search_page.search_for("NOTES")
    expect(search_page.results).to_have_count(1)


def test_search_by_author(search_page):
    search_page.open()
    search_page.search_for("okafor")
    expect(search_page.results).to_have_count(1)


def test_search_no_match(search_page):
    search_page.open()
    search_page.search_for("zzz")
    expect(search_page.results).to_have_count(0)

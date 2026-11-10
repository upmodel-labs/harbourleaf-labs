"""Step 2: prove each locator with expect(locator).to_be_visible().

The starter takes you to each page. Replace each TODO with your locator, and
write the same locator in locators.md with a one-line reason.
"""
from playwright.sync_api import Page, expect


def test_search_page(page: Page):
    page.goto("/")
    # TODO 1: the search box
    # TODO 2: the search button
    # TODO 3: the search result for the title in taps01_note.md
    #         (a result appears only after a search: do the search first)


def test_book_page(page: Page):
    page.goto("/book.html?id=b1")
    # TODO 4: the quantity
    # TODO 5: the Add to basket button


def test_basket_page(page: Page):
    # The starter puts one book in the basket for you, in one line.
    page.goto("/")
    page.evaluate("localStorage.setItem('practice-shop-basket', JSON.stringify([{id: 'b1', qty: 2}]))")
    page.goto("/basket.html")
    # TODO 6: the basket total

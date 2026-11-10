"""Step 3: the search-to-basket journey, one test. Follow taps01_note.md."""
from playwright.sync_api import Page, expect


def test_search_to_basket_journey(page: Page):
    page.goto("/")
    # search for the title, open that book, set the quantity to 2,
    # add it to the basket, open the basket
    # then assert the number of lines, the quantity on the line and the total text

"""Supplied. You read this in step 4. Do not edit it.

Each fixture builds one page object on the test's own browser page, or loads the book values.
The imports sit inside the functions, so pytest runs before the page objects exist.
"""
import json
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def short_wait(page):
    """A test that cannot find its element fails after 5 seconds, not 30."""
    page.set_default_timeout(5000)


@pytest.fixture
def search_page(page):
    from pages.search_page import SearchPage
    return SearchPage(page)


@pytest.fixture
def book_page(page):
    from pages.book_page import BookPage
    return BookPage(page)


@pytest.fixture
def basket_page(page):
    from pages.basket_page import BasketPage
    return BasketPage(page)


@pytest.fixture
def help_page(page):
    from pages.help_page import HelpPage
    return HelpPage(page)


@pytest.fixture
def books():
    return json.loads((Path(__file__).parent / "data" / "books.json").read_text(encoding="utf-8"))

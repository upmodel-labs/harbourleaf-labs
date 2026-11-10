"""Shared fixtures for the suite.

Supplied: the four page-object fixtures from chapter 3 (they build a page object on the test's own browser page)
and a base_url that points at a shop you start by hand on port 8000 (step 1).
You write: shop_server, books and basket_with_book (step 2), and change base_url (step 2).
Later: a fixture for the test that depends on another (step 4).
"""
import pytest


@pytest.fixture(scope="session")
def base_url():
    # Step 1: the shop you started by hand. Step 2: replace this so it uses your shop_server fixture.
    return "http://localhost:8000"


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


# Step 2: write shop_server (scope session), books (scope session) and basket_with_book (scope function) here.

"""Basket checks. Every test repeats the same set-up: open the book page, choose the quantity, add, open the basket."""
from playwright.sync_api import expect


def test_total_for_two_copies(book_page, basket_page):
    book_page.open("b1")
    book_page.add_to_basket(2)
    basket_page.open()
    expect(basket_page.total).to_have_text("Total: 36.00")


def test_one_line_in_the_basket(book_page, basket_page):
    book_page.open("b1")
    book_page.add_to_basket(2)
    basket_page.open()
    expect(basket_page.lines).to_have_count(1)


def test_quantity_shown_on_the_line(book_page, basket_page):
    book_page.open("b1")
    book_page.add_to_basket(2)
    basket_page.open()
    expect(basket_page.lines.locator(".line-qty")).to_have_text("2")


def test_remove_empties_the_basket(book_page, basket_page):
    book_page.open("b1")
    book_page.add_to_basket(2)
    basket_page.open()
    basket_page.remove("Learning to Test")
    expect(basket_page.lines).to_have_count(0)


def test_place_an_order(book_page, basket_page):
    book_page.open("b1")
    book_page.add_to_basket(2)
    basket_page.open()
    basket_page.place_order()
    expect(basket_page.order_status).to_contain_text("placed")

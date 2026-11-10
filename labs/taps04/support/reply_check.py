"""Supplied. Types an order number into the help box and checks the reply against one row.

check_reply(help_page, row): row is one line of a CSV file read with csv.DictReader. It has the columns
typed, must_hold and must_not_show. must_hold and must_not_show hold words separated by "|" (or nothing).
The reply must hold every must_hold word and show none of the must_not_show words.
Markup typed into the box must come back as text: the reply may not contain any element.
"""
from playwright.sync_api import expect


def _words(text):
    return [word for word in (text or "").split("|") if word]


def check_reply(help_page, row):
    help_page.open()
    reply = help_page.ask_about(row["typed"])
    for word in _words(row["must_hold"]):
        expect(reply).to_contain_text(word)
    for word in _words(row["must_not_show"]):
        expect(reply).not_to_contain_text(word)
    expect(reply.locator("*")).to_have_count(0)

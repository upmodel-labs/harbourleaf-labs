"""The order help box: check what must hold, never one exact sentence (the wording is chosen at random). Supplied."""
import re

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.smoke
def test_help_box_own_order(page: Page):
    page.goto("/help.html")
    page.get_by_label("Order number").fill("BK-1001")
    page.get_by_role("button", name="Ask").click()
    reply = page.get_by_test_id("help-reply")
    expect(reply).to_contain_text("BK-1001")
    expect(reply).to_contain_text(re.compile("shipped|out for delivery|delivered|packed|placed|cancelled"))

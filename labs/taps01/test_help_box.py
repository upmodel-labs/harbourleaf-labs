"""Step 5: the order help box. The reply is worded one of several ways. Check facts, not the sentence."""
from playwright.sync_api import Page, expect


def test_help_box_own_order(page: Page):
    page.goto("/help.html")
    # type BK-1001, press Ask, then assert what must hold

"""Step 6, Attack logs track only. Complete it with one of your three inputs and one assertion."""
from playwright.sync_api import Page, expect


def test_attack_on_the_order_box(page: Page):
    page.goto("/help.html")
    attack = ""  # TODO: one of your three inputs
    page.get_by_label("Order number").fill(attack)
    page.get_by_role("button", name="Ask").click()
    # TODO: one assertion on what the page must never show

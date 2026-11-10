"""The order help box: one journey."""


def test_help_box_says_the_order_is_shipped(help_page):
    help_page.open()
    help_page.order_box.fill("BK-1001")
    help_page.ask_button.click()
    help_page.page.wait_for_timeout(1000)
    assert "shipped" in help_page.reply.inner_text()

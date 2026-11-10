class HelpPage:
    def __init__(self, page):
        self.page = page
        self.order_box = page.get_by_test_id("order-box")
        self.ask_button = page.get_by_test_id("ask-button")
        self.reply = page.get_by_test_id("help-reply")
        self._ready_reply = page.locator("#help-reply.is-ready")

    def open(self):
        self.page.goto("/help.html")

    def ask_about(self, order_id):
        self.order_box.fill(order_id)
        self.ask_button.click()
        self._ready_reply.wait_for()
        return self.reply

    type_into_order_box = ask_about

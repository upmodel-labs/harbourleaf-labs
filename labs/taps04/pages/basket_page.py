class BasketPage:
    def __init__(self, page):
        self.page = page
        self.lines = page.locator(".basket-line")
        self.total = page.get_by_test_id("basket-total")
        self.order_status = page.get_by_test_id("order-status")
        self._remove_button = page.get_by_role("button", name="Remove")
        self._place_order_button = page.get_by_role("button", name="Place order")

    def open(self):
        self.page.goto("/basket.html")

    def remove(self, book_title):
        self.lines.filter(has_text=book_title).get_by_role("button", name="Remove").click()

    def place_order(self):
        self._place_order_button.click()

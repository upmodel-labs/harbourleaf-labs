class BookPage:
    def __init__(self, page):
        self.page = page
        self.title = page.locator("#book-title")
        self.price = page.get_by_test_id("book-price")
        self.quantity = page.get_by_label("Quantity")
        self.add_button = page.get_by_role("button", name="Add to basket")
        self.basket_count = page.get_by_test_id("basket-count")

    def open(self, book_id):
        self.page.goto(f"/book.html?id={book_id}")

    def add_to_basket(self, quantity=1):
        self.quantity.fill(str(quantity))
        self.add_button.click()

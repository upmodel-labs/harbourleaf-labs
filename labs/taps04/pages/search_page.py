class SearchPage:
    def __init__(self, page):
        self.page = page
        self.search_box = page.get_by_label("Search books")
        self.search_button = page.get_by_role("button", name="Search")
        self.results = page.locator(".result-link")
        self.status = page.locator("#search-status")

    def open(self):
        self.page.goto("/")

    def search_for(self, text):
        self.search_box.fill(text)
        self.search_button.click()

    def open_result(self, title):
        self.results.filter(has_text=title).click()

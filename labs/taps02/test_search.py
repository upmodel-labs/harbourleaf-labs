"""Step 3: one clean test of your own. Use the driver fixture, not your own webdriver.Chrome()."""
from selenium.webdriver.common.by import By

BASE = "http://localhost:8000"


def test_search_finds_the_title(driver):
    driver.get(BASE + "/")
    # find the search box by NAME and the Search button by CSS (see selenium_note.md)
    # search for the title in selenium_note.md
    # find the first result and assert that its text is that title
    # no time.sleep: wait for the first result if it is not there yet

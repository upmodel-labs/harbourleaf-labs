import time

from selenium.webdriver.common.by import By

BASE = "http://localhost:8000"


def test_search_with_no_match_says_so(driver):
    driver.get(BASE + "/")
    driver.find_element(By.NAME, "q").send_keys("zzzz")
    driver.find_element(By.CSS_SELECTOR, ".search-button").click()
    time.sleep(4)
    message = driver.find_element(By.XPATH, "//main/section[2]/p")
    assert "No books match" in message.text

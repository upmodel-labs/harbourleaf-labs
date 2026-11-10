import time

from selenium.webdriver.common.by import By

BASE = "http://localhost:8000"


def test_book_page_shows_title_and_price(driver):
    driver.get(BASE + "/book.html?id=b1")
    time.sleep(3)
    title = driver.find_element(By.XPATH, "//main/section/h1")
    price = driver.find_element(By.XPATH, "//main/section/p[1]/span[2]")
    assert title.text == "Learning to Test"
    assert price.text == "18.00"

import time

from selenium.webdriver.common.by import By

BASE = "http://localhost:8000"


def test_add_book_to_basket(driver):
    driver.get(BASE + "/book.html?id=b1")
    time.sleep(1)
    driver.find_element(By.ID, "add-button").click()
    time.sleep(2)
    status = driver.find_element(By.ID, "add-status")
    assert status.text == "Added to basket."
    driver.find_element(By.LINK_TEXT, "Go to your basket").click()
    time.sleep(3)
    lines = driver.find_elements(By.CSS_SELECTOR, ".basket-line")
    assert len(lines) == 1
    assert driver.find_element(By.CSS_SELECTOR, ".line-qty").text == "1"

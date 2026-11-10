import time

from selenium.webdriver.common.by import By

BASE = "http://localhost:8000"


def test_help_box_answers_for_own_order(driver):
    driver.get(BASE + "/help.html")
    driver.find_element(By.ID, "order-box").send_keys("BK-1001")
    driver.find_element(By.CSS_SELECTOR, "[data-testid='ask-button']").click()
    time.sleep(2)
    reply = driver.find_element(By.CSS_SELECTOR, "[data-testid='help-reply']")
    assert "BK-1001" in reply.text

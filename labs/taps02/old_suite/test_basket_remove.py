from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

BASE = "http://localhost:8000"


def test_remove_both_books_from_the_basket(driver):
    driver.get(BASE + "/")
    driver.execute_script(
        "localStorage.setItem('practice-shop-basket', JSON.stringify([{id: 'b1', qty: 1}, {id: 'b2', qty: 1}]))"
    )
    driver.get(BASE + "/basket.html")
    wait = WebDriverWait(driver, 10)
    wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, ".basket-line")) == 2)
    rows = driver.find_elements(By.CSS_SELECTOR, ".basket-line")
    rows[0].find_element(By.CSS_SELECTOR, ".remove-button").click()
    wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, ".basket-line")) == 1)
    rows[1].find_element(By.CSS_SELECTOR, ".remove-button").click()
    wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, ".basket-line")) == 0)
    assert driver.find_element(By.ID, "basket-empty").is_displayed()

from selenium.webdriver.common.by import By

BASE = "http://localhost:8000"


def test_search_finds_three_books(driver):
    driver.implicitly_wait(10)
    driver.get(BASE + "/")
    driver.find_element(By.XPATH, "//main/section[1]/form/div/input").send_keys("test")
    driver.find_element(By.CSS_SELECTOR, ".search-button").click()
    results = driver.find_elements(By.CSS_SELECTOR, ".result")
    assert len(results) == 3

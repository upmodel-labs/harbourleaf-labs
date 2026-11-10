"""Step 7, Attack logs track: the HTML snippet from selenium_note.md, typed into the order box. Run it only against your own practice shop."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE = "http://localhost:8000"


def test_html_is_shown_as_text(driver):
    driver.get(BASE + "/help.html")
    attack = ""  # GAP 1: the input to type (the HTML snippet from the note)
    driver.find_element(By.ID, "order-box").send_keys(attack)
    driver.find_element(By.CSS_SELECTOR, "[data-testid='ask-button']").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".reply.is-ready")))
    # GAP 2: assert that the page shows the snippet as text, and that find_elements
    # finds no element of that tag inside the reply

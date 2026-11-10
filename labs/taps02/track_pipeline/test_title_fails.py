"""Supplied. It fails on purpose, so your fixture has a failure to photograph."""
from selenium.webdriver.common.by import By

BASE = "http://localhost:8000"


def test_title_is_what_the_team_expects(driver):
    driver.get(BASE + "/")
    assert driver.title == "Practice Bookshop home"

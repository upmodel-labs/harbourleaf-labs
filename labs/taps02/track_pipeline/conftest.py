"""Step 7, Pipeline track: a copy of the driver fixture with two gaps. Fill gap 1 and gap 2."""
import pytest
from selenium import webdriver


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Supplied: stores each phase's result on the test item, so a fixture can read it."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)


@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    # GAP 1: make the browser headless. Add the option here.
    options.add_argument("--window-size=1280,900")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    # GAP 2: if the test failed, save a screenshot with driver.save_screenshot("...png").
    # The result of the test body is request.node.rep_call, and it has a .failed value.
    driver.quit()

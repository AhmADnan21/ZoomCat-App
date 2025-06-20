import pytest
from selenium.webdriver.chrome.webdriver import WebDriver
from pages.home_page import HomePage  # type: ignore
import time

def check_and_refresh_on_server_error(driver: WebDriver, url: str, wait_time=2):
    driver.get(url)
    time.sleep(wait_time)  # short wait before checking

    if "Server error" in driver.page_source:
        print("⚠️ Server error detected, refreshing page...")
        driver.refresh()
        driver.implicitly_wait(15)

@pytest.fixture
def setup():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.maximize_window()
    driver.implicitly_wait(15)

    yield driver

    driver.quit()

@pytest.fixture
def homepage_url():
    return "https://test-ipglobal.cd.xiaoxigroup.net/en"

def test_HP001_homepage_elements_visible(setup: WebDriver, homepage_url):
    check_and_refresh_on_server_error(setup, homepage_url)
    page = HomePage(setup)
    page.verify_main_sections()

def test_HP002_proxies_menu_hover_panel_appears(setup: WebDriver, homepage_url):
    check_and_refresh_on_server_error(setup, homepage_url)
    page = HomePage(setup)
    page.hover_over_proxies_menu()
    setup.implicitly_wait(1)  # brief wait to help rendering
    assert setup.find_element(*page.proxies_panel).is_displayed()

def test_HP003_proxies_dropdown_links_visible(setup: WebDriver, homepage_url):
    check_and_refresh_on_server_error(setup, homepage_url)
    page = HomePage(setup)
    page.hover_over_proxies_menu()
    page.verify_proxies_dropdown()

# ✅ Take screenshot if test fails
import os
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("setup")
        if driver:
            os.makedirs("reports", exist_ok=True)
            screenshot_path = f"reports/{item.name}.png"
            driver.save_screenshot(screenshot_path)
            print(f"\n📸 Screenshot saved to {screenshot_path}")

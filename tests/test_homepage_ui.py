from typing import Literal
from selenium.webdriver.chrome.webdriver import WebDriver
from pages.home_page import HomePage  # type: ignore
from pages.home_page import HomePage  # type: ignore

def test_HP001_homepage_elements_visible(setup: WebDriver, homepage_url: Literal['https://test-ipglobal.cd.xiaoxigroup.net/en']):
    setup.get(homepage_url)
    check_and_refresh_on_server_error(setup, homepage_url)  # <-- add this line
    page = HomePage(setup)
    page.verify_main_sections()

def test_HP002_proxies_menu_hover_panel_appears(setup: WebDriver, homepage_url: Literal['https://test-ipglobal.cd.xiaoxigroup.net/en']):
    setup.get(homepage_url)
    check_and_refresh_on_server_error(setup, homepage_url)  # <-- add this line
    page = HomePage(setup)
    page.hover_over_proxies_menu()
    setup.implicitly_wait(1)  # brief wait to help rendering
    assert setup.find_element(*page.proxies_panel).is_displayed()

def test_HP003_proxies_dropdown_links_visible(setup: WebDriver, homepage_url: Literal['https://test-ipglobal.cd.xiaoxigroup.net/en']):
    setup.get(homepage_url)
    check_and_refresh_on_server_error(setup, homepage_url)  # <-- add this line
    page = HomePage(setup)
    page.hover_over_proxies_menu()
    page.verify_proxies_dropdown()

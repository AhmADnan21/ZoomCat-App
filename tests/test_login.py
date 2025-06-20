from pages.login_page import LoginPage
from utils.config import USERNAME, PASSWORD  # Import credentials from config

def test_valid_login(setup):
    login_page = LoginPage(setup)
    
    # Assert the title before logging in
    assert login_page.get_title_before_login() == "Log in", "Title before login is incorrect"
    
    # Use credentials from .env
    login_page.login(USERNAME, PASSWORD)
    
    # Assert the title after logging in
    assert login_page.get_title_after_login() == "Welcome,Okey Proxy!", "Title after login is incorrect"
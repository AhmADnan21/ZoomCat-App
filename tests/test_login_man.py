from pages.login_page import LoginPage


def test_valid_login(setup):
    login_page = LoginPage(setup)
    
    # Assert the title before logging in
    assert login_page.get_title_before_login() == "Log in", "Title before login is incorrect"
    
    # Perform login
    login_page.login("ahmad21@getnada.com", "Ahmad21@")
    
    # Assert the title after logging in
    assert login_page.get_title_after_login() == "Welcome,Okey Proxy!", "Title after login is incorrect"

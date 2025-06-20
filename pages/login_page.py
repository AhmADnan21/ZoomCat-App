from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        # XPath selectors based on your provided data
        self.username = (By.XPATH, '//*[@id="__layout"]/div/div[2]/div[1]/div[2]/form/div[1]/div/div/input')
        self.password = (By.XPATH, '//*[@id="__layout"]/div/div[2]/div[1]/div[2]/form/div[2]/div/div/input')
        self.login_button = (By.XPATH, '//*[@id="__layout"]/div/div[2]/div[1]/div[2]/div[4]/button')
        self.login_title = (By.XPATH, '//*[@id="__layout"]/div/div[2]/div[1]/div[2]/div[1]')
        self.dashboard_title = (By.XPATH, '//*[@id="__layout"]/section/section/header/div/div[1]/div/span/span')

    def login(self, user, pwd):
        self.driver.find_element(*self.username).send_keys(user)
        self.driver.find_element(*self.password).send_keys(pwd)
        self.driver.find_element(*self.login_button).click()

    def get_title_before_login(self):
        return self.driver.find_element(*self.login_title).text

    def get_title_after_login(self):
        try:
            # Wait up to 15 seconds for the dashboard element to be visible
            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.dashboard_title)
            )
            return self.driver.find_element(*self.dashboard_title).text
        except Exception as e:
            # Print page source to help you debug if the element wasn't found
            print("⚠️ Could not find dashboard title. Page source:")
            print(self.driver.page_source)
            raise e  # Re-raise the original error so test still fails

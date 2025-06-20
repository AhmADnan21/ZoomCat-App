from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

        # Static elements
        self.logo = (By.XPATH, '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[1]/div/a/img')
        self.nav_bar = (By.XPATH, '//*[@id="__layout"]/div/div[2]/div[2]')
        self.headline = (By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div/div[1]/div[1]/h1')
        self.proxies_pricing = (By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div/div[2]/h2')
        self.datacenter_proxies = (By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div/div[3]/div[3]/div/h2')
        self.top_locations = (By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div/div[4]/div[1]/h2')
        self.why_choose = (By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div/div[5]/h2')
        self.testimonials = (By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div/div[6]/div[1]/h2')
        self.use_cases = (By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div/div[7]/div/h2')
        self.blog = (By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div/div[8]/div[1]/h2')
        self.trusted_by = (By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div/div[9]/div[1]/h2')
        self.free_trial = (By.XPATH, '//*[@id="__layout"]/div/div[4]/div/div/h2')

        # Hover elements
        self.proxies_menu = (By.XPATH, '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div[1]')
        self.proxies_panel = (By.XPATH, '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div[2]')
        self.rotating_proxies = (By.XPATH, '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div/a/div/div[3]/div[1]')
        self.static_isp_proxies = (By.XPATH, '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div/a/div/div[3]/div[1]')
        self.datacenter_proxies_hover = (By.XPATH, '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div[3]/div/a/div/div[3]/div[1]')
        self.more_locations = [
            '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div/a/div/div[3]/div',  # US
            '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[3]/div/a/div/div[3]/div',  # Russia
            '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[8]/div/a/div/div[3]/div',  # Pakistan
            '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[9]/div/a/div/div[3]/div',  # South Korea
        ]

    def verify_main_sections(self):
        elements = [
            self.logo, self.nav_bar, self.headline, self.proxies_pricing,
            self.datacenter_proxies, self.top_locations, self.why_choose,
            self.testimonials, self.use_cases, self.blog, self.trusted_by,
            self.free_trial
        ]
        for locator in elements:
            self.wait.until(EC.visibility_of_element_located(locator))

    def hover_over_proxies_menu(self):
        action = ActionChains(self.driver)
        menu = self.wait.until(EC.visibility_of_element_located(self.proxies_menu))
        action.move_to_element(menu).perform()
        self.wait.until(EC.visibility_of_element_located(self.proxies_panel))

    def verify_proxies_dropdown(self):
        items = [
            self.rotating_proxies,
            self.static_isp_proxies,
            self.datacenter_proxies_hover,
        ] + [(By.XPATH, xpath) for xpath in self.more_locations]

        for locator in items:
            self.wait.until(EC.visibility_of_element_located(locator))

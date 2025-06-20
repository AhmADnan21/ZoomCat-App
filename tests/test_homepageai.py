from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# ==== Configuration ====
HOMEPAGE_URL = "https://test-ipglobal.cd.xiaoxigroup.net/en"
driver = webdriver.Chrome()  # Ensure chromedriver is in your PATH
wait = WebDriverWait(driver, 10)
results = []

try:
    driver.get(HOMEPAGE_URL)

    # --- 1. Check main homepage elements ---
    homepage_checks = [
        ("Logo", By.XPATH, '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[1]/div/a/img'),
        ("Navigation Bar", By.XPATH, '//*[@id="__layout"]/div/div[2]/div[2]'),
        ("Main Headline", By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div/div[1]/div[1]/h1'),
        ("Proxies Pricing", By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div/div[2]/h2'),
        ("Rotating Residential Proxies", By.XPATH, '//*[contains(text(),"Rotating Residential Proxies") or contains(text(),"Rotating Residential")]'),
        ("Static ISP Residential Proxies", By.XPATH, '//*[contains(text(),"Static ISP Residential Proxies") or contains(text(),"Static ISP")]'),
        ("Datacenter Proxies", By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div/div[3]/div[3]/div/h2'),
        ("Top Locations", By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div/div[4]/div[1]/h2'),
        ("Why Choose OkeyProxy", By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div/div[5]/h2'),
        ("Customer Testimonials", By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div/div[6]/div[1]/h2'),
        ("Use Cases", By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div/div[7]/div/h2'),
        ("OkeyProxy Blog", By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div/div[8]/div[1]/h2'),
        ("Trusted by Thousands of Partners", By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div/div[9]/div[1]/h2'),
        ("Start Your Free Trial Now!", By.XPATH, '//*[@id="__layout"]/div/div[4]/div/div/h2')
    ]

    for label, by, locator in homepage_checks:
        try:
            wait.until(EC.visibility_of_element_located((by, locator)))
            results.append((label, "Visible"))
        except Exception as e:
            results.append((label, f"Not visible: {str(e)}"))

    # --- 2. Hover over "Proxies" and validate options ---
    proxies_menu = wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div[1]')
    ))
    ActionChains(driver).move_to_element(proxies_menu).perform()
    time.sleep(1)

    # Dropdown panel items
    menu_checks = [
        ("Rotating & Residential Proxies", By.XPATH, '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div/a/div/div[3]/div[1]'),
        ("Static Residential Proxies (ISP)", By.XPATH, '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div/a/div/div[3]/div[1]'),
        ("Datacenter Proxies", By.XPATH, '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div[3]/div/a/div/div[3]/div[1]'),
        ("Top Locations", By.XPATH, '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[1]/div/div[1]/div/a/div/div[3]/div[1]'),
        ("More Locations", By.XPATH, '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div[1]/div/div[1]')
    ]

    menu_countries = [
        ("US", '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div/a/div/div[3]/div'),
        ("UK", '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/div/a/div/div[3]/div'),
        ("Russia", '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[3]/div/a/div/div[3]/div'),
        ("Japan", '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[4]/div/a/div/div[3]/div'),
        ("Indonesia", '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[5]/div/a/div/div[3]/div'),
        ("Spain", '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[6]/div/a/div/div[3]/div'),
        ("India", '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[7]/div/a/div/div[3]/div'),
        ("Pakistan", '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[8]/div/a/div/div[3]/div'),
        ("South Korea", '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[9]/div/a/div/div[3]/div'),
    ]

    for label, by, locator in menu_checks:
        try:
            wait.until(EC.visibility_of_element_located((by, locator)))
            results.append((f"Menu: {label}", "Visible"))
        except Exception as e:
            results.append((f"Menu: {label}", f"Not visible: {str(e)}"))

    for label, locator in menu_countries:
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, locator)))
            results.append((f"Menu Country: {label}", "Visible"))
        except Exception as e:
            results.append((f"Menu Country: {label}", f"Not visible: {str(e)}"))

finally:
    print(f"{'Test Item':35} | Result")
    print('-'*60)
    for test, outcome in results:
        print(f"{test:35} | {outcome}")

    driver.quit()
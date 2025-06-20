import os
import sys
import time
from datetime import datetime
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Appium Configuration
APPIUM_SERVER = "http://localhost:4723"
CAPABILITIES = {
    "platformName": "Android",
    "appium:deviceName": "10AE9G0SJS001BT",
    "appium:automationName": "UiAutomator2",
    "appium:appPackage": "com.zoomcat.app",
    "appium:appActivity": "io.dcloud.PandoraEntryActivity",
    "appium:noReset": True
}

# Element Locators for Purchase Successful Flow Test
class Locators:
    # Purchase Flow Locators
    BUY_TAB = "//android.widget.TextView[@resource-id=\"com.zoomcat.app:id/tabTV\" and @text=\"Buy\"]"
    PURCHASE_BUTTON = "//android.view.View[@content-desc=\"Purchase\"]"
    GOOGLE_PLAY_IMAGE = "//android.widget.ImageView[@content-desc=\"Google Play\"]"
    ONE_TAP_BUY_BUTTON = "(//android.widget.FrameLayout[@resource-id=\"com.android.vending:id/0_resource_name_obfuscated\"])[8]"
    PURCHASE_SUCCESSFUL_SCREEN = "//android.view.View[@content-desc=\"Purchase successful\"]"
    GO_TO_CONNECT_BUTTON = "/hierarchy/android.widget.FrameLayout"
    PROFILE_ICON_CONNECT_PAGE = "//android.widget.ScrollView/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ImageView"

class PurchaseSuccessfulFlowTest:
    def __init__(self):
        self.driver = None
        self.report_dir = None
        self.test_name = "Purchase Successful Flow"
        
    def setup_driver(self):
        """Initialize the mobile driver"""
        print("=== Starting mobile driver initialization ===")
        try:
            self.driver = webdriver.Remote(APPIUM_SERVER, CAPABILITIES)
            print("Mobile driver initialized successfully")
            return True
        except Exception as e:
            print(f"Failed to initialize mobile driver: {e}")
            return False
    
    def take_screenshot(self, step_name):
        """Take a screenshot and save it to the report directory"""
        if self.driver and self.report_dir:
            timestamp = datetime.now().strftime("%H%M%S")
            filename = f"{step_name}_{timestamp}.png"
            filepath = os.path.join(self.report_dir, filename)
            self.driver.get_screenshot_as_file(filepath)
            print(f"Screenshot saved: {filepath}")
            return filepath
        return None
    
    def wait_for_element(self, locator, timeout=10, element_type="XPATH"):
        """Wait for an element to be present and return it"""
        try:
            if element_type == "XPATH":
                element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.XPATH, locator))
                )
            else:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.ID, locator))
                )
            return element
        except TimeoutException:
            print(f"Element not found within {timeout} seconds: {locator}")
            return None
    
    def click_element(self, locator, timeout=10, element_type="XPATH"):
        """Click on an element with wait"""
        element = self.wait_for_element(locator, timeout, element_type)
        if element:
            try:
                element.click()
                return True
            except Exception as e:
                print(f"Failed to click element: {e}")
                return False
        return False
    
    def run_purchase_successful_flow_test(self):
        """Run the Purchase Successful Flow test"""
        print(f"\n=== Starting {self.test_name} ===")
        
        try:
            # Step 1: Click the Buy tab
            print("--- Step 1: Click Buy Tab ---")
            if self.click_element(Locators.BUY_TAB):
                print("Buy tab clicked successfully")
                self.take_screenshot("01_buy_tab_clicked")
            else:
                print("Failed to click Buy tab")
                return False
            
            # Check if purchase successful screen appears immediately
            print("--- Checking for immediate purchase success screen ---")
            if self.wait_for_element(Locators.PURCHASE_SUCCESSFUL_SCREEN, timeout=3):
                print("Purchase successful screen appeared immediately - handling cached state")
                self.take_screenshot("01a_immediate_purchase_success")
                
                # Click Go to Connect button
                print("--- Clicking Go to Connect button ---")
                if self.click_element(Locators.GO_TO_CONNECT_BUTTON):
                    print("Go to Connect button clicked successfully")
                    self.take_screenshot("01b_go_to_connect_clicked")
                else:
                    print("Failed to click Go to Connect button")
                    return False
                
                # Wait for Connect page to load
                print("--- Waiting for Connect page to load ---")
                if self.wait_for_element(Locators.PROFILE_ICON_CONNECT_PAGE):
                    print("Connect page loaded successfully")
                    self.take_screenshot("01c_connect_page_loaded")
                else:
                    print("Connect page did not load")
                    return False
                
                # Wait a moment for page to stabilize
                time.sleep(3)
                
                # Restart test from Step 1
                print("--- Restarting test from Step 1 ---")
                return self.run_purchase_successful_flow_test()
            
            # Step 2: Wait for Purchase page
            print("--- Step 2: Wait for Purchase Page ---")
            if self.wait_for_element(Locators.PURCHASE_BUTTON):
                print("Purchase page appeared successfully")
                self.take_screenshot("02_purchase_page_loaded")
            else:
                print("Purchase page did not appear")
                return False
            time.sleep(5)
            
            # Step 3: Click Purchase button
            print("--- Step 3: Click Purchase Button ---")
            if self.click_element(Locators.PURCHASE_BUTTON):
                print("Purchase button clicked successfully")
                self.take_screenshot("03_purchase_button_clicked")
            else:
                print("Failed to click Purchase button")
                return False
            
            # Step 4: Wait for Google Play payment screen
            print("--- Step 4: Wait for Google Play Payment Screen ---")
            if self.wait_for_element(Locators.GOOGLE_PLAY_IMAGE):
                print("Google Play payment screen appeared successfully")
                self.take_screenshot("04_google_play_screen")
            else:
                print("Google Play payment screen did not appear")
                return False
            
            # Step 5: Click 1-tap buy button
            print("--- Step 5: Click 1-tap Buy Button ---")
            if self.click_element(Locators.ONE_TAP_BUY_BUTTON):
                print("1-tap buy button clicked successfully")
                self.take_screenshot("05_one_tap_buy_clicked")
            else:
                print("Failed to click 1-tap buy button")
                return False
            
            # Step 6: Wait for 5 seconds
            print("--- Step 6: Waiting 5 seconds ---")
            time.sleep(5)
            
            # Step 7: Verify Purchase successful screen
            print("--- Step 7: Verify Purchase Successful Screen ---")
            if self.wait_for_element(Locators.PURCHASE_SUCCESSFUL_SCREEN):
                print("Purchase successful screen appeared")
                self.take_screenshot("06_purchase_successful_screen")
            else:
                print("Purchase successful screen did not appear")
                return False
            
            # Step 8: Click Go to Connect button
            print("--- Step 8: Click Go to Connect Button ---")
            if self.click_element(Locators.GO_TO_CONNECT_BUTTON):
                print("Go to Connect button clicked successfully")
                self.take_screenshot("07_go_to_connect_clicked")
            else:
                print("Failed to click Go to Connect button")
                return False
            
            # Step 9: Wait for Connect page and locate profile icon
            print("--- Step 9: Wait for Connect Page and Profile Icon ---")
            if self.wait_for_element(Locators.PROFILE_ICON_CONNECT_PAGE):
                print("Connect page loaded and profile icon found")
                self.take_screenshot("08_connect_page_loaded")
            else:
                print("Connect page did not load or profile icon not found")
                return False
            
            # Step 10: Wait for 5 seconds
            print("--- Step 10: Waiting 5 seconds ---")
            time.sleep(5)
            
            print(f"{self.test_name} completed: PASSED")
            return True
            
        except Exception as e:
            print(f"Error during {self.test_name}: {e}")
            self.take_screenshot(f"error_{self.test_name.lower().replace(' ', '_')}")
            return False
    
    def run_test(self):
        """Main test execution method"""
        # Create report directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.report_dir = os.path.join("reports", f"{self.test_name}_{timestamp}")
        os.makedirs(self.report_dir, exist_ok=True)
        
        print(f"\n=== Running ZoomCat Mobile {self.test_name} with report directory: {os.path.abspath(self.report_dir)} ===")
        
        # Initialize driver
        if not self.setup_driver():
            return False
        
        try:
            # Wait for app to load
            print("Waiting for app to load completely...")
            time.sleep(5)
            self.take_screenshot("1-1_driver_initialized")
            
            # Run the test
            success = self.run_purchase_successful_flow_test()
            
            # Final screenshot
            self.take_screenshot("final_success" if success else "final_error")
            
            return success
            
        finally:
            # Cleanup
            if self.driver:
                print("=== Cleaning up and closing mobile driver ===")
                self.driver.quit()

def main():
    """Main execution function"""
    test = PurchaseSuccessfulFlowTest()
    success = test.run_test()
    
    print(f"\n=== Script execution completed with exit code: {0 if success else 1} ===")
    return 0 if success else 1

if __name__ == "__main__":
    exit(main()) 
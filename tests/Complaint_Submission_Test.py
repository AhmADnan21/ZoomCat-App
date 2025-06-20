import os
import sys
import time
import random
import string
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

# Element Locators for Complaint Submission Test
class Locators:
    # Complaint Submission Locators
    BLOG_TAB = "//android.widget.TextView[@resource-id=\"com.zoomcat.app:id/tabTV\" and @text=\"Blog\"]"
    AT_9365 = "//android.view.View[@content-desc=\"AT_9365\"]"
    AT_ARTICLE_459461 = "//android.view.View[@content-desc=\"AT_article_459461\"]"
    COMPLAINT_BUTTON = "//android.view.View[@content-desc=\"Complaint\"]"
    COMPLAINT_DETAILS_FIELD = "//android.widget.EditText[@text=\"Please provide more details here\"]"
    SUBMIT_BUTTON = "//android.view.View[@content-desc=\"Submit\"]"
    SUBMIT_SUCCESSFULLY_MESSAGE = "//android.view.View[@content-desc=\"Submit successfully\"]"
    BACK_BUTTON = "//android.widget.FrameLayout[@resource-id=\"android:id/content\"]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ImageView"
    CONNECT_TAB = "//android.widget.TextView[@resource-id=\"com.zoomcat.app:id/tabTV\" and @text=\"Connect\"]"
    PROFILE_ICON_CONNECT_PAGE = "//android.widget.ScrollView/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ImageView"

class ComplaintSubmissionTest:
    def __init__(self):
        self.driver = None
        self.report_dir = None
        self.test_name = "Complaint Submission"
        
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
    
    def enter_text(self, locator, text, timeout=10, element_type="XPATH"):
        """Enter text in an element with wait"""
        element = self.wait_for_element(locator, timeout, element_type)
        if element:
            try:
                element.clear()
                element.send_keys(text)
                return True
            except Exception as e:
                print(f"Failed to enter text: {e}")
                return False
        return False
    
    def hide_keyboard(self):
        """Hide the keyboard"""
        try:
            self.driver.hide_keyboard()
            print("Keyboard hidden successfully")
            return True
        except Exception as e:
            print(f"Failed to hide keyboard: {e}")
            return False
    
    def generate_random_text(self):
        """Generate random text for complaint"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        return f"Test_{random_chars}-{timestamp}"
    
    def run_complaint_submission_test(self):
        """Run the Complaint Submission test"""
        print(f"\n=== Starting {self.test_name} ===")
        
        try:
            # Step 1: Click the Blog tab
            print("--- Step 1: Click Blog Tab ---")
            if self.click_element(Locators.BLOG_TAB):
                print("Blog tab clicked successfully")
                self.take_screenshot("01_blog_tab_clicked")
            else:
                print("Failed to click Blog tab")
                return False
            
            # Step 2: Wait for AT_9365 to appear
            print("--- Step 2: Wait for AT_9365 ---")
            if self.wait_for_element(Locators.AT_9365):
                print("AT_9365 appeared successfully")
                self.take_screenshot("02_at_9365_found")
            else:
                print("AT_9365 did not appear")
                return False
            
            # Step 3: Click on AT_9365
            print("--- Step 3: Click on AT_9365 ---")
            if self.click_element(Locators.AT_9365):
                print("AT_9365 clicked successfully")
                self.take_screenshot("03_at_9365_clicked")
            else:
                print("Failed to click AT_9365")
                return False
            
            # Step 4: Wait for AT_article_459461 to appear
            print("--- Step 4: Wait for AT_article_459461 ---")
            if self.wait_for_element(Locators.AT_ARTICLE_459461):
                print("AT_article_459461 appeared successfully")
                self.take_screenshot("04_at_article_found")
            else:
                print("AT_article_459461 did not appear")
                return False
            
            # Step 5: Click on AT_article_459461
            print("--- Step 5: Click on AT_article_459461 ---")
            if self.click_element(Locators.AT_ARTICLE_459461):
                print("AT_article_459461 clicked successfully")
                self.take_screenshot("05_at_article_clicked")
            else:
                print("Failed to click AT_article_459461")
                return False
            
            # Step 6: Wait for Complaint button to appear
            print("--- Step 6: Wait for Complaint Button ---")
            if self.wait_for_element(Locators.COMPLAINT_BUTTON):
                print("Complaint button appeared successfully")
                self.take_screenshot("06_complaint_button_found")
            else:
                print("Complaint button did not appear")
                return False
            
            # Step 7: Click on Complaint button
            print("--- Step 7: Click on Complaint Button ---")
            if self.click_element(Locators.COMPLAINT_BUTTON):
                print("Complaint button clicked successfully")
                self.take_screenshot("07_complaint_button_clicked")
            else:
                print("Failed to click Complaint button")
                return False
            
            # Step 8: Wait for complaint details field
            print("--- Step 8: Wait for Complaint Details Field ---")
            if self.wait_for_element(Locators.COMPLAINT_DETAILS_FIELD):
                print("Complaint details field appeared successfully")
                self.take_screenshot("08_complaint_field_found")
            else:
                print("Complaint details field did not appear")
                return False
            
            # Step 9: Enter random text in the field
            print("--- Step 9: Enter Random Text ---")
            random_text = self.generate_random_text()
            if self.enter_text(Locators.COMPLAINT_DETAILS_FIELD, random_text):
                print(f"Random text entered successfully: {random_text}")
                self.take_screenshot("09_text_entered")
            else:
                print("Failed to enter text")
                return False
            
            # Step 10: Hide keyboard
            print("--- Step 10: Hide Keyboard ---")
            self.hide_keyboard()
            time.sleep(2)
            
            # Step 11: Look for Submit button
            print("--- Step 11: Look for Submit Button ---")
            if self.wait_for_element(Locators.SUBMIT_BUTTON):
                print("Submit button found successfully")
                self.take_screenshot("10_submit_button_found")
            else:
                print("Submit button not found")
                return False
            
            # Step 12: Click on Submit button
            print("--- Step 12: Click on Submit Button ---")
            if self.click_element(Locators.SUBMIT_BUTTON):
                print("Submit button clicked successfully")
                self.take_screenshot("11_submit_button_clicked")
            else:
                print("Failed to click Submit button")
                return False
            
            # Step 13: Verify Submit successfully message
            print("--- Step 13: Verify Submit Successfully Message ---")
            if self.wait_for_element(Locators.SUBMIT_SUCCESSFULLY_MESSAGE):
                print("Submit successfully message appeared")
                self.take_screenshot("12_submit_successful")
            else:
                print("Submit successfully message did not appear")
                return False
            
            # Step 14: Wait for 5 seconds
            print("--- Step 14: Waiting 5 seconds ---")
            time.sleep(5)
            
            # Step 15: Click Back button
            print("--- Step 15: Click Back Button ---")
            if self.click_element(Locators.BACK_BUTTON):
                print("Back button clicked successfully")
                self.take_screenshot("13_back_button_clicked")
            else:
                print("Failed to click Back button")
                return False
            
            # Step 16: Wait for 5 seconds
            print("--- Step 16: Waiting 5 seconds ---")
            time.sleep(5)
            
            # Step 17: Click on Connect tab
            print("--- Step 17: Click on Connect Tab ---")
            if self.click_element(Locators.CONNECT_TAB):
                print("Connect tab clicked successfully")
                self.take_screenshot("14_connect_tab_clicked")
            else:
                print("Failed to click Connect tab")
                return False
            
            # Step 18: Verify user is redirected to Connect page
            print("--- Step 18: Verify Connect Page ---")
            if self.wait_for_element(Locators.PROFILE_ICON_CONNECT_PAGE):
                print("User redirected to Connect page successfully")
                self.take_screenshot("15_connect_page_verified")
            else:
                print("User not redirected to Connect page")
                return False
            
            # Step 19: Wait for 5 seconds
            print("--- Step 19: Waiting 5 seconds ---")
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
            success = self.run_complaint_submission_test()
            
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
    test = ComplaintSubmissionTest()
    success = test.run_test()
    
    print(f"\n=== Script execution completed with exit code: {0 if success else 1} ===")
    return 0 if success else 1

if __name__ == "__main__":
    exit(main()) 
"""
Appium Test Automation for Mobile Login System - ZoomCat App
This script automates the process of:
1. Mobile app initialization and connection
2. Email-based login with verification code
3. Terms and conditions acceptance
4. Login validation and verification
5. Comprehensive reporting and screenshot capture
"""

# ===== Imports =====
import time
import pytest
import os
from datetime import datetime
from pathlib import Path
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, InvalidElementStateException
from selenium.webdriver.common.action_chains import ActionChains
from appium.webdriver.common.mobileby import MobileBy
from typing import Tuple, List, Optional
from selenium.webdriver.common.keys import Keys

# ===== Global Configuration =====
class Config:
    """Centralized configuration class"""
    # Appium Capabilities
    CAPABILITIES = {
        "platformName": "Android",
        "appium:deviceName": "10AE9G0SJS001BT",
        "appium:automationName": "UiAutomator2",
        "appium:appPackage": "com.zoomcat.app",
        "appium:appActivity": "io.dcloud.PandoraEntryActivity",
        "appium:noReset": True
    }

    # Appium Server
    APPIUM_SERVER = "http://localhost:4723"

    # Test Credentials
    TEST_EMAIL = "zoomcatcs01@gmail.com"
    TEST_VERIFICATION_CODE = "999999"

    # Element Locators
    class Locators:
        EMAIL_FIELD = "//android.widget.ScrollView/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]"
        VERIFICATION_CODE_FIELD = "//android.widget.ScrollView/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]"
        TERMS_CHECKBOX = "//android.widget.ScrollView/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[3]/android.widget.FrameLayout[1]/android.widget.FrameLayout"
        LOGIN_BUTTON = "//android.widget.ScrollView/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.widget.FrameLayout"
        PROFILE_ICON = "//android.widget.ScrollView/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ImageView"

# ===== Utility Functions =====
def create_report_dir(test_name="Login via Verification Code test"):
    """Creates a timestamped directory for test reports"""
    report_dir = os.path.join(os.getcwd(), "reports")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_dir = os.path.join(report_dir, f"{test_name}_{timestamp}")
    os.makedirs(test_dir)
    return test_dir

def take_screenshot(driver, step_name, report_dir):
    """Takes and saves a screenshot with the given step name"""
    screenshot_path = os.path.join(report_dir, f"{step_name}.png")
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved: {screenshot_path}")

def highlight_and_wait(driver, element, wait_time=1):
    """Highlights an element with a red border and waits"""
    try:
        driver.execute_script("arguments[0].style.border='3px solid red'", element)
        time.sleep(wait_time)
    except Exception:
        # Mobile elements don't support style modification, just wait
        time.sleep(wait_time)

def interact_with_element(driver, element, action, step_name, report_dir, wait_time=1, **kwargs):
    """Handles element interaction with screenshots and highlighting"""
    try:
        highlight_and_wait(driver, element, 1)
        
        if action == "click":
            element.click()
        elif action == "send_keys":
            element.send_keys(kwargs.get('keys', ''))
        elif action == "clear":
            element.clear()
        elif action == "clear_and_send":
            element.clear()
            element.send_keys(kwargs.get('keys', ''))
        
        time.sleep(wait_time)
        take_screenshot(driver, step_name, report_dir)
        
    except Exception as e:
        take_screenshot(driver, f"error_{step_name}", report_dir)
        raise Exception(f"Failed to {action} element: {str(e)}")

def wait_for_app_load(driver, wait):
    """Wait for the mobile app to load completely"""
    try:
        print("Waiting for app to load completely...")
        time.sleep(5)  # Initial wait for app startup
        print("App loaded successfully")
    except Exception:
        print("App load timeout")
        raise

# ===== Driver Setup Utilities =====
class DriverUtils:
    """Utility class for driver setup and configuration"""
    
    @staticmethod
    def create_driver_options() -> UiAutomator2Options:
        """Create and configure UiAutomator2Options with all necessary capabilities"""
        options = UiAutomator2Options()
        
        # Set basic capabilities
        for key, value in Config.CAPABILITIES.items():
            if key.startswith("appium:"):
                options.set_capability(key, value)
            else:
                setattr(options, key.lower().replace("name", "_name"), value)
        
        # Add stability capabilities
        stability_caps = {
            "newCommandTimeout": 300,
            "autoGrantPermissions": True,
            "autoAcceptAlerts": True,
            "waitForIdleTimeout": 0,
            "androidInstallTimeout": 90000,
            "adbExecTimeout": 60000
        }
        
        for cap, value in stability_caps.items():
            options.set_capability(cap, value)
            
        return options

class LocatorStrategy:
    """Utility class to handle multiple locator strategies"""
    
    @staticmethod
    def get_input_field_locators(field_xpath: str, instance: int = 0) -> List[Tuple[str, str]]:
        """Get multiple locator strategies for input fields"""
        return [
            (By.XPATH, field_xpath),
            (MobileBy.CLASS_NAME, "android.widget.EditText"),
            (MobileBy.ANDROID_UIAUTOMATOR, f'new UiSelector().className("android.widget.EditText").instance({instance})')
        ]
    
    @staticmethod
    def get_checkbox_locators(checkbox_xpath: str) -> List[Tuple[str, str]]:
        """Get multiple locator strategies for checkboxes"""
        return [
            (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.CheckBox").instance(0)'),
            (By.XPATH, checkbox_xpath),
            (MobileBy.CLASS_NAME, "android.widget.CheckBox")
        ]
    
    @staticmethod
    def get_button_locators(button_xpath: str) -> List[Tuple[str, str]]:
        """Get multiple locator strategies for buttons"""
        return [
            (By.XPATH, button_xpath),
            (MobileBy.CLASS_NAME, "android.widget.Button")
        ]

# ===== Test Step Functions =====
def initialize_mobile_driver(report_dir):
    """Initialize mobile driver with proper configuration"""
    try:
        print("\n=== Starting mobile driver initialization ===")
        
        options = DriverUtils.create_driver_options()
        driver = webdriver.Remote(Config.APPIUM_SERVER, options=options)
        driver.implicitly_wait(10)
        
        print("Mobile driver initialized successfully")
        take_screenshot(driver, "1-1_driver_initialized", report_dir)
        
        return driver
        
    except Exception as e:
        print(f"Failed to initialize driver: {str(e)}")
        raise

def test_email_login_flow(driver, report_dir):
    """Test case for email-based login with verification code"""
    try:
        print("\n=== Starting Email Login Flow Test ===")
        
        # Wait for app to load completely
        print("Waiting for app to load completely...")
        wait_for_app_load(driver, WebDriverWait(driver, 20))
        take_screenshot(driver, "1-2_app_loaded", report_dir)
        
        # Step 1: Enter email
        try:
            print("\n--- Step 1: Entering Email Address ---")
            
            # Try multiple locator strategies for email field
            locators = LocatorStrategy.get_input_field_locators(Config.Locators.EMAIL_FIELD, 0)
            email_field = None
            
            for by, locator in locators:
                try:
                    print(f"Trying to find email field using {by}...")
                    email_field = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((by, locator))
                    )
                    print(f"Found email field using {by}")
                    break
                except TimeoutException:
                    continue
            
            if not email_field:
                raise Exception("Could not find email field with any locator strategy")
            
            # Step 1a: Click on email field and delete existing content
            try:
                print("Clicking on email field to focus it...")
                email_field.click()
                time.sleep(1)
                
                print("Deleting existing email content...")
                # Try multiple deletion strategies focused on select all + delete
                deletion_strategies = [
                    # Strategy 1: Double click to select all, then delete
                    lambda: (email_field.click(), time.sleep(0.5), email_field.click(), time.sleep(0.5), email_field.send_keys(Keys.DELETE)),
                    # Strategy 2: Long press to select all, then delete
                    lambda: ActionChains(driver).move_to_element(email_field).click_and_hold().pause(2).release().pause(1).send_keys(Keys.DELETE).perform(),
                    # Strategy 3: Use Android keycodes for select all and delete
                    lambda: (driver.press_keycode(123), time.sleep(0.5), driver.press_keycode(67), time.sleep(0.5), driver.press_keycode(112)),
                    # Strategy 4: Clear method
                    lambda: email_field.clear(),
                    # Strategy 5: ActionChains with keyboard shortcuts
                    lambda: ActionChains(driver).move_to_element(email_field).click().pause(1).send_keys(Keys.CONTROL + "a").pause(1).send_keys(Keys.DELETE).perform(),
                    # Strategy 6: Direct keyboard shortcuts
                    lambda: email_field.send_keys(Keys.CONTROL + "a" + Keys.DELETE),
                ]
                
                content_deleted = False
                for i, strategy in enumerate(deletion_strategies):
                    try:
                        print(f"Trying deletion strategy {i+1}...")
                        strategy()
                        time.sleep(1)
                        content_deleted = True
                        print("Email field content deleted successfully")
                        break
                    except Exception as e:
                        print(f"Deletion strategy {i+1} failed: {str(e)}")
                        continue
                
                if not content_deleted:
                    print("Warning: Could not delete email field content, proceeding anyway")
                
                # Click back to ensure field is focused
                print("Clicking back on email field to ensure focus...")
                email_field.click()
                time.sleep(1)
                
            except Exception as e:
                print(f"Could not delete email field content: {str(e)}")
            
            # Clear the field first to ensure clean input
            try:
                print("Clearing email field first...")
                email_field.clear()
                time.sleep(1)
            except Exception as e:
                print(f"Could not clear email field: {str(e)}")
            
            # Try multiple input strategies
            input_strategies = [
                lambda: email_field.send_keys(Config.TEST_EMAIL),
                lambda: ActionChains(driver).move_to_element(email_field).click().pause(1).send_keys(Config.TEST_EMAIL).perform(),
                lambda: email_field.send_keys(Config.TEST_EMAIL)
            ]
            
            email_entered = False
            for i, strategy in enumerate(input_strategies):
                try:
                    print(f"Trying email input strategy {i+1}...")
                    strategy()
                    email_entered = True
                    print("Email entered successfully")
                    break
                except Exception as e:
                    print(f"Email input strategy {i+1} failed: {str(e)}")
                    continue
            
            if not email_entered:
                raise Exception("Failed to enter email with any input strategy")
            
            take_screenshot(driver, "1-3_email_entered", report_dir)
            
        except Exception as e:
            print(f"ERROR: Failed to enter email: {str(e)}")
            take_screenshot(driver, "error_email_entry", report_dir)
            raise
        
        # Step 2: Enter verification code
        try:
            print("\n--- Step 2: Entering Verification Code ---")
            
            # Try multiple locator strategies for verification code field
            locators = LocatorStrategy.get_input_field_locators(Config.Locators.VERIFICATION_CODE_FIELD, 1)
            code_field = None
            
            for by, locator in locators:
                try:
                    print(f"Trying to find verification code field using {by}...")
                    code_field = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((by, locator))
                    )
                    print(f"Found verification code field using {by}")
                    break
                except TimeoutException:
                    continue
            
            if not code_field:
                raise Exception("Could not find verification code field with any locator strategy")
            
            # Log field attributes for debugging
            print(f"Verification code field attributes:")
            print(f"  Enabled: {code_field.is_enabled()}")
            print(f"  Displayed: {code_field.is_displayed()}")
            print(f"  Location: {code_field.location}")
            print(f"  Size: {code_field.size}")
            
            # Try multiple input strategies
            code_entered = False
            for i, strategy in enumerate(input_strategies):
                try:
                    print(f"Trying verification code input strategy {i+1}...")
                    if i == 2:  # Clear and send strategy
                        code_field.clear()
                        time.sleep(1)
                        code_field.send_keys(Config.TEST_VERIFICATION_CODE)
                    else:
                        # Adapt strategy for verification code
                        if i == 0:
                            code_field.send_keys(Config.TEST_VERIFICATION_CODE)
                        else:
                            ActionChains(driver).move_to_element(code_field).click().pause(1).send_keys(Config.TEST_VERIFICATION_CODE).perform()
                    
                    code_entered = True
                    print("Verification code entered successfully")
                    break
                except Exception as e:
                    print(f"Verification code input strategy {i+1} failed: {str(e)}")
                    continue
            
            if not code_entered:
                raise Exception("Failed to enter verification code with any input strategy")
            
            # Hide keyboard after entering code
            print("Hiding keyboard after entering verification code...")
            try:
                driver.hide_keyboard()
                print("Keyboard hidden successfully")
            except Exception as e:
                print(f"Could not hide keyboard: {str(e)}")
            
            time.sleep(1)  # Let the UI settle
            take_screenshot(driver, "1-4_verification_code_entered", report_dir)
            
        except Exception as e:
            print(f"ERROR: Failed to enter verification code: {str(e)}")
            take_screenshot(driver, "error_verification_code", report_dir)
            raise
        
        # Step 3: Accept terms and conditions
        try:
            print("\n--- Step 3: Accepting Terms and Conditions ---")
            
            # Hide keyboard before handling checkbox
            print("Ensuring keyboard is hidden before checkbox interaction...")
            try:
                driver.hide_keyboard()
                print("Keyboard hidden successfully")
            except Exception:
                print("No keyboard to hide or hide failed")
            time.sleep(1)  # Let the UI settle
            
            # Try multiple locator strategies for checkbox
            locators = LocatorStrategy.get_checkbox_locators(Config.Locators.TERMS_CHECKBOX)
            checkbox = None
            
            max_attempts = 3
            for attempt in range(max_attempts):
                print(f"Terms acceptance attempt {attempt + 1}/{max_attempts}")
                
                for by, locator in locators:
                    try:
                        print(f"Trying to find checkbox using {by}...")
                        checkbox = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((by, locator))
                        )
                        print(f"Found checkbox using {by}")
                        break
                    except TimeoutException:
                        continue
                
                if checkbox:
                    # Log checkbox attributes
                    print(f"Checkbox attributes:")
                    print(f"  Enabled: {checkbox.is_enabled()}")
                    print(f"  Displayed: {checkbox.is_displayed()}")
                    print(f"  Location: {checkbox.location}")
                    print(f"  Size: {checkbox.size}")
                    
                    # Try to click the checkbox
                    try:
                        print("Clicking checkbox...")
                        checkbox.click()
                        print("Checkbox clicked successfully")
                        break
                    except Exception as e:
                        print(f"Checkbox click failed: {str(e)}")
                        if attempt < max_attempts - 1:
                            time.sleep(2)
                            continue
                        else:
                            raise
                else:
                    if attempt < max_attempts - 1:
                        print("Checkbox not found, retrying...")
                        time.sleep(2)
                        continue
                    else:
                        raise Exception("Could not find checkbox with any locator strategy")
            
            take_screenshot(driver, "1-5_terms_accepted", report_dir)
            
        except Exception as e:
            print(f"ERROR: Failed to accept terms: {str(e)}")
            take_screenshot(driver, "error_terms_acceptance", report_dir)
            raise
        
        # Step 4: Click login button
        try:
            print("\n--- Step 4: Clicking Login Button ---")
            
            # Try multiple locator strategies for login button
            locators = LocatorStrategy.get_button_locators(Config.Locators.LOGIN_BUTTON)
            login_button = None
            
            for by, locator in locators:
                try:
                    print(f"Trying to find login button using {by}...")
                    login_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((by, locator))
                    )
                    print(f"Found login button using {by}")
                    break
                except TimeoutException:
                    continue
            
            if not login_button:
                raise Exception("Could not find login button with any locator strategy")
            
            # Log login button attributes
            print(f"Login button attributes:")
            print(f"  Enabled: {login_button.is_enabled()}")
            print(f"  Displayed: {login_button.is_displayed()}")
            print(f"  Location: {login_button.location}")
            print(f"  Size: {login_button.size}")
            
            # Click the login button
            print("Clicking login button...")
            login_button.click()
            print("Login button clicked successfully")
            time.sleep(1)  # Let the UI settle
            
            take_screenshot(driver, "1-6_login_button_clicked", report_dir)
            
        except Exception as e:
            print(f"ERROR: Failed to click login button: {str(e)}")
            take_screenshot(driver, "error_login_button", report_dir)
            raise
        
        # Step 5: Verify login success
        try:
            print("\n--- Step 5: Verifying Login Success ---")
            
            # Wait for PROFILE ICON to appear
            print("Waiting for PROFILE ICON to appear...")
            PROFILE_ICON = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((AppiumBy.XPATH, Config.Locators.PROFILE_ICON))
            )
            
            # Verify the PROFILE ICON is displayed
            time.sleep(5)  # Wait 5 seconds after profile icon verification
            if PROFILE_ICON.is_displayed():
                print("PROFILE ICON found and displayed - Login successful!")
                take_screenshot(driver, "1-7_login_success", report_dir)
                return True
            else:
                raise Exception("PROFILE ICON found but not displayed")
            
        except TimeoutException:
            print("ERROR: PROFILE ICON not found - Login may have failed")
            take_screenshot(driver, "error_login_verification", report_dir)
            return False
        except Exception as e:
            print(f"ERROR: Failed to verify login success: {str(e)}")
            take_screenshot(driver, "error_login_verification", report_dir)
            return False
        
    except Exception as e:
        print(f"\n=== Login test failed with error: {str(e)} ===")
        take_screenshot(driver, "final_login_error", report_dir)
        raise

# ===== Main Test Function =====
def run_zoomcat_login_tests():
    """Main function to run all ZoomCat login tests"""
    report_dir = create_report_dir("Login via Verification Code test")
    print(f"\n=== Running ZoomCat Mobile Login Tests with report directory: {report_dir} ===")
    
    # Track test results
    test_results = {
        "email_login_flow": "NOT_RUN"
    }
    
    driver = None
    
    try:
        # Initialize mobile driver
        print("\n" + "="*60)
        print("INITIALIZING MOBILE DRIVER")
        print("="*60)
        driver = initialize_mobile_driver(report_dir)
        
        # Test: Email login flow
        print("\n" + "="*60)
        print("TEST: EMAIL LOGIN FLOW")
        print("="*60)
        try:
            result = test_email_login_flow(driver, report_dir)
            test_results["email_login_flow"] = "PASSED" if result else "FAILED"
            print(f"✓ Email Login Flow test completed: {test_results['email_login_flow']}")
        except Exception as e:
            test_results["email_login_flow"] = "FAILED"
            print(f"✗ Email Login Flow test failed with error: {str(e)}")
            take_screenshot(driver, "test_email_login_final_error", report_dir)
        
        # Print final test summary
        print("\n" + "="*60)
        print("FINAL TEST SUMMARY - ZOOMCAT MOBILE LOGIN")
        print("="*60)
        passed_count = sum(1 for result in test_results.values() if result == "PASSED")
        failed_count = sum(1 for result in test_results.values() if result == "FAILED")
        
        for test_name, result in test_results.items():
            status_icon = "✓" if result == "PASSED" else "✗" if result == "FAILED" else "⚠"
            print(f"{status_icon} {test_name.replace('_', ' ').title()}: {result}")
        
        print(f"\nOverall Results:")
        print(f"  Passed: {passed_count}")
        print(f"  Failed: {failed_count}")
        print(f"  Total: {len(test_results)}")
        print(f"\nTest reports saved in: {report_dir}")
        
        return test_results
        
    except Exception as e:
        print(f"\n=== Critical error during test execution: {str(e)} ===")
        if driver:
            take_screenshot(driver, "critical_error", report_dir)
        raise
        
    finally:
        if driver:
            print("\n=== Cleaning up and closing mobile driver ===")
            driver.quit()

# ===== Pytest Integration =====
class TestZoomCatLogin:
    """Test class with pytest integration"""
    
    @pytest.fixture(scope="function")
    def setup_test_environment(self):
        """Setup test environment and reporting"""
        report_dir = create_report_dir("Login via Verification Code test")
        print(f"Test environment setup - Report directory: {report_dir}")
        return report_dir
    
    def test_email_login_flow_pytest(self, setup_test_environment):
        """Pytest wrapper for email login flow test"""
        report_dir = setup_test_environment
        driver = None
        
        try:
            # Initialize driver
            driver = initialize_mobile_driver(report_dir)
            
            # Run the login test
            result = test_email_login_flow(driver, report_dir)
            
            # Assert the result
            assert result == True, "Email login flow test failed"
            print("✅ Pytest Email Login Flow test completed successfully")
            
        except Exception as e:
            print(f"❌ Pytest Email Login Flow test failed: {e}")
            if driver:
                take_screenshot(driver, "pytest_final_error", report_dir)
            raise
            
        finally:
            if driver:
                driver.quit()

# ===== Script Execution =====
if __name__ == "__main__":
    """Run tests when script is executed directly"""
    try:
        results = run_zoomcat_login_tests()
        
        # Exit with appropriate code
        failed_tests = sum(1 for result in results.values() if result == "FAILED")
        exit_code = 0 if failed_tests == 0 else 1
        
        print(f"\n=== Script execution completed with exit code: {exit_code} ===")
        exit(exit_code)
        
    except KeyboardInterrupt:
        print("\n=== Test execution interrupted by user ===")
        exit(130)
    except Exception as e:
        print(f"\n=== Script execution failed with error: {str(e)} ===")
        exit(1) 
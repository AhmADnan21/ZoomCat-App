"""
Appium Test Automation for Mobile Login System - ZoomCat App (Password Login)
This script automates the process of:
1. Mobile app initialization and connection
2. Password login method selection
3. Email and password input
4. Login validation and verification
5. Logout flow execution
6. Comprehensive reporting and screenshot capture
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
    TEST_PASSWORD = "Xiaoxi3321"

    # Element Locators
    class Locators:
        # Password Login Flow Locators
        PASSWORD_BUTTON = "//android.view.View[@content-desc=\"Password\"]"
        EMAIL_FIELD = "//android.widget.ScrollView/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]"
        PASSWORD_FIELD = "//android.widget.ScrollView/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]"
        TERMS_CHECKBOX = "//android.widget.ScrollView/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[3]/android.widget.FrameLayout[1]/android.widget.FrameLayout"
        LOGIN_BUTTON = "//android.widget.ScrollView/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.widget.FrameLayout"
        PROFILE_ICON = "//android.widget.ScrollView/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ImageView"
        
        # Logout Flow Locators (reused from Logout_Test.py)
        MY_ACCOUNT_SECTION = "//android.view.View[@content-desc=\"My account\"]"
        LOGOUT_BUTTON = "//android.view.View[@content-desc=\"Log out\"]"
        CONFIRMATION_POPUP = "//android.widget.FrameLayout[@resource-id=\"android:id/content\"]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[2]/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout"
        CONFIRM_BUTTON = "//android.view.View[@content-desc=\"Confirm\"]"
        LOGIN_PAGE_VERIFICATION = "(//android.view.View[@content-desc=\"Log in\"])[1]"

# ===== Utility Functions =====
def create_report_dir(test_name="Login by Password test"):
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
    def get_button_locators(button_xpath: str) -> List[Tuple[str, str]]:
        """Get multiple locator strategies for buttons"""
        return [
            (By.XPATH, button_xpath),
            (MobileBy.CLASS_NAME, "android.widget.Button"),
            (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View")')
        ]
    
    @staticmethod
    def get_input_field_locators(field_xpath: str, instance: int = 0) -> List[Tuple[str, str]]:
        """Get multiple locator strategies for input fields"""
        return [
            (By.XPATH, field_xpath),
            (MobileBy.CLASS_NAME, "android.widget.EditText"),
            (MobileBy.ANDROID_UIAUTOMATOR, f'new UiSelector().className("android.widget.EditText").instance({instance})')
        ]
    
    @staticmethod
    def get_image_view_locators(image_xpath: str) -> List[Tuple[str, str]]:
        """Get multiple locator strategies for image views (profile icon)"""
        return [
            (By.XPATH, image_xpath),
            (MobileBy.CLASS_NAME, "android.widget.ImageView"),
            (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView")')
        ]
    
    @staticmethod
    def get_section_locators(section_xpath: str) -> List[Tuple[str, str]]:
        """Get multiple locator strategies for sections"""
        return [
            (By.XPATH, section_xpath),
            (MobileBy.CLASS_NAME, "android.widget.FrameLayout")
        ]
    
    @staticmethod
    def get_popup_locators(popup_xpath: str) -> List[Tuple[str, str]]:
        """Get multiple locator strategies for popups"""
        return [
            (By.XPATH, popup_xpath),
            (MobileBy.CLASS_NAME, "android.widget.FrameLayout")
        ]
    
    @staticmethod
    def get_checkbox_locators(checkbox_xpath: str) -> List[Tuple[str, str]]:
        """Get multiple locator strategies for checkboxes"""
        return [
            (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.CheckBox").instance(0)'),
            (By.XPATH, checkbox_xpath),
            (MobileBy.CLASS_NAME, "android.widget.CheckBox")
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

def test_password_login_flow(driver, report_dir):
    """Test case for password-based login flow"""
    try:
        print("\n=== Starting Password Login Flow Test ===")
        
        # Wait for app to load completely
        print("Waiting for app to load completely...")
        wait_for_app_load(driver, WebDriverWait(driver, 20))
        take_screenshot(driver, "1-2_app_loaded", report_dir)
        
        # Step 1: Click on the "Password" button
        try:
            print("\n--- Step 1: Clicking Password Button ---")
            
            # Try multiple locator strategies for password button
            locators = LocatorStrategy.get_button_locators(Config.Locators.PASSWORD_BUTTON)
            password_button = None
            
            for by, locator in locators:
                try:
                    print(f"Trying to find password button using {by}...")
                    password_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((by, locator))
                    )
                    print(f"Found password button using {by}")
                    break
                except TimeoutException:
                    continue
            
            if not password_button:
                raise Exception("Could not find password button with any locator strategy")
            
            # Log password button attributes
            print(f"Password button attributes:")
            print(f"  Enabled: {password_button.is_enabled()}")
            print(f"  Displayed: {password_button.is_displayed()}")
            print(f"  Location: {password_button.location}")
            print(f"  Size: {password_button.size}")
            
            # Click the password button
            print("Clicking password button...")
            password_button.click()
            print("Password button clicked successfully")
            time.sleep(2)  # Wait for password login screen to load
            
            take_screenshot(driver, "1-3_password_button_clicked", report_dir)
            
        except Exception as e:
            print(f"ERROR: Failed to click password button: {str(e)}")
            take_screenshot(driver, "error_password_button", report_dir)
            raise
        
        # Step 2: Wait for the password login screen to fully load
        try:
            print("\n--- Step 2: Waiting for Password Login Screen to Load ---")
            print("Waiting for password login screen to fully load...")
            time.sleep(3)  # Wait for screen transition
            take_screenshot(driver, "1-4_password_screen_loaded", report_dir)
            
        except Exception as e:
            print(f"ERROR: Failed to wait for password screen: {str(e)}")
            take_screenshot(driver, "error_password_screen", report_dir)
            raise
        
        # Step 3: Enter email
        try:
            print("\n--- Step 3: Entering Email Address ---")
            
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
            
            # Step 3a: Click on email field and delete existing content
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
            
            take_screenshot(driver, "1-5_email_entered", report_dir)
            
        except Exception as e:
            print(f"ERROR: Failed to enter email: {str(e)}")
            take_screenshot(driver, "error_email_entry", report_dir)
            raise
        
        # Step 4: Enter password
        try:
            print("\n--- Step 4: Entering Password ---")
            
            # Try multiple locator strategies for password field
            locators = LocatorStrategy.get_input_field_locators(Config.Locators.PASSWORD_FIELD, 1)
            password_field = None
            
            for by, locator in locators:
                try:
                    print(f"Trying to find password field using {by}...")
                    password_field = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((by, locator))
                    )
                    print(f"Found password field using {by}")
                    break
                except TimeoutException:
                    continue
            
            if not password_field:
                raise Exception("Could not find password field with any locator strategy")
            
            # Log field attributes for debugging
            print(f"Password field attributes:")
            print(f"  Enabled: {password_field.is_enabled()}")
            print(f"  Displayed: {password_field.is_displayed()}")
            print(f"  Location: {password_field.location}")
            print(f"  Size: {password_field.size}")
            
            # Try multiple input strategies
            password_entered = False
            for i, strategy in enumerate(input_strategies):
                try:
                    print(f"Trying password input strategy {i+1}...")
                    if i == 2:  # Clear and send strategy
                        password_field.clear()
                        time.sleep(1)
                        password_field.send_keys(Config.TEST_PASSWORD)
                    else:
                        # Adapt strategy for password
                        if i == 0:
                            password_field.send_keys(Config.TEST_PASSWORD)
                        else:
                            ActionChains(driver).move_to_element(password_field).click().pause(1).send_keys(Config.TEST_PASSWORD).perform()
                    
                    password_entered = True
                    print("Password entered successfully")
                    break
                except Exception as e:
                    print(f"Password input strategy {i+1} failed: {str(e)}")
                    continue
            
            if not password_entered:
                raise Exception("Failed to enter password with any input strategy")
            
            # Hide keyboard after entering password
            print("Hiding keyboard after entering password...")
            try:
                driver.hide_keyboard()
                print("Keyboard hidden successfully")
            except Exception as e:
                print(f"Could not hide keyboard: {str(e)}")
            
            time.sleep(1)  # Let the UI settle
            take_screenshot(driver, "1-6_password_entered", report_dir)
            
        except Exception as e:
            print(f"ERROR: Failed to enter password: {str(e)}")
            take_screenshot(driver, "error_password_entry", report_dir)
            raise
        
        # Step 5: Accept terms and conditions
        try:
            print("\n--- Step 5: Accepting Terms and Conditions ---")
            
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
            
            take_screenshot(driver, "1-7_terms_accepted", report_dir)
            
        except Exception as e:
            print(f"ERROR: Failed to accept terms: {str(e)}")
            take_screenshot(driver, "error_terms_acceptance", report_dir)
            raise
        
        # Step 6: Click login button
        try:
            print("\n--- Step 6: Clicking Login Button ---")
            
            # Try multiple locator strategies for login button
            locators = LocatorStrategy.get_button_locators(Config.Locators.LOGIN_BUTTON)
            login_button = None
            
            for by, locator in locators:
                try:
                    print(f"Trying to find login button using {by}...")
                    login_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((by, locator))
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
            time.sleep(2)  # Let the UI settle
            
            take_screenshot(driver, "1-8_login_button_clicked", report_dir)
            
        except Exception as e:
            print(f"ERROR: Failed to click login button: {str(e)}")
            take_screenshot(driver, "error_login_button", report_dir)
            raise
        
        # Step 7: Verify login success
        try:
            print("\n--- Step 7: Verifying Login Success ---")
            
            # Wait for PROFILE ICON to appear
            print("Waiting for PROFILE ICON to appear...")
            PROFILE_ICON = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((AppiumBy.XPATH, Config.Locators.PROFILE_ICON))
            )
            
            # Verify the PROFILE ICON is displayed
            time.sleep(5)  # Wait 5 seconds after profile icon verification
            if PROFILE_ICON.is_displayed():
                print("PROFILE ICON found and displayed - Login successful!")
                take_screenshot(driver, "1-9_login_success", report_dir)
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
        print(f"\n=== Password login test failed with error: {str(e)} ===")
        take_screenshot(driver, "final_password_login_error", report_dir)
        raise

def test_logout_flow(driver, report_dir):
    """Test case for logout flow (reused from Logout_Test.py)"""
    try:
        print("\n=== Starting Logout Flow Test ===")
        
        # Step 1: Click on the profile icon
        try:
            print("\n--- Step 1: Clicking Profile Icon ---")
            
            # Try multiple locator strategies for profile icon
            locators = LocatorStrategy.get_image_view_locators(Config.Locators.PROFILE_ICON)
            profile_icon = None
            
            for by, locator in locators:
                try:
                    print(f"Trying to find profile icon using {by}...")
                    profile_icon = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((by, locator))
                    )
                    print(f"Found profile icon using {by}")
                    break
                except TimeoutException:
                    continue
            
            if not profile_icon:
                raise Exception("Could not find profile icon with any locator strategy")
            
            # Log profile icon attributes
            print(f"Profile icon attributes:")
            print(f"  Enabled: {profile_icon.is_enabled()}")
            print(f"  Displayed: {profile_icon.is_displayed()}")
            print(f"  Location: {profile_icon.location}")
            print(f"  Size: {profile_icon.size}")
            
            # Click the profile icon
            print("Clicking profile icon...")
            profile_icon.click()
            print("Profile icon clicked successfully")
            time.sleep(2)  # Wait for navigation
            
            take_screenshot(driver, "2-1_profile_icon_clicked", report_dir)
            
        except Exception as e:
            print(f"ERROR: Failed to click profile icon: {str(e)}")
            take_screenshot(driver, "error_profile_icon", report_dir)
            raise
        
        # Step 2: Wait until "My account" appears and click on it
        try:
            print("\n--- Step 2: Accessing My Account Section ---")
            
            # Wait for "My account" section to appear
            print("Waiting for 'My account' section to appear...")
            my_account_section = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, Config.Locators.MY_ACCOUNT_SECTION))
            )
            
            # Log my account section attributes
            print(f"My account section attributes:")
            print(f"  Enabled: {my_account_section.is_enabled()}")
            print(f"  Displayed: {my_account_section.is_displayed()}")
            print(f"  Location: {my_account_section.location}")
            print(f"  Size: {my_account_section.size}")
            
            # Click on My account
            print("Clicking on My account...")
            my_account_section.click()
            print("My account clicked successfully")
            time.sleep(2)  # Wait for navigation
            
            take_screenshot(driver, "2-2_my_account_clicked", report_dir)
            
        except TimeoutException:
            print("ERROR: My account section not found within timeout")
            take_screenshot(driver, "error_my_account_not_found", report_dir)
            raise
        except Exception as e:
            print(f"ERROR: Failed to access My account: {str(e)}")
            take_screenshot(driver, "error_my_account", report_dir)
            raise
        
        # Step 3: Click on the logout button
        try:
            print("\n--- Step 3: Clicking Logout Button ---")
            
            # Try multiple locator strategies for logout button
            locators = LocatorStrategy.get_button_locators(Config.Locators.LOGOUT_BUTTON)
            logout_button = None
            
            for by, locator in locators:
                try:
                    print(f"Trying to find logout button using {by}...")
                    logout_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((by, locator))
                    )
                    print(f"Found logout button using {by}")
                    break
                except TimeoutException:
                    continue
            
            if not logout_button:
                raise Exception("Could not find logout button with any locator strategy")
            
            # Log logout button attributes
            print(f"Logout button attributes:")
            print(f"  Enabled: {logout_button.is_enabled()}")
            print(f"  Displayed: {logout_button.is_displayed()}")
            print(f"  Location: {logout_button.location}")
            print(f"  Size: {logout_button.size}")
            
            # Click the logout button
            print("Clicking logout button...")
            logout_button.click()
            print("Logout button clicked successfully")
            time.sleep(2)  # Wait for popup to appear
            
            take_screenshot(driver, "2-3_logout_button_clicked", report_dir)
            
        except Exception as e:
            print(f"ERROR: Failed to click logout button: {str(e)}")
            take_screenshot(driver, "error_logout_button", report_dir)
            raise
        
        # Step 4: Wait for confirmation popup and click Confirm
        try:
            print("\n--- Step 4: Handling Confirmation Popup ---")
            
            # Wait for confirmation popup to appear
            print("Waiting for confirmation popup to appear...")
            confirmation_popup = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, Config.Locators.CONFIRMATION_POPUP))
            )
            
            # Log popup attributes
            print(f"Confirmation popup attributes:")
            print(f"  Enabled: {confirmation_popup.is_enabled()}")
            print(f"  Displayed: {confirmation_popup.is_displayed()}")
            print(f"  Location: {confirmation_popup.location}")
            print(f"  Size: {confirmation_popup.size}")
            
            # Click on Confirm button
            print("Clicking Confirm button...")
            confirm_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, Config.Locators.CONFIRM_BUTTON))
            )
            
            confirm_button.click()
            print("Confirm button clicked successfully")
            time.sleep(2)  # Wait for logout process
            
            take_screenshot(driver, "2-4_confirmation_popup_handled", report_dir)
            
        except TimeoutException:
            print("ERROR: Confirmation popup not found within timeout")
            take_screenshot(driver, "error_confirmation_popup", report_dir)
            raise
        except Exception as e:
            print(f"ERROR: Failed to handle confirmation popup: {str(e)}")
            take_screenshot(driver, "error_confirmation_popup", report_dir)
            raise
        
        # Step 5: Verify redirection to Login page
        try:
            print("\n--- Step 5: Verifying Login Page Redirection ---")
            
            # Wait for login page to appear
            print("Waiting for login page to appear...")
            login_page_element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, Config.Locators.LOGIN_PAGE_VERIFICATION))
            )
            
            # Verify the login page element is displayed
            if login_page_element.is_displayed():
                print("Login page element found and displayed - Logout successful!")
                
                # Add short wait after redirection as requested
                print("Waiting 2 seconds after redirection...")
                time.sleep(2)
                
                take_screenshot(driver, "2-5_logout_success", report_dir)
                return True
            else:
                raise Exception("Login page element found but not displayed")
            
        except TimeoutException:
            print("ERROR: Login page not found - Logout may have failed")
            take_screenshot(driver, "error_login_page_verification", report_dir)
            return False
        except Exception as e:
            print(f"ERROR: Failed to verify login page redirection: {str(e)}")
            take_screenshot(driver, "error_login_page_verification", report_dir)
            return False
        
    except Exception as e:
        print(f"\n=== Logout test failed with error: {str(e)} ===")
        take_screenshot(driver, "final_logout_error", report_dir)
        raise

# ===== Main Test Function =====
def run_zoomcat_password_login_tests():
    """Main function to run all ZoomCat password login tests"""
    report_dir = create_report_dir("Login by Password test")
    print(f"\n=== Running ZoomCat Mobile Password Login Tests with report directory: {report_dir} ===")
    
    # Track test results
    test_results = {
        "password_login_flow": "NOT_RUN",
        "logout_flow": "NOT_RUN"
    }
    
    driver = None
    
    try:
        # Initialize mobile driver
        print("\n" + "="*60)
        print("INITIALIZING MOBILE DRIVER")
        print("="*60)
        driver = initialize_mobile_driver(report_dir)
        
        # Test: Password login flow
        print("\n" + "="*60)
        print("TEST: PASSWORD LOGIN FLOW")
        print("="*60)
        try:
            result = test_password_login_flow(driver, report_dir)
            test_results["password_login_flow"] = "PASSED" if result else "FAILED"
            print(f"✓ Password Login Flow test completed: {test_results['password_login_flow']}")
        except Exception as e:
            test_results["password_login_flow"] = "FAILED"
            print(f"✗ Password Login Flow test failed with error: {str(e)}")
            take_screenshot(driver, "test_password_login_final_error", report_dir)
        
        # Test: Logout flow
        print("\n" + "="*60)
        print("TEST: LOGOUT FLOW")
        print("="*60)
        try:
            result = test_logout_flow(driver, report_dir)
            test_results["logout_flow"] = "PASSED" if result else "FAILED"
            print(f"✓ Logout Flow test completed: {test_results['logout_flow']}")
        except Exception as e:
            test_results["logout_flow"] = "FAILED"
            print(f"✗ Logout Flow test failed with error: {str(e)}")
            take_screenshot(driver, "test_logout_final_error", report_dir)
        
        # Print final test summary
        print("\n" + "="*60)
        print("FINAL TEST SUMMARY - ZOOMCAT MOBILE PASSWORD LOGIN")
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
class TestZoomCatPasswordLogin:
    """Test class with pytest integration"""
    
    @pytest.fixture(scope="function")
    def setup_test_environment(self):
        """Setup test environment and reporting"""
        report_dir = create_report_dir("Login by Password test")
        print(f"Test environment setup - Report directory: {report_dir}")
        return report_dir
    
    def test_password_login_flow_pytest(self, setup_test_environment):
        """Pytest wrapper for password login flow test"""
        report_dir = setup_test_environment
        driver = None
        
        try:
            # Initialize driver
            driver = initialize_mobile_driver(report_dir)
            
            # Run the password login test
            result = test_password_login_flow(driver, report_dir)
            
            # Assert the result
            assert result == True, "Password login flow test failed"
            print("✅ Pytest Password Login Flow test completed successfully")
            
        except Exception as e:
            print(f"❌ Pytest Password Login Flow test failed: {e}")
            if driver:
                take_screenshot(driver, "pytest_final_error", report_dir)
            raise
            
        finally:
            if driver:
                driver.quit()
    
    def test_logout_flow_pytest(self, setup_test_environment):
        """Pytest wrapper for logout flow test"""
        report_dir = setup_test_environment
        driver = None
        
        try:
            # Initialize driver
            driver = initialize_mobile_driver(report_dir)
            
            # First login, then logout
            login_result = test_password_login_flow(driver, report_dir)
            assert login_result == True, "Login failed before logout test"
            
            # Run the logout test
            result = test_logout_flow(driver, report_dir)
            
            # Assert the result
            assert result == True, "Logout flow test failed"
            print("✅ Pytest Logout Flow test completed successfully")
            
        except Exception as e:
            print(f"❌ Pytest Logout Flow test failed: {e}")
            if driver:
                take_screenshot(driver, "pytest_logout_final_error", report_dir)
            raise
            
        finally:
            if driver:
                driver.quit()

# ===== Script Execution =====
if __name__ == "__main__":
    """Run tests when script is executed directly"""
    try:
        results = run_zoomcat_password_login_tests()
        
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
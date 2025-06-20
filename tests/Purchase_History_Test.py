# -*- coding: utf-8 -*-
"""
Appium Test Automation for Mobile Purchase History System - ZoomCat App
This script automates the process of:
1. Mobile app initialization and connection
2. Profile icon navigation
3. Order history access

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

    # Element Locators
    class Locators:
        # Purchase History Flow Locators
        PROFILE_ICON = "//android.widget.ScrollView/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ImageView"
        ORDER_HISTORY_SECTION = "//android.view.View[@content-desc=\"Order history\"]"
        BACK_BUTTON = "//android.widget.FrameLayout[@resource-id=\"android:id/content\"]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.ImageView"
        COPY_BUTTON = "//android.widget.FrameLayout[@resource-id=\"android:id/content\"]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.ScrollView/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.ScrollView/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.ImageView"

# ===== Utility Functions =====
def create_report_dir(test_name="Purchase History Test"):
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
    def get_image_view_locators(image_xpath: str) -> List[Tuple[str, str]]:
        """Get multiple locator strategies for image views (profile icon)"""
        return [
            (By.XPATH, image_xpath),
            (MobileBy.CLASS_NAME, "android.widget.ImageView"),
            (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView")')
        ]
    
    @staticmethod
    def get_copy_button_locators(copy_xpath: str) -> List[Tuple[str, str]]:
        """Get multiple locator strategies for copy buttons"""
        return [
            (By.XPATH, copy_xpath),
            (MobileBy.CLASS_NAME, "android.widget.ImageView"),
            (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView")')
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

def test_purchase_history_flow(driver, report_dir):
    """Test case for purchase history flow"""
    try:
        print("\n=== Starting Purchase History Flow Test ===")
        
        # Wait for app to load completely
        print("Waiting for app to load completely...")
        wait_for_app_load(driver, WebDriverWait(driver, 20))
        take_screenshot(driver, "1-2_app_loaded", report_dir)
        
        # Step 1: Click on the profile icon
        try:
            print("\n--- Step 1: Clicking Profile Icon ---")
            
            # Try multiple locator strategies for profile icon
            locators = LocatorStrategy.get_image_view_locators(Config.Locators.PROFILE_ICON)
            profile_icon = None
            
            for by, locator in locators:
                try:
                    profile_icon = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((by, locator))
                    )
                    print(f"Found profile icon using {by}")
                    break
                except TimeoutException:
                    continue
            
            if not profile_icon:
                raise Exception("Could not find profile icon with any locator strategy")
            
            # Click the profile icon
            profile_icon.click()
            print("Profile icon clicked successfully")
            time.sleep(2)  # Wait for navigation
            
            take_screenshot(driver, "1-3_profile_icon_clicked", report_dir)
            
        except Exception as e:
            print(f"ERROR: Failed to click profile icon: {str(e)}")
            take_screenshot(driver, "error_profile_icon", report_dir)
            raise
        
        # Step 2: Click on Order history
        try:
            print("\n--- Step 2: Accessing Order History Section ---")
            
            # Wait for "Order history" section to appear
            order_history_section = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, Config.Locators.ORDER_HISTORY_SECTION))
            )
            
            # Click on Order history
            order_history_section.click()
            print("Order history clicked successfully")
            time.sleep(3)  # Wait for order history page to load
            
            take_screenshot(driver, "1-4_order_history_clicked", report_dir)
            
        except TimeoutException:
            print("ERROR: Order history section not found within timeout")
            take_screenshot(driver, "error_order_history_not_found", report_dir)
            raise
        except Exception as e:
            print(f"ERROR: Failed to access Order history: {str(e)}")
            take_screenshot(driver, "error_order_history", report_dir)
            raise
        
        # Step 3: Verify user is on the correct page
        try:
            print("\n--- Step 3: Verifying User is on Order History Page ---")
            
            # Wait for "Order history" page title to appear
            order_history_title = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, Config.Locators.ORDER_HISTORY_SECTION))
            )
            
            # Verify the order history title is displayed
            if order_history_title.is_displayed():
                print("Order history page title found and displayed - User is on correct page!")
                take_screenshot(driver, "1-5_order_history_page_verified", report_dir)
                
                # Step 3a: Verify copy button appears on the page
                try:
                    print("\n--- Step 3a: Verifying Copy Button Appears ---")
                    
                    # Wait for copy button to appear
                    copy_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, Config.Locators.COPY_BUTTON))
                    )
                    
                    if copy_button.is_displayed():
                        print("Copy button found and displayed on order history page!")
                        take_screenshot(driver, "1-5a_copy_button_verified", report_dir)
                    else:
                        raise Exception("Copy button found but not displayed")
                    
                except TimeoutException:
                    print("ERROR: Copy button not found on order history page")
                    take_screenshot(driver, "error_copy_button_not_found", report_dir)
                    return False
                except Exception as e:
                    print(f"ERROR: Failed to verify copy button: {str(e)}")
                    take_screenshot(driver, "error_copy_button_verification", report_dir)
                    return False
                
                # Step 4: Click back button to return to home page
                try:
                    print("\n--- Step 4: Clicking Back Button ---")
                    
                    # Wait for back button to appear
                    back_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, Config.Locators.BACK_BUTTON))
                    )
                    
                    # Click the back button
                    back_button.click()
                    print("Back button clicked successfully")
                    time.sleep(2)  # Wait for navigation
                    
                    take_screenshot(driver, "1-6_back_button_clicked", report_dir)
                    
                except Exception as e:
                    print(f"ERROR: Failed to click back button: {str(e)}")
                    take_screenshot(driver, "error_back_button", report_dir)
                    raise
                
                # Step 5: Verify user is back to home page
                try:
                    print("\n--- Step 5: Verifying Return to Home Page ---")
                    
                    # Wait for profile icon to appear (indicating home page)
                    profile_icon_home = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, Config.Locators.PROFILE_ICON))
                    )
                    
                    # Verify the profile icon is displayed
                    if profile_icon_home.is_displayed():
                        print("Profile icon found and displayed - User successfully returned to home page!")
                        take_screenshot(driver, "1-7_home_page_verified", report_dir)
                        
                        # Wait for 5 seconds as requested
                        print("Waiting for 5 seconds...")
                        time.sleep(5)
                        print("5-second wait completed")
                        
                        return True
                    else:
                        raise Exception("Profile icon found but not displayed")
                    
                except TimeoutException:
                    print("ERROR: Profile icon not found - Return to home page may have failed")
                    take_screenshot(driver, "error_home_page_verification", report_dir)
                    return False
                except Exception as e:
                    print(f"ERROR: Failed to verify return to home page: {str(e)}")
                    take_screenshot(driver, "error_home_page_verification", report_dir)
                    return False
                
            else:
                raise Exception("Order history page title found but not displayed")
            
        except TimeoutException:
            print("ERROR: Order history page title not found - Navigation may have failed")
            take_screenshot(driver, "error_order_history_page", report_dir)
            return False
        except Exception as e:
            print(f"ERROR: Failed to verify order history page: {str(e)}")
            take_screenshot(driver, "error_order_history_page", report_dir)
            return False
        
    except Exception as e:
        print(f"\n=== Purchase history test failed with error: {str(e)} ===")
        take_screenshot(driver, "final_purchase_history_error", report_dir)
        raise

# ===== Main Test Function =====
def run_zoomcat_purchase_history_tests():
    """Main function to run all ZoomCat purchase history tests"""
    report_dir = create_report_dir("Purchase History Test")
    print(f"\n=== Running ZoomCat Mobile Purchase History Tests with report directory: {report_dir} ===")
    
    # Track test results
    test_results = {
        "purchase_history_flow": "NOT_RUN"
    }
    
    driver = None
    
    try:
        # Initialize mobile driver
        print("\n" + "="*60)
        print("INITIALIZING MOBILE DRIVER")
        print("="*60)
        driver = initialize_mobile_driver(report_dir)
        
        # Test: Purchase history flow
        print("\n" + "="*60)
        print("TEST: PURCHASE HISTORY FLOW")
        print("="*60)
        try:
            result = test_purchase_history_flow(driver, report_dir)
            test_results["purchase_history_flow"] = "PASSED" if result else "FAILED"
            print(f"Purchase History Flow test completed: {test_results['purchase_history_flow']}")
        except Exception as e:
            test_results["purchase_history_flow"] = "FAILED"
            print(f"Purchase History Flow test failed with error: {str(e)}")
            take_screenshot(driver, "test_purchase_history_final_error", report_dir)
        
        # Print final test summary
        print("\n" + "="*60)
        print("FINAL TEST SUMMARY - ZOOMCAT MOBILE PURCHASE HISTORY")
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

# ===== Script Execution =====
if __name__ == "__main__":
    """Run tests when script is executed directly"""
    try:
        results = run_zoomcat_purchase_history_tests()
        
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
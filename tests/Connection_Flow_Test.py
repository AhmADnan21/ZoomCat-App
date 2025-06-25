# -*- coding: utf-8 -*-
"""
Appium Test Automation for Mobile Connection Flow System - ZoomCat App
This script automates the process of:
1. Mobile app initialization and connection
2. Connect functionality with timer verification
3. Disconnect functionality with button verification
4. IP switching with sticky IPs selection
5. Random IP selection with confirmation
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
        # Connection Flow Locators
        CONNECT_BUTTON = "//android.view.View[@content-desc=\"Connect\"]"
        CONNECTION_TIMER = "//android.view.View[@content-desc=\"00:00:06\"]"
        CONNECTION_TIMER_AFTER_IP_SWITCH = "//android.view.View[@content-desc=\"00:00:09\"]"
        DISCONNECT_BUTTON = "//android.widget.ScrollView/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]"
        
        # IP Switching Locators
        IP_LIST_SCROLL_VIEW = "//android.widget.ScrollView/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout[3]/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.ImageView"
        STICKY_IPS_TEXT = "(//android.view.View[@content-desc=\"Sticky IPs\"])[1]"
        AKTEST_116_SELECTION = "//android.widget.HorizontalScrollView/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout[4]/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ImageView"
        RANDOM_OPTION = "//android.widget.HorizontalScrollView/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout[4]/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.widget.FrameLayout"
        CONFIRMATION_POPUP = "//android.widget.FrameLayout[@resource-id=\"android:id/content\"]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[2]/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]"
        CONFIRM_BUTTON = "//android.view.View[@content-desc=\"Confirm\"]"

# ===== Utility Functions =====
def create_report_dir(test_name="Connection Flow Test"):
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

def test_connection_flow(driver, report_dir):
    """Test case for complete connection flow with IP switching"""
    try:
        print("\n=== Starting Connection Flow Test ===")
        
        # Wait for app to load completely
        print("Waiting for app to load completely...")
        wait_for_app_load(driver, WebDriverWait(driver, 20))
        take_screenshot(driver, "1-2_app_loaded", report_dir)
        
        # Step 1: Connect - Success Verification
        try:
            print("\n--- Step 1: Connect - Success Verification ---")
            
            # Click on the Connect button
            connect_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, Config.Locators.CONNECT_BUTTON))
            )
            connect_button.click()
            print("Connect button clicked successfully")
            
            # Verify the connection timer appears
            connection_timer = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, Config.Locators.CONNECTION_TIMER))
            )
            print("Connection timer appeared successfully")
            
            # Wait for 5 seconds
            print("Waiting for 5 seconds...")
            time.sleep(5)
            
            take_screenshot(driver, "1-3_connection_established", report_dir)
            
        except Exception as e:
            print(f"ERROR: Failed to establish connection: {str(e)}")
            take_screenshot(driver, "error_connection", report_dir)
            raise
        
        # Step 2: Switch to Different IP
        try:
            print("\n--- Step 2: Switch to Different IP ---")
            
            # Click on the Scroll View (IP list)
            ip_list_scroll = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, Config.Locators.IP_LIST_SCROLL_VIEW))
            )
            ip_list_scroll.click()
            print("IP list scroll view clicked successfully")
            
            # Wait until "Sticky IPs" text appears
            sticky_ips_text = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, Config.Locators.STICKY_IPS_TEXT))
            )
            print("Sticky IPs text appeared successfully")
            
            # Click on the Horizontal Scroll View to select akTest_+116
            aktest_116_selection = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, Config.Locators.AKTEST_116_SELECTION))
            )
            aktest_116_selection.click()
            print("akTest_+116 selection clicked successfully")
            
            # Wait for 3 seconds
            print("Waiting for 3 seconds...")
            time.sleep(3)
            
            # Select the Random option
            random_option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, Config.Locators.RANDOM_OPTION))
            )
            random_option.click()
            print("Random option selected successfully")
            
            # Wait for the confirmation popup
            confirmation_popup = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, Config.Locators.CONFIRMATION_POPUP))
            )
            print("Confirmation popup appeared")
            
            # Click Confirm
            confirm_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, Config.Locators.CONFIRM_BUTTON))
            )
            confirm_button.click()
            print("Confirm button clicked successfully")
            
            # Wait for 5 seconds
            print("Waiting for 5 seconds...")
            time.sleep(5)
            
            # Verify the connection timer appears again
            connection_timer_again = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, Config.Locators.CONNECTION_TIMER_AFTER_IP_SWITCH))
            )
            print("Connection timer appeared again - IP switch successful")
            
            # Wait another 5 seconds
            print("Waiting another 5 seconds...")
            time.sleep(5)
            
            take_screenshot(driver, "1-4_ip_switch_completed", report_dir)
            
        except Exception as e:
            print(f"ERROR: Failed to switch IP: {str(e)}")
            take_screenshot(driver, "error_ip_switch", report_dir)
            raise
        
        # Step 3: Disconnect - Final Check
        try:
            print("\n--- Step 3: Disconnect - Final Check ---")
            
            # Click the Disconnect button
            disconnect_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, Config.Locators.DISCONNECT_BUTTON))
            )
            disconnect_button.click()
            print("Disconnect button clicked successfully")
            
            # Wait for 5 seconds
            print("Waiting for 5 seconds...")
            time.sleep(5)
            
            # Verify the Connect button appears
            connect_button_final = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, Config.Locators.CONNECT_BUTTON))
            )
            print("Connect button appears - Final disconnection successful")
            
            # Wait for 5 seconds
            print("Waiting for 5 seconds...")
            time.sleep(5)
            
            take_screenshot(driver, "1-5_final_disconnection", report_dir)
            return True
            
        except Exception as e:
            print(f"ERROR: Failed final disconnection: {str(e)}")
            take_screenshot(driver, "error_final_disconnection", report_dir)
            raise
        
    except Exception as e:
        print(f"\n=== Connection flow test failed with error: {str(e)} ===")
        take_screenshot(driver, "final_connection_error", report_dir)
        raise

# ===== Main Test Function =====
def run_zoomcat_connection_flow_tests():
    """Main function to run all ZoomCat connection flow tests"""
    report_dir = create_report_dir("Connection Flow Test")
    print(f"\n=== Running ZoomCat Mobile Connection Flow Tests with report directory: {report_dir} ===")
    
    # Track test results
    test_results = {
        "connection_flow": "NOT_RUN"
    }
    
    driver = None
    
    try:
        # Initialize mobile driver
        print("\n" + "="*60)
        print("INITIALIZING MOBILE DRIVER")
        print("="*60)
        driver = initialize_mobile_driver(report_dir)
        
        # Test: Connection flow
        print("\n" + "="*60)
        print("TEST: CONNECTION FLOW")
        print("="*60)
        try:
            result = test_connection_flow(driver, report_dir)
            test_results["connection_flow"] = "PASSED" if result else "FAILED"
            print(f"Connection Flow test completed: {test_results['connection_flow']}")
        except Exception as e:
            test_results["connection_flow"] = "FAILED"
            print(f"Connection Flow test failed with error: {str(e)}")
            take_screenshot(driver, "test_connection_flow_final_error", report_dir)
        
        # Print final test summary
        print("\n" + "="*60)
        print("FINAL TEST SUMMARY - ZOOMCAT MOBILE CONNECTION FLOW")
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
        results = run_zoomcat_connection_flow_tests()
        
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
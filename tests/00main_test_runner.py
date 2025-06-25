import sys
import traceback
import importlib.util
import time

# Dynamically import the login test module (filename has spaces)
def import_login_module():
    module_name = "login_via_verification_code"
    file_path = "tests/Login via Verification Code.py"
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Import all test functions
from Logout_Test import run_zoomcat_logout_tests
from Purchase_Successful_Flow_Test import PurchaseSuccessfulFlowTest
from Purchase_History_Test import run_zoomcat_purchase_history_tests
from Connection_Flow_Test import run_zoomcat_connection_flow_tests
from Complaint_Submission_Test import ComplaintSubmissionTest
from Login_by_Password import run_zoomcat_password_login_tests

def main():
    print("\n=== ZOOMCAT APP AUTOMATION: MAIN TEST RUNNER ===\n")
    overall_results = {}
    
    # 1. Run Login Test
    try:
        print("\n[1/6] Running Login Test...")
        login_module = import_login_module()
        login_results = login_module.run_zoomcat_login_tests()
        overall_results['login'] = login_results
        login_passed = all(v == 'PASSED' for v in login_results.values())
    except Exception as e:
        print("Login test failed with error:", e)
        traceback.print_exc()
        overall_results['login'] = 'FAILED'
        login_passed = False
    
    # 2. Run Purchase Successful Flow Test (only if login passed)
    if login_passed:
        try:
            print("\n[2/6] Running Purchase Successful Flow Test...")
            print("Adding 5-second delay to allow app state to stabilize after login...")
            time.sleep(5)
            purchase_flow_test = PurchaseSuccessfulFlowTest()
            purchase_flow_result = purchase_flow_test.run_test()
            overall_results['purchase_successful_flow'] = 'PASSED' if purchase_flow_result else 'FAILED'
        except Exception as e:
            print("Purchase Successful Flow test failed with error:", e)
            traceback.print_exc()
            overall_results['purchase_successful_flow'] = 'FAILED'
    else:
        print("\nSkipping Purchase Successful Flow Test because Login did not pass.")
        overall_results['purchase_successful_flow'] = 'SKIPPED'
    
    # 3. Run Purchase History Test (only if previous tests passed)
    if login_passed and overall_results.get('purchase_successful_flow') == 'PASSED':
        try:
            print("\n[3/6] Running Purchase History Test...")
            purchase_history_results = run_zoomcat_purchase_history_tests()
            overall_results['purchase_history'] = purchase_history_results
        except Exception as e:
            print("Purchase History test failed with error:", e)
            traceback.print_exc()
            overall_results['purchase_history'] = 'FAILED'
    else:
        print("\nSkipping Purchase History Test because previous tests did not pass.")
        overall_results['purchase_history'] = 'SKIPPED'
    
    # 4. Run Connection Flow Test (only if previous tests passed)
    if login_passed and overall_results.get('purchase_successful_flow') == 'PASSED' and (isinstance(overall_results.get('purchase_history'), dict) and all(v == 'PASSED' for v in overall_results.get('purchase_history', {}).values())):
        try:
            print("\n[4/6] Running Connection Flow Test...")
            connection_flow_result = run_zoomcat_connection_flow_tests()
            overall_results['connection_flow'] = 'PASSED' if connection_flow_result else 'FAILED'
        except Exception as e:
            print("Connection Flow test failed with error:", e)
            traceback.print_exc()
            overall_results['connection_flow'] = 'FAILED'
    else:
        print("\nSkipping Connection Flow Test because previous tests did not pass.")
        overall_results['connection_flow'] = 'SKIPPED'
    
    # 5. Run Complaint Submission Test (only if previous tests passed)
    if login_passed and overall_results.get('purchase_successful_flow') == 'PASSED' and (isinstance(overall_results.get('purchase_history'), dict) and all(v == 'PASSED' for v in overall_results.get('purchase_history', {}).values())) and overall_results.get('connection_flow') == 'PASSED':
        try:
            print("\n[5/6] Running Complaint Submission Test...")
            complaint_submission_test = ComplaintSubmissionTest()
            complaint_submission_result = complaint_submission_test.run_test()
            overall_results['complaint_submission'] = 'PASSED' if complaint_submission_result else 'FAILED'
        except Exception as e:
            print("Complaint Submission test failed with error:", e)
            traceback.print_exc()
            overall_results['complaint_submission'] = 'FAILED'
    else:
        print("\nSkipping Complaint Submission Test because previous tests did not pass.")
        overall_results['complaint_submission'] = 'SKIPPED'
    
    # 6. Run Logout Test (only if all previous tests passed)
    if login_passed and overall_results.get('purchase_successful_flow') == 'PASSED' and (isinstance(overall_results.get('purchase_history'), dict) and all(v == 'PASSED' for v in overall_results.get('purchase_history', {}).values())) and overall_results.get('connection_flow') == 'PASSED' and overall_results.get('complaint_submission') == 'PASSED':
        try:
            print("\n[6/6] Running Logout Test...")
            logout_results = run_zoomcat_logout_tests()
            overall_results['logout'] = logout_results
        except Exception as e:
            print("Logout test failed with error:", e)
            traceback.print_exc()
            overall_results['logout'] = 'FAILED'
    else:
        print("\nSkipping Logout Test because previous tests did not pass.")
        overall_results['logout'] = 'SKIPPED'

    # 7. Run Login by Password Test (always runs last)
    try:
        print("\n[7/7] Running Login by Password Test...")
        login_by_password_results = run_zoomcat_password_login_tests()
        overall_results['login_by_password'] = login_by_password_results
    except Exception as e:
        print("Login by Password test failed with error:", e)
        traceback.print_exc()
        overall_results['login_by_password'] = 'FAILED'

    # Final summary
    print("\n=== FINAL SUMMARY ===")
    for test, result in overall_results.items():
        status_icon = "✓" if (isinstance(result, dict) and all(v == 'PASSED' for v in result.values())) or result == 'PASSED' else "✗" if result == 'FAILED' else "⚠"
        print(f"{status_icon} {test.replace('_', ' ').title()}: {result}")
    
    # Count results
    passed_count = sum(1 for result in overall_results.values() 
                      if (isinstance(result, dict) and all(v == 'PASSED' for v in result.values())) or result == 'PASSED')
    failed_count = sum(1 for result in overall_results.values() if result == 'FAILED')
    skipped_count = sum(1 for result in overall_results.values() if result == 'SKIPPED')
    
    print(f"\nOverall Results:")
    print(f"  Passed: {passed_count}")
    print(f"  Failed: {failed_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"  Total: {len(overall_results)}")
    
    # Exit code: 0 if all passed, 1 otherwise
    if failed_count == 0:
        print("\nAll tests passed or were skipped appropriately.")
        sys.exit(0)
    else:
        print("\nSome tests failed.")
        sys.exit(1)

if __name__ == "__main__":
    main() 
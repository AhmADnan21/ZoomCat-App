class Config:
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
        # Login Locators
        EMAIL_FIELD = "//android.widget.ScrollView/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]"
        VERIFICATION_CODE_FIELD = "//android.widget.ScrollView/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]"
        TERMS_CHECKBOX = "//android.widget.ScrollView/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[3]/android.widget.FrameLayout[1]/android.widget.FrameLayout"
        LOGIN_BUTTON = "//android.widget.ScrollView/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.widget.FrameLayout"
        
        # Connection Flow Locators
        CONNECT_BUTTON = "//android.view.View[@content-desc=\"Connect\"]"
        CONNECTION_TIMER = "//android.view.View[@content-desc=\"00:00:06\"]"
        CONNECTION_TIMER_AFTER_IP_SWITCH = "//android.view.View[@content-desc=\"00:00:09\"]"
        DISCONNECT_BUTTON = "//android.widget.ScrollView/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]"
        
        # Profile and Navigation Locators
        PROFILE_ICON = "//android.widget.ScrollView/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ImageView"
        MY_ACCOUNT_BUTTON = "//android.view.View[@content-desc=\"My account\"]"
        LOGOUT_BUTTON = "//android.view.View[@content-desc=\"Logout\"]"
        ORDER_HISTORY_BUTTON = "//android.view.View[@content-desc=\"Order history\"]"
        COPY_BUTTON = "//android.view.View[@content-desc=\"Copy\"]"
        
        # Purchase Flow Locators
        BUY_TAB = "//android.widget.TextView[@resource-id=\"com.zoomcat.app:id/tabTV\" and @text=\"Buy\"]"
        PURCHASE_PAGE = "//android.view.View[@content-desc=\"Purchase\"]"
        GOOGLE_PLAY_IMAGE = "//android.widget.ImageView[@content-desc=\"Google Play\"]"
        ONE_TAP_BUY_BUTTON = "(//android.widget.FrameLayout[@resource-id=\"com.android.vending:id/0_resource_name_obfuscated\"])[8]"
        PURCHASE_SUCCESSFUL_SCREEN = "//android.view.View[@content-desc=\"Purchase successful\"]"
        GO_TO_CONNECT_BUTTON = "/hierarchy/android.widget.FrameLayout"
        PROFILE_ICON_CONNECT_PAGE = "//android.widget.ScrollView/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ImageView"
        
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
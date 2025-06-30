# ZoomCat App - Mobile Automation Testing

This repository contains comprehensive automated test scripts for the ZoomCat mobile application using Appium and Python.

## 🚀 Features

- **Login/Logout Testing**: Automated verification code login and logout flows
- **Purchase Flow Testing**: Complete purchase history and successful purchase workflows
- **Complaint Submission**: Automated complaint submission testing
- **Connection Flow**: App connection and initialization testing
- **Screenshot Reporting**: Automatic screenshot capture for test debugging
- **Cross-platform Support**: Works with both Android and iOS devices

## 📁 Project Structure

```
ZoomCat_App_GH/
├── tests/                          # Test scripts
│   ├── 00main_test_runner.py      # Main test runner
│   ├── Login_by_Password.py       # Password-based login testing
│   ├── Login via Verification Code.py
│   ├── Logout_Test.py
│   ├── Purchase_History_Test.py
│   ├── Purchase_Successful_Flow_Test.py
│   ├── Complaint_Submission_Test.py
│   └── Connection_Flow_Test.py
├── mobile_automation/              # Configuration and utilities
│   ├── config.py                  # Appium configuration
│   ├── requirements.txt           # Python dependencies
│   └── README.md                  # Setup instructions
├── reports/                       # Test reports and screenshots (gitignored)
└── README.md                      # This file
```

## 🛠️ Prerequisites

- Python 3.7+
- Appium Server
- Android SDK (for Android testing)
- Xcode (for iOS testing)
- Real device or emulator

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ZoomCat-App.git
   cd ZoomCat-App
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r mobile_automation/requirements.txt
   ```

3. **Install Appium**:
   ```bash
   npm install -g appium
   ```

4. **Start Appium Server**:
   ```bash
   appium
   ```

## ⚙️ Configuration

Update the configuration in `mobile_automation/config.py`:

```python
# Device configuration
DEVICE_NAME = "your_device_name"
PLATFORM_NAME = "Android"  # or "iOS"
APP_PACKAGE = "com.zoomcat.app"
APP_ACTIVITY = "com.zoomcat.app.MainActivity"
```

## 🧪 Running Tests

### Run all tests:
```bash
python tests/00main_test_runner.py
```

### Run specific test:
```bash
python tests/Login_by_Password.py
python tests/Login via Verification Code.py
python tests/Purchase_History_Test.py
python tests/Complaint_Submission_Test.py
```

### Run with pytest:
```bash
pytest tests/ -v
```

## 📊 Test Reports

Test reports and screenshots are automatically generated in the `reports/` directory with timestamps for easy debugging and analysis.

## 🔧 Test Scripts Overview

### 1. Login by Password
- Tests username/password-based login functionality
- Validates authentication success and failure scenarios
- Comprehensive login flow testing with error handling

### 2. Login via Verification Code
- Tests email-based login with verification code
- Validates login success and error scenarios
- Screenshot capture at each step

### 3. Logout Test
- Tests user logout functionality
- Verifies proper session termination
- Validates logout confirmation

### 4. Purchase History Test
- Navigates to purchase history section
- Validates purchase records display
- Tests filtering and sorting functionality

### 5. Purchase Successful Flow Test
- Tests complete purchase workflow
- Validates payment processing
- Confirms successful purchase completion

### 6. Complaint Submission Test
- Tests complaint submission form
- Validates form validation
- Confirms complaint submission success

### 7. Connection Flow Test
- Tests app initialization
- Validates connection establishment
- Screenshots connection status

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions, please open an issue in the GitHub repository.

## 🔄 Updates

- **Latest Update**: Initial repository setup with comprehensive test suite
- **Test Coverage**: Login, Logout, Purchase, Complaint, and Connection flows
- **Framework**: Appium + Python + Pytest 
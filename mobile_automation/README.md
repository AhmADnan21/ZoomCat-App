# ZoomCat Mobile App Automation

This project contains automated tests for the ZoomCat mobile app using Appium and Python.

## Prerequisites

- Python 3.7 or higher
- Appium Server
- Android device or emulator
- Android SDK
- USB Debugging enabled on the device

## Setup

1. Install the required Python packages:
```bash
pip install -r requirements.txt
```

2. Make sure Appium server is running on `http://localhost:4723`

3. Connect your Android device or start an emulator

4. Verify the device is connected:
```bash
adb devices
```

## Running Tests

To run the login test:
```bash
pytest tests/test_login.py -v
```

## Project Structure

- `config.py`: Contains Appium capabilities and test configuration
- `pages/`: Page Object Model classes
  - `login_page.py`: Login page interactions
- `tests/`: Test files
  - `test_login.py`: Login test cases
- `requirements.txt`: Python package dependencies 
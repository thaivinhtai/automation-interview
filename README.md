# Tai Thai - Automation QA Submission

## Table of Contents
  - [Set up](#Set up)
    - [Pre-requisites](#Pre requisites)
    - [Set up the dependencies](#Set up the dependencies)
  - [Lightweight Automation Framework Usage](#Lightweight Automation Framework Usage)
    - [Before you start](#Before you start) 
    - [Quick start](#Quick start)
    - [Test the specified module](#Test the specified module)
    - [Running with different browsers](#Running with different browsers)
    - [Running in Debug Mode](#Running in Debug Mode)
    - [Open Allure Report after running](#Open Allure Report after running)
    - [More features](#More features)

## Set up
### Pre requisites
- Python 3.8 or above https://www.python.org/
- Java Runtime Environment (JRE)
- [Android Studio](https://developer.android.com/studio)
- [Appium](https://appium.io/)
- To run test on Android device/emulator, you need to set up required Environment Variable, such as: JAVA_HOME, ANDROID_HOME, ANDROID_AVD_HOME
- [Chrome Browser](https://www.google.com/chrome/)
- [Brave Browser](https://brave.com/vi/) (Optional)

### Set up the dependencies

1. Create the Python Virtual Environment:
   ```shell
   cd testing_framework
   python -m venv .venv
   ```
2. Access the Virtual Environment:
   - macOS/Linux:
      ```shell
      source .venv/bin/activate
      ```
   - Windows:
     ```shell
      .\.venv\Scripts\activate
     ```
3. Install the requirements:
   ```shell
   pip install -r requirements.txt
   ```

## Lightweight Automation Framework Usage

### Before you start
- To test sending email via Gmail and Read mail using IMAP, you need to create a "receiver_credential" file in test_data
- The test_data/receiver_credential should have the following content:
  ```shell
  username=<Gmail_account@gmail.com>
  password=<app_password> 
  ```
- To set up the Gmail app_password, please visit [here](#https://support.google.com/accounts/answer/185833?hl=en&ref_topic=7189145)

### Quick start
```shell
cd testing_framework
python main.py --device-name ${device_name} --mobile-platform-ver ${platform_version} --run-allure
```
- **_device_name_**: name of an Android emulator or real connected-device uid
  - If the _device_name_ is the name of a not-started-yet emulator, it will start automatically
- **_platform_version_**: The Android version of the device

### Test the specified module
#### Test web only
```shell
python main.py -m web
```

#### Test mobile only
```shell
python main.py -m mobile --device-name ${device_name} --mobile-platform-ver ${platform_version}
```

#### Test api only
```shell
python main.py -m api
```

#### Test web and api
```shell
python main.py -m api web
```

#### Test web and mobile
```shell
python main.py -m mobile web --device-name ${device_name} --mobile-platform-ver ${platform_version}
```

#### Test api and mobile
```shell
python main.py -m mobile api --device-name ${device_name} --mobile-platform-ver ${platform_version}
```

***IMPORTANT:*** Always declare _--device-name ${device_name} --mobile-platform-ver ${platform_version}_when running mobile.

### Running mobile test with given apk path

```shell
python main.py -m mobile --device-name ${device_name} --mobile-platform-ver ${platform_version} --app ${apk_path}
```

- If the _apk_path_ is not provided, the test will download it automatically using the link in the assigment.

### Running with different browsers

The project currently supports the following browsers: Chrome, Brave (MacOS only)

By adding the '--browser' flag and the browser name as above, the tests can be conducted on the target browser.

For example:
```shell
python main.py -m web --browser brave --run-allure --debug
```

If there is no '--browser' flag, the Chrome

### Running in Debug Mode

By adding the '--debug' flag, the scripts will run in debug mode. This means the logging is more detailed.

### Open Allure Report after running

By adding the '--run-allure' flag, the allure report will start after the test finish.

### Generate test cases document
```shell
python main.py --gen-doc
```

### More features

Fore more features of the framework, please review the file ***framework_module/args_parser.py***

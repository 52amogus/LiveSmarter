# Simple reminders



**Note: Notifications work on mac os only, winows support is coming soon**

## ⬇️ Installation

Download and install Python from https://www.python.org/downloads/.

Download the source code.

### Packages required

+ PySide6
  ```
  pip install pyside6
  ```
+ macos-notifications(If you use mac os)
  ```
  pip install macos-notifications
  ```


## Packaging into an executable file

To share the application or run it easier, you might have to build it into an executable

+ ### Using pyinstaller(all platforms)

  To install pyinstaller run the following command:

  ```
  pip install pyinstaller
  ```

  To build your application:

  ```
  pyinstaller --onefile <PATH_TO_MAIN.PY>
  ```

  The applicaion and you can run it anytime or share with anyone even if they dont have python installed.

+ ### Using py2app(mac os only)

  To install py2app, run the following:

  ```
  pip install py2app
  ```
  Make sure to run "run_before_setup.py" before starting

  Make sure pagkage "setuptools" is of version 70.3.0 or older, The newer version don`t work with py2app

  Run the following command:

  ```
  python setup.py py2app
  ```

## Usage
The app supports thse languages:
+ English
+ Русский









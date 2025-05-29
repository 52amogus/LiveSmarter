# Simple reminders



**Note: Notifications work on mac os only, winows support is coming soon**

## Orreview
This is a simple reminders app for both mac os and windows.
It is written in pure python using pyside6.
and it is still in development so, if you encounter issues, make sure to report them.

<image src = "screenshot.png">

## ⬇️ Installation

Download and install Python from https://www.python.org/downloads/.

clone the repository using git, run
```
git clone https://github.com/52amogus/Reminders/tree/main
```

For open the project folder, run
```
cd <PROJECT FOLDER>
```

### Packages required

To install everything, run
```
pip install -r requirements.txt
```
Or you can install the packages one by one from this list

+ PySide6
  ```
  pip install pyside6
  ```
+ Or PySide6_Essentials (If you don`t have a lot of disk space left)
  ```
  pip install pyside6-essentials
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









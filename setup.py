from setuptools import setup

APP = ['main.py']
#DATA_FILES = ["languages.json"]
OPTIONS = {"iconfile":"icon"}

setup(
    app=APP,
    name="LiveSmarter",
    version="1.0",
    #data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

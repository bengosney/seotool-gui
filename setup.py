#!/usr/bin/env python
# Third Party
from setuptools import find_packages, setup

setup(
    name="seotool GUI",
    version="0.0.1",
    packages=find_packages(),
    python_requires="~=3.8",
    install_requires=[
        "pyqt5",
        "pyqt5-tools",
        "rich",
        "qasync",
        "seotool",
    ],
    entry_points={"seo_processor": ["guioutput=seogui.gui"]},
)

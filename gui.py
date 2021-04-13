import asyncio
import functools
# from PyQt5.QtWidgets import QApplication
import sys
from pprint import pprint

import qasync
from icecream import ic
from PyQt5 import QtCore, QtGui, QtWidgets
from qasync import QApplication, asyncClose, asyncSlot
from rich.console import Console

import ui
from seogui.gui import main

if __name__ == "__main__":
    try:
        qasync.run(main())
    except asyncio.exceptions.CancelledError:
        sys.exit(0)

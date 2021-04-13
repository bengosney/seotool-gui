import asyncio
import functools
# from PyQt5.QtWidgets import QApplication
import sys
from pprint import pprint

import qasync
from icecream import ic
from processors import hookimpl_processor
from PyQt5 import QtCore, QtGui, QtWidgets
from qasync import QApplication, asyncClose, asyncSlot
from rich.console import Console
from seotool.crawl import Crawler

import ui

updateFunctions = []
output = ""


@hookimpl_processor(tryfirst=True)
def log(line):
    global updateFunctions, output

    output = f"{output}\n{line}"
    ic(updateFunctions)
    for updateFunction in updateFunctions:
        updateFunction(output)


class SeoGUI(QtWidgets.QMainWindow, ui.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()

    @asyncSlot()
    async def doCrawl(self):
        url = self.inputURL.text()
        self.crawler = Crawler(url)
        ic(self.crawler.get_plugin_list())
        await self.crawler.crawl()

    def updateOutput(self, text):
        self.textOutput.document().setPlainText(text)
        # self.textOutput

    def connectSignalsSlots(self):
        self.btnCrawl.clicked.connect(self.doCrawl)


async def main():
    global updateFunctions

    def close_future(future, loop):
        loop.call_later(10, future.cancel)
        future.cancel("Close Application")

    loop = asyncio.get_event_loop()
    future = asyncio.Future()

    app = QApplication.instance()
    if hasattr(app, "aboutToQuit"):
        getattr(app, "aboutToQuit").connect(
            functools.partial(close_future, future, loop)
        )

    form = SeoGUI()
    updateFunctions.append(form.updateOutput)
    form.show()

    await future

    return True


if __name__ == "__main__":
    try:
        qasync.run(main())
    except asyncio.exceptions.CancelledError:
        sys.exit(0)

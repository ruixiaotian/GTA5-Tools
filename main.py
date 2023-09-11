#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :main.py
# @Time :2023-9-10 下午 04:24
# @Author :Qiao
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from creart import it

from Ui import MainWindow

if __name__ == "__main__":

    #  适配高DPI
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    it(MainWindow)
    app.exec()

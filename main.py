#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :main.py
# @Time :2023-9-10 下午 04:24
# @Author :Qiao
import sys

from PyQt5.QtCore import Qt, QLocale, QTranslator
from PyQt5.QtWidgets import QApplication
from creart import it
from qfluentwidgets import FluentTranslator

from Ui import MainWindow

if __name__ == "__main__":
    #  适配高DPI
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # 创建app实例
    app = QApplication(sys.argv)

    # 加载翻译
    app.instance()

    fluentTranslator = FluentTranslator(QLocale(QLocale.Chinese, QLocale.China))
    settingTranslator = QTranslator()
    settingTranslator.load(
        QLocale(QLocale.Chinese, QLocale.China),
        "MenuInstaller",
        "_",
        "Ui/resource/i18n"
    )

    app.installTranslator(fluentTranslator)
    app.installTranslator(settingTranslator)

    # 显示窗体
    it(MainWindow)
    # 进入循环
    app.exec()

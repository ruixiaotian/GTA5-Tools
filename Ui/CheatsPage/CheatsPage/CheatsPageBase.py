#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :CheatsPageBase.py
# @Time :2023-9-20 下午 10:46
# @Author :Qiao
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets.common import FluentIconBase

from Ui.CheatsPage.CheatsPage.Control import MenuInfoCard, MenuContentCard
from Ui.StyleSheet import CheatsPageStyleSheet


class CheatsPageBase(QWidget):
    objectName: str | None
    icon: FluentIconBase | None
    name: str | None
    url: str | None
    tagDict: dict | None

    InfoDict = {
        "system": None,  # 系统要求
        "untie": None,  # 解绑时间
        "opMode": None,  # 操作方式
        "Key": None,  # 呼出键
        "Lua": None,  # Lua支持性
        "Shv": None,  # Shv插件支持性
        "Mode": None,  # Mod支持性
        "Language": None  # 是否支持多语言
    }

    def __init__(self):
        super().__init__()
        self.setObjectName(self.objectName)

        self.createControl()
        self.setupLayout()

        CheatsPageStyleSheet.CHEATS_PAGE.apply(self)

    def createControl(self):
        self.menuInfoCard = MenuInfoCard(self.icon, self.name, self.url)
        self.menuContentCard = MenuContentCard(self, self.InfoDict)

    def setupLayout(self):
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(int(self.height() * 0.4), 20, int(self.height() * 0.4), 20)
        self.vBoxLayout.addWidget(self.menuInfoCard)
        self.vBoxLayout.addWidget(self.menuContentCard)

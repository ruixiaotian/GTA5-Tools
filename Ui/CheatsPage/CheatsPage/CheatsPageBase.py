#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :CheatsPageBase.py
# @Time :2023-9-20 下午 10:46
# @Author :Qiao
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets.common import FluentIconBase
from qfluentwidgets.components import (
    ScrollArea
)

from Ui.CheatsPage.CheatsPage.Control import MenuInfoCard
from Ui.StyleSheet import CheatsPageStyleSheet


class CheatsPageBase(QWidget):
    objectName: str | None
    icon: FluentIconBase | None
    name: str | None
    url: str | None

    def __init__(self):
        super().__init__()
        self.setObjectName(self.objectName)

        self.createControl()
        self.setupLayout()

        CheatsPageStyleSheet.CHEATS_PAGE.apply(self)

    def createControl(self):
        self.menuInfoCard = MenuInfoCard(self.icon, self.name, self.url)

    def setupLayout(self):
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(30, 20, 30, 10)
        self.vBoxLayout.addWidget(self.menuInfoCard)
        self.vBoxLayout.addWidget(QWidget())

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :MenuContentCard.py
# @Time :2023-10-28 下午 09:52
# @Author :Qiao
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout
)
from qfluentwidgets.common import FluentIconBase, setFont
from qfluentwidgets.components import (
    CaptionLabel, BodyLabel, IconWidget, FlowLayout, HeaderCardWidget
)

from Ui.StyleSheet import CheatsPageStyleSheet
from Ui.icon import CheatsPageIcon as CPI


class MenuContentCard(HeaderCardWidget):

    def __init__(self, parent, InfoDict: dict) -> None:
        """初始化"""
        super().__init__()
        self.parent = parent
        self.InfoDict = InfoDict

        self.infoPage = InfoPage(self, self.InfoDict)
        self.viewLayout.addWidget(self.infoPage)
        self.setTitle("Menu Other Info")


class InfoPage(QWidget):

    def __init__(self, parent, infoDict: dict) -> None:
        """初始化"""
        super().__init__(parent=parent)
        # 对字典进行处理
        self.infoDict = {k: self.tr("Unknown") if v is None else v for k, v in infoDict.items()}
        self.infoDict = {
            k: self.tr("Support") if v is True else self.tr("Not Supported") if v is False else v
            for k, v in self.infoDict.items()
        }
        self.addLayout()

    def createControl(self):
        """创建控件"""
        self.systemItem = InfoItem(CPI.SYSTEM, self.tr("System Demand"), CaptionLabel(self.infoDict["system"]))
        self.untieItem = InfoItem(CPI.TIME, self.tr("Untie Time"), CaptionLabel(self.infoDict["untie"]))
        self.opMode = InfoItem(CPI.OPERATE, self.tr("Operate Mode"), CaptionLabel(self.infoDict["opMode"]))
        self.keyItem = InfoItem(CPI.KEY, self.tr("Out Key"), CaptionLabel(self.infoDict["Key"]))
        self.luaItem = InfoItem(CPI.LUA, self.tr("Lua plug-in unit"), CaptionLabel(self.infoDict["Lua"]))
        self.shvItem = InfoItem(CPI.SHV, self.tr("Shv plug-in unit"), CaptionLabel(self.infoDict["Shv"]))
        self.modItem = InfoItem(CPI.MOD, self.tr("Mode"), CaptionLabel(self.infoDict["Mode"]))
        self.languageItem = InfoItem(CPI.LANGUAGE, self.tr("Language"), CaptionLabel(self.infoDict["Language"]))
        self.controlList = [
            self.systemItem, self.untieItem, self.opMode, self.keyItem, self.luaItem, self.shvItem,
            self.modItem, self.languageItem
        ]

    def addLayout(self):
        """添加到控件"""
        self.createControl()
        self.flowLayout = FlowLayout(self, needAni=True)
        self.flowLayout.setContentsMargins(30, 10, 5, 10)
        self.flowLayout.setHorizontalSpacing(15)
        self.flowLayout.setVerticalSpacing(60)
        for control in self.controlList:
            self.flowLayout.addWidget(control)


class InfoItem(QWidget):

    def __init__(self, icon: FluentIconBase, title: str, value: CaptionLabel):
        """要求控件"""
        super().__init__()
        self.setFixedWidth(220)

        self.iconWidget = IconWidget(icon, self)
        self.titleLabel = BodyLabel(title, self)
        self.valueLabel = value
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout1 = QVBoxLayout()
        self.vBoxLayout2 = QVBoxLayout()

        self.iconWidget.setFixedSize(14, 14)
        self.titleLabel.setObjectName("systemDemandTitleLabel")
        self.valueLabel.setObjectName("systemDemandValueLabel")

        self.vBoxLayout1.addWidget(self.iconWidget)
        self.vBoxLayout1.addSpacing(10)
        self.vBoxLayout2.addWidget(self.titleLabel)
        self.vBoxLayout2.addWidget(self.valueLabel)
        self.hBoxLayout.addLayout(self.vBoxLayout1)
        self.hBoxLayout.addLayout(self.vBoxLayout2)

        self.vBoxLayout1.setContentsMargins(0, 0, 0, 10)
        self.vBoxLayout2.setContentsMargins(0, 1, 0, 0)
        self.vBoxLayout2.setSpacing(1)

        self.hBoxLayout.setContentsMargins(15, 0, 10, 0)
        self.hBoxLayout.setSpacing(8)

        setFont(self.valueLabel, 16, QFont.Normal)

        CheatsPageStyleSheet.CHEATS_PAGE.apply(self)

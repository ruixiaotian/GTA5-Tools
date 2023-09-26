#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :Control.py
# @Time :2023-9-20 下午 10:47
# @Author :Qiao
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy,
    QStackedWidget
)
from qfluentwidgets.common import FluentIconBase, setFont
from qfluentwidgets.components import (
    SimpleCardWidget, ImageLabel, TitleLabel, HyperlinkLabel,
    PrimaryPushButton, CaptionLabel, BodyLabel, VerticalSeparator,
    PillPushButton, Pivot, IconWidget, FlowLayout
)

from Ui.StyleSheet import CheatsPageStyleSheet
from Ui.icon import CheatsPageIcon as CPI


class MenuInfoCard(SimpleCardWidget):
    """ 菜单信息卡片 """

    def __init__(self, icon: FluentIconBase, name: str, url: str):
        super().__init__()
        self.icon = icon
        self.name = name
        self.url = url

        self.createControl()
        self.setupControl()
        self.setupLayout()

        CheatsPageStyleSheet.CHEATS_PAGE.apply(self)

    def createControl(self):
        """创建需要的控件"""
        # 基本控件
        self.iconLabel = ImageLabel(self.icon.path(), self)
        self.nameLabel = TitleLabel(self.name, self)
        self.urlLabel = HyperlinkLabel(QUrl(self.url), self.tr("Open the official website"), self)
        self.installButton = PrimaryPushButton(self.tr("Install"), self)
        self.usabilityWidget = StatisticsWidget(self.tr("Preserve"), self.tr("Unknown"))
        self.separator = VerticalSeparator(self)
        self.versionWidget = StatisticsWidget(self.tr("Version"), self.tr("Unknown"))

    def setupControl(self):
        """设置控件"""
        # 设置自身
        self.setFixedHeight(220)

        # 命名
        self.nameLabel.setObjectName("nameLabel")
        self.urlLabel.setObjectName("urlLabel")
        self.installButton.setObjectName("installButton")

        # 设置子控件
        self.nameLabel.setFixedHeight(25)
        self.iconLabel.scaledToWidth(160)
        self.installButton.setFixedWidth(160)

    def setupLayout(self):
        """设置布局"""
        # 创建控件
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.statisticsLayout = QHBoxLayout()
        self.tagLayout = TagLayout()

        # 添加控件
        self.hBoxLayout.setSpacing(20)
        self.hBoxLayout.setContentsMargins(30, 20, 30, 20)
        self.hBoxLayout.addWidget(self.iconLabel)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 10)
        self.vBoxLayout.setSpacing(0)

        # 添加名字Label和安装按钮
        self.vBoxLayout.addLayout(self.topLayout)
        self.topLayout.setContentsMargins(0, 8, 10, 5)
        self.topLayout.addWidget(self.nameLabel)
        self.topLayout.addWidget(self.installButton, 0, Qt.AlignRight)

        # 添加链接Label
        self.vBoxLayout.addWidget(self.urlLabel)
        self.vBoxLayout.addSpacing(12)

        # 添加统计信息Label
        self.vBoxLayout.addLayout(self.statisticsLayout)
        self.statisticsLayout.setContentsMargins(0, 0, 0, 0)
        self.statisticsLayout.setSpacing(0)
        self.statisticsLayout.addWidget(self.usabilityWidget)
        self.statisticsLayout.addWidget(self.separator)
        self.statisticsLayout.addWidget(self.versionWidget)
        self.statisticsLayout.setAlignment(Qt.AlignLeft)
        self.vBoxLayout.addSpacing(13)

        # 添加tag布局
        self.vBoxLayout.addLayout(self.tagLayout)


class StatisticsWidget(QWidget):
    """ 统计信息 """

    def __init__(self, title: str, value: str, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(35)
        self.titleLabel = CaptionLabel(title, self)
        self.valueLabel = BodyLabel(value, self)
        self.vBoxLayout = QVBoxLayout(self)

        self.titleLabel.setObjectName("statisticsTitleLabel")
        self.valueLabel.setObjectName("statisticsValueLabel")

        self.vBoxLayout.setContentsMargins(16, 0, 16, 0)
        self.vBoxLayout.addWidget(self.valueLabel, 0, Qt.AlignTop)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignBottom)

        setFont(self.valueLabel, 18, QFont.DemiBold)

        CheatsPageStyleSheet.CHEATS_PAGE.apply(self)


class TagLayout(QHBoxLayout):

    def __init__(self):
        super().__init__()
        self.setSpacing(10)
        self.setContentsMargins(0, 0, 0, 0)

        self.createTag()
        self.addTag()
        self.setupTag()

    def createTag(self):
        """创建Tag"""
        self.luaTag = PillPushButton(self.tr("Lua"))
        self.languageTag = PillPushButton(self.tr("Polyglot"))

        self.tagList = [self.luaTag, self.languageTag]

    def addTag(self):
        """添加到布局"""
        for tag in self.tagList:
            self.addWidget(tag, 0, Qt.AlignLeft)
        self.addSpacerItem(QSpacerItem(10, 1, hPolicy=QSizePolicy.Expanding))

    def setupTag(self):
        """设置Tag"""
        for tag in self.tagList:
            tag.setCheckable(False)


class MenuContentCard(SimpleCardWidget):

    def __init__(self, parent, InfoDict: dict) -> None:
        """初始化"""
        super().__init__()
        self.parent = parent
        self.InfoDict = InfoDict

        self.createControl()
        self.setupControl()
        self.setupLayout()

    def createControl(self):
        """创建需要的控件"""
        self.pivot = Pivot(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.infoPage = InfoPage(self, self.InfoDict)

        self.addSubInterface(self.infoPage, "InfoPage", self.tr("Info"))

    def setupControl(self):
        """设置控件"""
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)

    def addSubInterface(self, widget: QWidget, objectName: str, text: str):
        """添加页面的接口函数"""
        widget.setObjectName(objectName)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )

    def setupLayout(self):
        """设置布局"""
        self.vBoxLayout.addWidget(self.pivot)
        self.vBoxLayout.addWidget(self.stackedWidget)

    def onCurrentIndexChanged(self, index: int):
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())


class InfoPage(QWidget):

    def __init__(self, parent, infoDict: dict) -> None:
        """初始化"""
        super().__init__(parent=parent)
        # 对字典进行处理
        self.infoDict = {k: "Unknown" if v is None else v for k, v in infoDict.items()}
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
        self.setFixedWidth(240)

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

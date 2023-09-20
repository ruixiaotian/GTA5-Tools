#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :Control.py
# @Time :2023-9-20 下午 10:47
# @Author :Qiao
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from qfluentwidgets.common import FluentIconBase, setFont
from qfluentwidgets.components import (
    SimpleCardWidget, ImageLabel, TitleLabel, HyperlinkLabel,
    PrimaryPushButton, CaptionLabel, BodyLabel, VerticalSeparator,
    PillPushButton
)
from qfluentwidgets.common import FluentIcon as FIF


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

        # 标签
        self.luaTag = PillPushButton(self.tr("Support Lua"), self)
        self.tagList = [self.luaTag]

    def setupControl(self):
        """设置控件"""
        # 设置自身
        self.setFixedHeight(220)

        # 设置子控件
        self.nameLabel.setFixedHeight(25)
        self.iconLabel.scaledToWidth(160)
        self.installButton.setFixedWidth(160)
        self.luaTag.setIcon(FIF.CODE)
        for tag in self.tagList:
            tag.setCheckable(False)

    def setupLayout(self):
        """设置布局"""
        # 创建控件
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.statisticsLayout = QHBoxLayout()
        self.tagLayout = QHBoxLayout()

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
        self.topLayout.setSpacing(0)
        self.tagLayout.setContentsMargins(0, 0, 0, 0)
        self.tagLayout.addWidget(self.luaTag, 0, Qt.AlignLeft)
        self.tagLayout.addSpacing(10)


class StatisticsWidget(QWidget):
    """ 统计信息 """

    def __init__(self, title: str, value: str, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(35)
        self.titleLabel = CaptionLabel(title, self)
        self.valueLabel = BodyLabel(value, self)
        self.vBoxLayout = QVBoxLayout(self)

        self.vBoxLayout.setContentsMargins(16, 0, 16, 0)
        self.vBoxLayout.addWidget(self.valueLabel, 0, Qt.AlignTop)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignBottom)

        setFont(self.valueLabel, 18, QFont.DemiBold)
        self.titleLabel.setTextColor(QColor(96, 96, 96), QColor(206, 206, 206))

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :CheatsCard.py
# @Time :2023-9-11 下午 08:15
# @Author :Qiao
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from creart import it
from qfluentwidgets.common import FluentIconBase
from qfluentwidgets.components import (
    IconWidget, CardWidget, TabBar
)

from Ui.StyleSheet import CheatsPageStyleSheet
from Ui.icon import CheatsIcon as Ci


class CheatsCardBase(CardWidget):
    iconWidget: IconWidget
    titleLabel: QLabel
    routeKey: str
    text: str
    icon: FluentIconBase
    page: QWidget

    def __init__(self) -> None:
        """初始化控件"""
        super().__init__()
        # 设置卡片属性
        self.setFixedSize(200, 280)
        self.setCursor(Qt.PointingHandCursor)

        # 创建子控件
        self.iconWidget = IconWidget(self)
        self.titleLabel = QLabel(self)

        # 设置子控件
        self.iconWidget.setFixedSize(96, 96)
        self.titleLabel.setObjectName("titleLabel")
        self.titleLabel.setAlignment(Qt.AlignCenter)

        # 设置布局
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addSpacing(40)
        self.vBoxLayout.addWidget(self.iconWidget)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.setAlignment(Qt.AlignHCenter)
        self.setLayout(self.vBoxLayout)

        # 引用样式表
        CheatsPageStyleSheet.CHEATS_CARD.apply(self)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """重构鼠标事件实现点击效果"""
        super().mouseReleaseEvent(event)
        from Ui import MainWindow
        from Ui.CheatsPage import CheatsWidget
        self.tabBar: TabBar = it(MainWindow).titleBar.tabBar
        if self.routeKey in self.tabBar.itemMap:
            # 判断路由键是否重复
            it(CheatsWidget).setCurrentWidget(self.page)
            self.tabBar.setCurrentTab(self.routeKey)
        else:
            self.tabBar.insertTab(
                index=self.tabBar.count(),
                routeKey=self.routeKey,
                text=self.text,
                icon=self.icon,
                onClick=self.tabTrough
            )
            self.tabBar.setCurrentTab(self.routeKey)
            it(MainWindow).titleBar.router[f'{self.tabBar.count()}'] = "CheatsPage"
            it(CheatsWidget).setCurrentWidget(self.page)

    def tabTrough(self) -> None:
        """tab标签被点击时的槽函数"""
        from Ui import MainWindow
        from Ui.CheatsPage import CheatsWidget
        it(MainWindow).stackedWidget.setCurrentWidget(it(CheatsWidget))
        it(CheatsWidget).setCurrentWidget(it(CheatsWidget).findChild(QWidget, self.routeKey))


class TwoTakeOneCard(CheatsCardBase):

    def __init__(self) -> None:
        """初始化控件"""
        super().__init__()
        # 设置子控件
        self.iconWidget.setIcon(Ci.TWO_TAKE_ONE)
        self.titleLabel.setText(self.tr("2TAKE1"))

        from Ui.CheatsPage import CheatsWidget
        self.routeKey = '2take1'
        self.text = '2TAKE1'
        self.icon = Ci.TWO_TAKE_ONE
        self.page = it(CheatsWidget).twoTakeOnePage


class StandCard(CheatsCardBase):

    def __init__(self) -> None:
        """初始化控件"""
        super().__init__()
        # 设置子控件
        self.iconWidget.setIcon(Ci.STAND)
        self.titleLabel.setText(self.tr("Stand"))

        from Ui.CheatsPage import CheatsWidget
        self.routeKey = 'Stand'
        self.text = 'Stand'
        self.icon = Ci.STAND
        self.page = it(CheatsWidget).standPage

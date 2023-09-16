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
    IconWidget, CardWidget, TabBar, TabItem, TabCloseButtonDisplayMode
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
        self.setFixedSize(195, 240)
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
        if self.routeKey in it(MainWindow).titleBar.tabBar.itemMap:
            # 判断routeKey是否重复
            it(CheatsWidget).setCurrentWidget(self.page)
            it(MainWindow).titleBar.tabBar.setCurrentTab(self.routeKey)
        else:
            self.addTab()

    def addTab(self):
        """添加Tab"""
        from Ui import MainWindow
        from Ui.CheatsPage import CheatsWidget
        self.tabBar: TabBar = it(MainWindow).titleBar.tabBar

        self.item = TabItem(self.text, self.tabBar.view, self.icon)
        self.item.setRouteKey(self.routeKey)

        # 设置Tab大小
        self.item.setMinimumWidth(self.tabBar.tabMaximumWidth())
        self.item.setMaximumWidth(self.tabBar.tabMaximumWidth())

        # 设置样式
        self.item.setShadowEnabled(self.tabBar.isTabShadowEnabled())
        self.item.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.ON_HOVER)
        self.item.setSelectedBackgroundColor(
            self.tabBar.lightSelectedBackgroundColor,
            self.tabBar.darkSelectedBackgroundColor
        )

        # 链接信号
        self.item.pressed.connect(self.tabTrough)
        self.item.closed.connect(self.tabCloseTrough)

        # 添加进tab
        index = self.tabBar.count() + 1
        self.tabBar.itemLayout.insertWidget(index, self.item, 1)
        self.tabBar.items.insert(index, self.item)
        self.tabBar.itemMap[self.routeKey] = self.item

        # 切换至tab和切换至相对应页面
        self.tabTrough()

    def tabTrough(self) -> None:
        """tab标签被点击时的槽函数"""
        from Ui import MainWindow
        from Ui.CheatsPage import CheatsWidget
        self.tabBar.setCurrentTab(self.routeKey)
        it(MainWindow).stackedWidget.setCurrentWidget(it(CheatsWidget))
        it(CheatsWidget).setCurrentWidget(it(CheatsWidget).findChild(QWidget, self.routeKey))

    def tabCloseTrough(self) -> None:
        """tab标签关闭时槽函数"""
        from Ui.CheatsPage import CheatsWidget
        it(CheatsWidget).setCurrentWidget(it(CheatsWidget).HomePage)
        self.tabBar.setCurrentTab("HomeTab")
        self.tabBar.tabCloseRequested.emit(self.tabBar.items.index(self.item))


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
        self.page = it(CheatsWidget).TwoTakeOnePage


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
        self.page = it(CheatsWidget).StandPage


class DarkStarCard(CheatsCardBase):

    def __init__(self) -> None:
        """初始化控件"""
        super().__init__()
        # 设置子控件
        self.iconWidget.setIcon(Ci.DARK_STAR)
        self.titleLabel.setText(self.tr("DarkStar"))

        from Ui.CheatsPage import CheatsWidget
        self.routeKey = 'DarkStar'
        self.text = 'DarkStar'
        self.icon = Ci.DARK_STAR
        self.page = it(CheatsWidget).DarkStarPage


class XiProCard(CheatsCardBase):

    def __init__(self) -> None:
        """初始化控件"""
        super().__init__()
        # 设置子控件
        self.iconWidget.setIcon(Ci.XI_PRP)
        self.titleLabel.setText(self.tr("XiPro"))

        from Ui.CheatsPage import CheatsWidget
        self.routeKey = 'XiPro'
        self.text = 'XiPro'
        self.icon = Ci.XI_PRP
        self.page = it(CheatsWidget).XiProPage


class MidnightCard(CheatsCardBase):

    def __init__(self) -> None:
        """初始化控件"""
        super().__init__()
        # 设置子控件
        self.iconWidget.setIcon(Ci.MIDNIGHT)
        self.titleLabel.setText(self.tr("Midnight"))

        from Ui.CheatsPage import CheatsWidget
        self.routeKey = 'Midnight'
        self.text = 'Midnight'
        self.icon = Ci.MIDNIGHT
        self.page = it(CheatsWidget).MidnightPage


class NightfallCard(CheatsCardBase):

    def __init__(self) -> None:
        """初始化控件"""
        super().__init__()
        # 设置子控件
        self.iconWidget.setIcon(Ci.NIGHTFALL)
        self.titleLabel.setText(self.tr("Nightfall"))

        from Ui.CheatsPage import CheatsWidget
        self.routeKey = 'Nightfall'
        self.text = 'Nightfall'
        self.icon = Ci.NIGHTFALL
        self.page = it(CheatsWidget).NightfallPage


class OxCheatsCard(CheatsCardBase):

    def __init__(self) -> None:
        """初始化控件"""
        super().__init__()
        # 设置子控件
        self.iconWidget.setIcon(Ci.OX_CHEATS)
        self.titleLabel.setText(self.tr(" OxCheats"))

        from Ui.CheatsPage import CheatsWidget
        self.routeKey = 'OxCheats'
        self.text = 'OxCheats'
        self.icon = Ci.OX_CHEATS
        self.page = it(CheatsWidget).OxCheatsPage


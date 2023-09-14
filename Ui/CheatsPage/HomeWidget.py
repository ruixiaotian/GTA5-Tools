#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :HomeWidget.py
# @Time :2023-9-11 下午 08:11
# @Author :Qiao
from PyQt5.QtCore import QEasingCurve, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from qfluentwidgets.components import FlowLayout, SmoothScrollArea

from creart import it

from Ui.CheatsPage.CheatsCard import (
    TwoTakeOneCard, StandCard, DarkStarCard, XiProCard, MidnightCard, NightfallCard,
    OxCheatsCard
)
from Ui.StyleSheet import CheatsPageStyleSheet


class CheatsHome(QWidget):
    """菜单页面的主页"""

    def __init__(self, parent) -> None:
        super().__init__()
        self.setObjectName("CheatsHome")
        self.view = CardView(parent)

        self.setupLayout()

    def setupLayout(self) -> None:
        """设置布局"""
        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.addWidget(self.view, 10)

        self.setLayout(self.vBoxLayout)


class CardView(SmoothScrollArea):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setupView()
        self.setupViewLayout()

        self.setScrollAnimation(Qt.Vertical, 400, QEasingCurve.OutQuint)
        self.setWidgetResizable(True)
        self.setWidget(self.view)

        CheatsPageStyleSheet.HOME_PAGE.apply(self)

    def setupView(self) -> None:
        """创建视图"""
        from Ui import MainWindow
        # 创建控件
        self.view = QWidget()
        self.view.setObjectName("view")
        # 获取卡片
        self.TwoTakeOneCard = TwoTakeOneCard()
        self.StandCard = StandCard()
        self.DarkStarCard = DarkStarCard()
        self.XiProCard = XiProCard()
        self.MidnightCard = MidnightCard()
        self.NightfallCard = NightfallCard()
        self.OxCheatsCard = OxCheatsCard()

    def setupViewLayout(self) -> None:
        """设置布局"""
        self.flowLayout = FlowLayout(self, needAni=True)
        self.flowLayout.setAnimation(650, QEasingCurve.OutQuad)

        self.flowLayout.setContentsMargins(30, 30, 30, 30)
        self.flowLayout.setHorizontalSpacing(15)
        self.flowLayout.setVerticalSpacing(25)

        self.flowLayout.addWidget(self.TwoTakeOneCard)
        self.flowLayout.addWidget(self.StandCard)
        self.flowLayout.addWidget(self.DarkStarCard)
        self.flowLayout.addWidget(self.XiProCard)
        self.flowLayout.addWidget(self.MidnightCard)
        self.flowLayout.addWidget(self.NightfallCard)
        self.flowLayout.addWidget(self.OxCheatsCard)

        self.view.setLayout(self.flowLayout)

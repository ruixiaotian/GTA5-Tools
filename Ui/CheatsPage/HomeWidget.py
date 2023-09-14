#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :HomeWidget.py
# @Time :2023-9-11 下午 08:11
# @Author :Qiao
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QEasingCurve

from qfluentwidgets.components import FlowLayout

from Ui.CheatsPage.CheatsCard import (
    TwoTakeOneCard, StandCard, DarkStarCard, XiProCard, MidnightCard, NightfallCard,
    OxCheatsCard
)


class CheatsHome(QWidget):
    """菜单页面的主页"""

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("CheatsHome")

        # 获取卡片
        self.TwoTakeOneCard = TwoTakeOneCard()
        self.StandCard = StandCard()
        self.DarkStarCard = DarkStarCard()
        self.XiProCard = XiProCard()
        self.MidnightCard = MidnightCard()
        self.NightfallCard = NightfallCard()
        self.OxCheatsCard = OxCheatsCard()

        self.setupLayout()

    def setupLayout(self) -> None:
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

        self.setLayout(self.flowLayout)

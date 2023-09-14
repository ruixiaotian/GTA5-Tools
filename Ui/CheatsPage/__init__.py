#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :__init__.py.py
# @Time :2023-9-11 下午 07:59
# @Author :Qiao
from abc import ABC

from PyQt5.QtWidgets import QStackedWidget
from creart import add_creator, exists_module
from creart.creator import CreateTargetInfo, AbstractCreator

from Ui.CheatsPage.CheatsPage import (
    TwoTakeOnePage, StandPage, DarkStarPage, XiProPage, MidnightPage, NightfallPage,
    OxCheatsPage
)
from Ui.CheatsPage.HomeWidget import CheatsHome


class CheatsWidget(QStackedWidget):
    """菜单界面"""

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("CheatsPage")

    def initialize(self, parent) -> None:
        """初始化"""
        self.parentClass = parent
        self.addPage()

    def addPage(self) -> None:
        """添加子页面"""
        # 获取页面
        self.TwoTakeOnePage = TwoTakeOnePage()
        self.StandPage = StandPage()
        self.DarkStarPage = DarkStarPage()
        self.XiProPage = XiProPage()
        self.MidnightPage = MidnightPage()
        self.NightfallPage = NightfallPage()
        self.OxCheatsPage = OxCheatsPage()
        self.HomePage = CheatsHome()
        # 添加页面
        self.addWidget(self.HomePage)
        self.addWidget(self.TwoTakeOnePage)
        self.addWidget(self.StandPage)
        self.addWidget(self.DarkStarPage)
        self.addWidget(self.XiProPage)
        self.addWidget(self.MidnightPage)
        self.addWidget(self.NightfallPage)
        self.addWidget(self.OxCheatsPage)


class CheatsWidgetClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (CreateTargetInfo("Ui.CheatsPage", "CheatsWidget"),)

    # 静态方法available()，用于检查模块"CheatsWidget"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Ui.CheatsPage")

    # 静态方法create()，用于创建CheatsWidget类的实例，返回值为CheatsWidget对象。
    @staticmethod
    def create(create_type: [CheatsWidget]) -> CheatsWidget:
        return CheatsWidget()


add_creator(CheatsWidgetClassCreator)

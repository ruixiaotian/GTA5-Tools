#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :CheatsPageBase.py
# @Time :2023-9-20 下午 10:46
# @Author :Qiao
from typing import Dict, List, Union
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from qfluentwidgets.common import FluentIconBase
from qfluentwidgets.components import SingleDirectionScrollArea

from Ui.CheatsPage.CheatsPage.Control import MenuInfoCard, MenuContentCard
from Ui.StyleSheet import CheatsPageStyleSheet


class CheatsPageBase(QWidget):
    objectName: str | None
    icon: FluentIconBase | None
    name: str | None
    dwUrl: Dict[str, Union[bool, str, List[Dict[str, str]]]]
    url: str | None
    tagDict: dict | None

    InfoDict = {
        "system": None,  # 系统要求
        "untie": None,  # 解绑时间
        "opMode": None,  # 操作方式
        "Key": None,  # 呼出键
        "Lua": None,  # Lua支持性
        "Asi": None,  # ASI 插件支持性
        "Shv": None,  # Shv插件支持性
        "Mode": None,  # Mod支持性
        "Language": None  # 是否支持多语言
    }
    dwUrl = {
        "multipleVersions": False,
        "url": None,
        "versionList": [
            {
                "name": None,
                "url": None
            }
        ]
    }

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName(self.objectName)

        self.createControl()
        self.setupLayout()

        CheatsPageStyleSheet.CHEATS_PAGE.apply(self)

        # 将控件从子控件提取出来
        self.installButton = self.centreWidget.menuInfoCard.installButton
        self.downloadBar = self.centreWidget.menuInfoCard.downloadBar
        self.inDownloadBar = self.centreWidget.menuInfoCard.inDownloadBar
        self.infoBar = self.centreWidget.menuInfoCard.infoBar

    def createControl(self) -> None:
        self.centreWidget = CentreWidget(self)

    def setupLayout(self) -> None:
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(int(self.width() * 0.3), 20, int(self.width() * 0.3), 20)
        self.hBoxLayout.addWidget(self.centreWidget)


class CentreWidget(SingleDirectionScrollArea):
    """中间的内容展示"""

    def __init__(self, parent: CheatsPageBase) -> None:
        super().__init__(parent=parent)
        self.parent: CheatsPageBase = parent
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.createControl()
        self.setupLayout()

    def createControl(self) -> None:
        self.menuInfoCard = MenuInfoCard(self.parent)
        self.menuContentCard = MenuContentCard(self, self.parent.InfoDict)

    def setupLayout(self) -> None:
        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.addWidget(self.menuInfoCard)
        self.vBoxLayout.addWidget(self.menuContentCard)

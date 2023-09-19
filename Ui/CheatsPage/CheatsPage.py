#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :CheatsPage.py
# @Time :2023-9-11 下午 09:47
# @Author :Qiao
from PyQt5.QtWidgets import QLabel
from qfluentwidgets.components import ScrollArea

from Ui.StyleSheet import CheatsPageStyleSheet


class CheatsPageBase(ScrollArea):
    objectName: str | None

    def __init__(self):
        super().__init__()
        self.setObjectName(self.objectName)

        CheatsPageStyleSheet.CHEATS_PAGE.apply(self)


class TopCard:
    pass


class TwoTakeOnePage(CheatsPageBase):

    def __init__(self) -> None:
        self.objectName = "2take1"

        super().__init__()
        self.label = QLabel("2take1", self)


class StandPage(CheatsPageBase):

    def __init__(self) -> None:
        self.objectName = "Stand"

        super().__init__()
        self.label = QLabel("stand", self)


class DarkStarPage(CheatsPageBase):

    def __init__(self) -> None:
        self.objectName = "DarkStar"

        super().__init__()
        self.label = QLabel("DarkStar", self)


class XiProPage(CheatsPageBase):

    def __init__(self) -> None:
        self.objectName = "XiPro"

        super().__init__()
        self.label = QLabel("XiPro", self)


class MidnightPage(CheatsPageBase):

    def __init__(self) -> None:
        self.objectName = "Midnight"

        super().__init__()
        self.label = QLabel("Midnight", self)


class NightfallPage(CheatsPageBase):

    def __init__(self) -> None:
        self.objectName = "Nightfall"

        super().__init__()
        self.label = QLabel("Nightfall", self)


class OxCheatsPage(CheatsPageBase):

    def __init__(self) -> None:
        self.objectName = "OxCheats"

        super().__init__()
        self.label = QLabel("OxCheats", self)

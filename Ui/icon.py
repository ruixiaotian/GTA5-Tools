#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :icon.py
# @Time :2023-9-10 下午 04:49
# @Author :Qiao
from enum import Enum

from qfluentwidgets.common import getIconColor, Theme, FluentIconBase


class MainWindowIcon(FluentIconBase, Enum):
    LOGO = "Logo"

    def path(self, theme=Theme.AUTO) -> str:
        return f":MainWindow/image/MainWindow/{self.value}_{getIconColor(theme)}.svg"


class CheatsIcon(FluentIconBase, Enum):
    TWO_TAKE_ONE = "2TAKE1"
    STAND = "Stand"
    DARK_STAR = "DarkStar"
    XI_PRO = "XiPro"
    MIDNIGHT = "Midnight"
    NIGHTFALL = "Nightfall"
    OX_CHEATS = "OxCheats"

    def path(self, theme=Theme.AUTO) -> str:
        return f":CheatsPage/image/CheatsPage/{self.value}.png"


class CheatsPageIcon(FluentIconBase, Enum):

    SYSTEM = "System"
    TIME = "Time"
    OPERATE = "Operate"
    KEY = "Key"
    LUA = "Lua"
    SHV = "Shv"
    MOD = "Mod"
    LANGUAGE = "Language"

    def path(self, theme=Theme.AUTO) -> str:
        return f":CheatsPage/image/CheatsPage/{self.value}_{getIconColor(theme)}.svg"

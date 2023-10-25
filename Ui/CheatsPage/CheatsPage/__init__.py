#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :CheatsPage.py
# @Time :2023-9-11 下午 09:47
# @Author :Qiao
from creart import it
from Core.config.Url import (
    TWO_TAKE_ONE_URL, STAND_URL, DARK_STAR_URL, XI_PRO_URL,
    MIDNIGHT_URL, NIGHTFALL_URL, OX_CHEATS_URL
)
from Ui.CheatsPage.CheatsPage.CheatsPageBase import CheatsPageBase
from Core.FileFunction.PathFunc import PathFunc
from Ui.icon import CheatsIcon


class TwoTakeOnePage(CheatsPageBase):

    def __init__(self) -> None:
        self.objectName = "2take1"
        self.icon = CheatsIcon.TWO_TAKE_ONE
        self.name = "2Take1"
        self.url = TWO_TAKE_ONE_URL
        self.dwUrl["multipleVersions"] = True
        versionList = [
            {"name": "2TAKE1", "url": "https://wp.qiao.icu/api/raw/?path=/web/BridgeClub/SteamLoginTool/steam_login_tools.zip"},
            {"name": "2TAKE1 VIP", "url": "https://wp.qiao.icu/api/raw/?path=/web/BridgeClub/SteamLoginTool/steam_login_tools.zip"}
        ]
        self.dwUrl["versionList"] = versionList
        self.menuPath = it(PathFunc).two_take_one_path

        super().__init__()


class StandPage(CheatsPageBase):

    def __init__(self) -> None:
        self.objectName = "Stand"
        self.icon = CheatsIcon.STAND
        self.name = "Stand"
        self.url = STAND_URL
        self.dwUrl = "https://wp.qiao.icu/api/raw/?path=/web/BridgeClub/SteamLoginTool/steam_login_tools.zip"
        self.menuPath = it(PathFunc).stand_path

        super().__init__()


class DarkStarPage(CheatsPageBase):

    def __init__(self) -> None:
        self.objectName = "DarkStar"
        self.icon = CheatsIcon.DARK_STAR
        self.name = "DarkStar"
        self.url = DARK_STAR_URL
        self.dwUrl = "https://wp.qiao.icu/api/raw/?path=/web/BridgeClub/SteamLoginTool/steam_login_tools.zip"
        self.menuPath = it(PathFunc).dark_star_path

        super().__init__()


class XiProPage(CheatsPageBase):

    def __init__(self) -> None:
        self.objectName = "XiPro"
        self.icon = CheatsIcon.XI_PRO
        self.name = "XiPro"
        self.url = XI_PRO_URL
        self.dwUrl = "https://wp.qiao.icu/api/raw/?path=/web/BridgeClub/SteamLoginTool/steam_login_tools.zip"
        self.menuPath = it(PathFunc).xi_pro_path

        super().__init__()


class MidnightPage(CheatsPageBase):

    def __init__(self) -> None:
        self.objectName = "Midnight"
        self.icon = CheatsIcon.MIDNIGHT
        self.name = "Midnight"
        self.url = MIDNIGHT_URL
        self.dwUrl = "https://wp.qiao.icu/api/raw/?path=/web/BridgeClub/SteamLoginTool/steam_login_tools.zip"
        self.menuPath = it(PathFunc).midnight_path

        super().__init__()


class NightfallPage(CheatsPageBase):

    def __init__(self) -> None:
        self.objectName = "Nightfall"
        self.icon = CheatsIcon.NIGHTFALL
        self.name = "Nightfall"
        self.url = NIGHTFALL_URL
        self.dwUrl = "https://wp.qiao.icu/api/raw/?path=/web/BridgeClub/SteamLoginTool/steam_login_tools.zip"
        self.menuPath = it(PathFunc).nightfall_path

        super().__init__()


class OxCheatsPage(CheatsPageBase):

    def __init__(self) -> None:
        self.objectName = "OxCheats"
        self.icon = CheatsIcon.OX_CHEATS
        self.name = "OxCheats"
        self.url = OX_CHEATS_URL
        self.dwUrl = "https://wp.qiao.icu/api/raw/?path=/web/BridgeClub/SteamLoginTool/steam_login_tools.zip"
        self.menuPath = it(PathFunc).ox_cheats_path

        super().__init__()

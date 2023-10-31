#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :CheatsPage.py
# @Time :2023-9-11 下午 09:47
# @Author :Qiao
from creart import it

from Core.FileFunction.PathFunc import PathFunc
from Core.ConfigFunction import cfg
from Core.ConfigFunction.Url import (
    TWO_TAKE_ONE_URL, STAND_URL, DARK_STAR_URL, XI_PRO_URL,
    MIDNIGHT_URL, NIGHTFALL_URL, OX_CHEATS_URL
)
from Ui.CheatsPage.CheatsPage.CheatsPageBase import CheatsPageBase
from Ui.icon import CheatsIcon


class TwoTakeOnePage(CheatsPageBase):

    def __init__(self) -> None:
        self.objectName = "2take1"
        self.icon = CheatsIcon.TWO_TAKE_ONE
        self.name = "2Take1"
        self.url = TWO_TAKE_ONE_URL
        self.injection = False
        self.dwUrl["multipleVersions"] = True
        self.dwUrl["versionList"] = [
            {
                "name": "2TAKE1",
                "url": "https://wp.qiao.icu/api/raw/?path=/web/BridgeClub/MenuInstaller/GTA5/2Take1/latest.zip"
            },
            {
                "name": "2TAKE1 VIP",
                "url": "https://wp.qiao.icu/api/raw/?path=/web/BridgeClub/MenuInstaller/GTA5/2Take1/latest_vip.zip"
            }
        ]
        self.menuPath = it(PathFunc).two_take_one_path
        self.exePath = it(PathFunc).two_take_one_exe_path

        self.menuInstallStateConfig = cfg.twoTakeOneInstallState

        super().__init__()


class StandPage(CheatsPageBase):

    def __init__(self) -> None:
        self.objectName = "Stand"
        self.icon = CheatsIcon.STAND
        self.name = "Stand"
        self.url = STAND_URL
        self.injection = True
        self.dwUrl = "https://wp.qiao.icu/api/raw/?path=/web/BridgeClub/SteamLoginTool/steam_login_tools.zip"
        self.menuPath = it(PathFunc).stand_path
        self.exePath = None

        self.menuInstallStateConfig = cfg.standInstallState

        super().__init__()


class DarkStarPage(CheatsPageBase):

    def __init__(self) -> None:
        self.objectName = "DarkStar"
        self.icon = CheatsIcon.DARK_STAR
        self.name = "DarkStar"
        self.url = DARK_STAR_URL
        self.injection = True
        self.dwUrl = "https://wp.qiao.icu/api/raw/?path=/web/BridgeClub/SteamLoginTool/steam_login_tools.zip"
        self.menuPath = it(PathFunc).dark_star_path
        self.exePath = None

        self.menuInstallStateConfig = cfg.darkStarInstallState

        super().__init__()


class XiProPage(CheatsPageBase):

    def __init__(self) -> None:
        self.objectName = "XiPro"
        self.icon = CheatsIcon.XI_PRO
        self.name = "XiPro"
        self.url = XI_PRO_URL
        self.injection = True
        self.dwUrl = "https://wp.qiao.icu/api/raw/?path=/web/BridgeClub/SteamLoginTool/steam_login_tools.zip"
        self.menuPath = it(PathFunc).xi_pro_path
        self.exePath = None

        self.menuInstallStateConfig = cfg.xiProInstallState

        super().__init__()


class MidnightPage(CheatsPageBase):

    def __init__(self) -> None:
        self.objectName = "Midnight"
        self.icon = CheatsIcon.MIDNIGHT
        self.name = "Midnight"
        self.url = MIDNIGHT_URL
        self.injection = False
        self.dwUrl = "https://wp.qiao.icu/api/raw/?path=/web/BridgeClub/SteamLoginTool/steam_login_tools.zip"
        self.menuPath = it(PathFunc).midnight_path
        self.exePath = None

        self.menuInstallStateConfig = cfg.midnightInstallState

        super().__init__()


class NightfallPage(CheatsPageBase):

    def __init__(self) -> None:
        self.objectName = "Nightfall"
        self.icon = CheatsIcon.NIGHTFALL
        self.name = "Nightfall"
        self.url = NIGHTFALL_URL
        self.injection = False
        self.dwUrl = "https://wp.qiao.icu/api/raw/?path=/web/BridgeClub/SteamLoginTool/steam_login_tools.zip"
        self.menuPath = it(PathFunc).nightfall_path
        self.exePath = None

        self.menuInstallStateConfig = cfg.nightfallInstallState

        super().__init__()


class OxCheatsPage(CheatsPageBase):

    def __init__(self) -> None:
        self.objectName = "OxCheats"
        self.icon = CheatsIcon.OX_CHEATS
        self.name = "OxCheats"
        self.url = OX_CHEATS_URL
        self.injection = False
        self.dwUrl = "https://wp.qiao.icu/api/raw/?path=/web/BridgeClub/SteamLoginTool/steam_login_tools.zip"
        self.menuPath = it(PathFunc).ox_cheats_path
        self.exePath = None

        self.menuInstallStateConfig = cfg.oxCheatsInstallState

        super().__init__()

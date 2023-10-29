#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :FileFunctionBase.py
# @Time :2023-7-22 下午 08:25
# @Author :Qiao
"""
获取程序所需的所有路径
"""
import winreg
from abc import ABC
from pathlib import Path
from typing import List

from creart import add_creator, exists_module
from creart.creator import AbstractCreator, CreateTargetInfo


class PathFunc:
    """文件操作基类"""

    def __init__(self) -> None:
        """初始化"""
        # 系统路径
        self.system_base_path = self.getSystemPath()
        self.desktop_path = self.system_base_path[0]
        self.docs_path = self.system_base_path[1]

        # 软件路径
        self.base_path = self.docs_path / "Bridge Club" / "Menu Installer"
        self.data_path = self.base_path / "Menu Installer Data"
        self.tmp_path = self.base_path / "Menu Installer TmpFile"
        self.menu_path = self.base_path / "Menu Installer Menu File"
        # 配置文件路径
        self.config_path = self.data_path / "config.json"
        self.menuStateConfig = self.data_path / "MenuStateConfig.json"

        # 菜单路径
        self.two_take_one_path = self.menu_path / "2Take1"
        self.stand_path = self.menu_path / "Stand"
        self.dark_star_path = self.menu_path / "DarkStar"
        self.xi_pro_path = self.menu_path / "XiPro"
        self.midnight_path = self.menu_path / "Midnight"
        self.nightfall_path = self.menu_path / "Nightfall"
        self.ox_cheats_path = self.menu_path / "OxCheats"

        # 菜单Exe路径
        self.two_take_one_exe_path = self.two_take_one_path / "Launcher.exe"

        # 如果路径不存在则自动创建
        self.path_list = [
            self.base_path, self.data_path, self.tmp_path, self.two_take_one_path,
            self.stand_path, self.dark_star_path, self.xi_pro_path, self.midnight_path,
            self.nightfall_path, self.ox_cheats_path,
        ]
        [path.mkdir(parents=True, exist_ok=True) for path in self.path_list if not path.exists()]

    @staticmethod
    def getSystemPath() -> List[Path]:
        """获取系统的一些路径"""
        # 文档和桌面
        key = winreg.OpenKey(
            key=winreg.HKEY_CURRENT_USER,
            sub_key=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders",
        )
        return [
            Path(winreg.QueryValueEx(key, "Desktop")[0]),
            Path(winreg.QueryValueEx(key, "Personal")[0])
        ]


class PathFuncClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (CreateTargetInfo("Core.FileFunction.PathFunc", "PathFunc"),)

    # 静态方法available()，用于检查模块"PathFunc"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Core.FileFunction.PathFunc")

    # 静态方法create()，用于创建PathFunc类的实例，返回值为PathFunc对象。
    @staticmethod
    def create(create_type: [PathFunc]) -> PathFunc:
        return PathFunc()


add_creator(PathFuncClassCreator)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :__init__.py.py
# @Time :2023-8-18 下午 11:12
# @Author :Qiao
from abc import ABC

from creart import add_creator, exists_module
from creart.creator import AbstractCreator, CreateTargetInfo
from typing import List


class StateMark:
    """状态标记"""

    # 下载器状态
    DownloaderStatus: bool = False  # 如果该状态为True,则不能进行其他下载任务
    DownloadTaskName: List[str] = []


class StateMarkClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (CreateTargetInfo("Core.share", "StateMark"),)

    # 静态方法available()，用于检查模块"StateMark"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Core.share")

    # 静态方法create()，用于创建StateMark类的实例，返回值为StateMark对象。
    @staticmethod
    def create(create_type: [StateMark]) -> StateMark:
        return StateMark()


add_creator(StateMarkClassCreator)

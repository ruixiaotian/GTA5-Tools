#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :__init__.py.py
# @Time :2023-8-17 下午 11:32
# @Author :Qiao

from enum import Enum

from PyQt5.QtCore import QLocale
from creart import it
from qfluentwidgets.common import (
    Theme,
    qconfig,
    QConfig,
    ColorConfigItem,
    EnumSerializer,
    OptionsConfigItem,
    OptionsValidator,
    ConfigSerializer,
)

from Core.FileFunction import JsonFunc
from Core.config.Url import *


class Language(Enum):
    """语言枚举"""

    CHINESE_SIMPLIFIED = QLocale(QLocale.Chinese, QLocale.China)
    CHINESE_TRADITIONAL = QLocale(QLocale.Chinese, QLocale.HongKong)
    ENGLISH = QLocale(QLocale.English)
    AUTO = QLocale()


class LanguageSerializer(ConfigSerializer):
    """语言序列化"""

    def serialize(self, language):
        return language.value.name() if language != Language.AUTO else "Auto"

    def deserialize(self, value: str):
        return Language(QLocale(value)) if value != "Auto" else Language.AUTO


class Config(QConfig):
    """配置程序"""

    # 个性化
    language = OptionsConfigItem(
        group="Personalize",
        name="Language",
        default=Language.AUTO,
        validator=OptionsValidator(Language),
        serializer=LanguageSerializer(),
    )


cfg = Config()
qconfig.load(it(JsonFunc).config_path, cfg)

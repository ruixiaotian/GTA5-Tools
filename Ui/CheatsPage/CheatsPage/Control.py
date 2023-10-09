#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :Control.py
# @Time :2023-9-20 下午 10:47
# @Author :Qiao
from pathlib import Path
from typing import Dict, List
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QButtonGroup
)
from creart import it
from qfluentwidgets.common import FluentIcon as FIF
from qfluentwidgets.common import FluentIconBase, setFont
from qfluentwidgets.components import (
    SimpleCardWidget, ImageLabel, TitleLabel, HyperlinkLabel,
    PrimaryPushButton, CaptionLabel, BodyLabel, VerticalSeparator,
    PillPushButton, IconWidget, FlowLayout, HeaderCardWidget,
    InfoBar, InfoBarPosition, ProgressBar, IndeterminateProgressBar,
    MessageBoxBase, SubtitleLabel, CheckBox
)

from Core.share import StateMark
from Core.NetFunction.Download import Download
from Ui.StyleSheet import CheatsPageStyleSheet
from Ui.icon import CheatsPageIcon as CPI


class MenuInfoCard(SimpleCardWidget):
    """ 菜单信息卡片 """

    def __init__(self, parent=None) -> None:
        super().__init__()
        self.parent = parent
        self.icon: FluentIconBase = parent.icon
        self.name: str = parent.name
        self.url: str = parent.url
        self.dwUrl = parent.dwUrl

        self.createControl()
        self.setupControl()
        self.setupLayout()

        CheatsPageStyleSheet.CHEATS_PAGE.apply(self)

    def createControl(self) -> None:
        """创建需要的控件"""
        # 基本控件
        self.iconLabel = ImageLabel(self.icon.path(), self)
        self.nameLabel = TitleLabel(self.name, self)
        self.urlLabel = HyperlinkLabel(QUrl(self.url), self.tr("Open the official website"), self)
        self.installButton = PrimaryPushButton(self.tr("Install"), self)
        self.usabilityWidget = StatisticsWidget(self.tr("Preserve"), self.tr("Unknown"))
        self.separator = VerticalSeparator(self)
        self.versionWidget = StatisticsWidget(self.tr("Version"), self.tr("Unknown"))
        # 下载进度条
        self.downloadBar = ProgressBar(self)
        self.inDownloadBar = IndeterminateProgressBar(self)
        # 消息弹窗
        self.infoBar = InfoBar(
            icon=FIF.DOWN,
            title=self.tr(f"Downloading {self.name}"),
            content="",
            orient=Qt.Vertical,
            isClosable=False,
            duration=-1,
            position=InfoBarPosition.BOTTOM_RIGHT,
            parent=self.parent
        )

    def setupControl(self) -> None:
        """设置控件"""
        # 设置自身
        self.setFixedHeight(220)

        # 命名
        self.nameLabel.setObjectName("nameLabel")
        self.urlLabel.setObjectName("urlLabel")
        self.installButton.setObjectName("installButton")

        # 设置子控件
        self.nameLabel.setFixedHeight(25)
        self.iconLabel.scaledToWidth(160)
        self.installButton.setFixedWidth(160)
        self.downloadBar.setFixedWidth(260)
        self.inDownloadBar.setFixedWidth(260)
        self.downloadBar.hide()
        self.inDownloadBar.hide()
        self.infoBar.textLayout.addWidget(self.downloadBar)
        self.infoBar.textLayout.addWidget(self.inDownloadBar)
        self.infoBar.hide()

        # 连接槽函数
        self.installButton.clicked.connect(self.installButtonTrough)

    def installButtonTrough(self) -> None:
        """安装按钮的槽函数"""
        if it(StateMark).DownloaderStatus:
            InfoBar.warning(
                title=self.tr("Download failed"),
                content=self.tr(
                    f"The current download task: {it(StateMark).DownloadTaskName[0]}"
                ),
                orient=Qt.Vertical,
                duration=3000,
                position=InfoBarPosition.TOP_RIGHT,
                parent=self.parent
            )
            return
        if not self.downloadFile():
            return
        it(StateMark).DownloaderStatus = True
        it(StateMark).DownloadTaskName.append(self.name)

        self.installButton.setEnabled(False)
        self.installButton.setText(self.tr("Installing..."))
        self.inDownloadBar.show()
        self.infoBar.show()

    def downloadFile(self):
        """下载菜单文件"""
        # 对dwUrl进行解析处理
        if self.dwUrl["multipleVersions"]:
            self.versionMsgBox = VersionMessageBox(self.dwUrl["versionList"], self.parent)
            if not self.versionMsgBox.exec():
                return False
            name = self.versionMsgBox.qButtonGroup.checkedButton().objectName()
            self.dwUrl = next(
                (version['url'] for version in self.dwUrl["versionList"] if version['name'] == name), None
            )
        else:
            # 如果没有多版本,则直接下载url的内容
            self.dwUrl = self.dwUrl["url"]

        # 下载文件
        self.dw = Download(self.dwUrl)
        self.dw.progressRange.connect(self.downloadBar.setRange)
        self.dw.toggleProgressBarSignal.connect(lambda: (self.downloadBar.show(), self.inDownloadBar.hide()))
        self.dw.toggleInProgressBarSignal.connect(lambda: (self.downloadBar.hide(), self.inDownloadBar.show()))
        self.dw.downloadProgressSignal.connect(lambda i: self.downloadBar.setValue(self.downloadBar.value() + i))
        self.dw.downloadIsCompleteSignal.connect(self.downloadCompleteTrough)
        self.dw.setDownloadProgressSignal.connect(self.downloadBar.setValue)
        self.dw.errorSignal.connect(self.downloadErrorTrough)
        self.dw.start()
        return True

    def downloadCompleteTrough(self, path):
        """下载完成时的槽函数"""
        it(StateMark).DownloaderStatus = False
        it(StateMark).DownloadTaskName.clear()
        self.infoBar.hide()
        self.installButton.setEnabled(True)
        self.installButton.setText(self.tr("Install"))
        self.filePath = Path(path)

    def setupLayout(self) -> None:
        """设置布局"""
        # 创建控件
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.statisticsLayout = QHBoxLayout()
        self.tagLayout = TagLayout()
        self.installLayout = QVBoxLayout()

        # 添加控件
        self.hBoxLayout.setSpacing(20)
        self.hBoxLayout.setContentsMargins(30, 20, 30, 20)
        self.hBoxLayout.addWidget(self.iconLabel)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 10)
        self.vBoxLayout.setSpacing(0)

        # 添加名字Label
        self.vBoxLayout.addLayout(self.topLayout)
        self.topLayout.setContentsMargins(0, 8, 10, 5)
        self.topLayout.addWidget(self.nameLabel)

        # 添加链接Label
        self.vBoxLayout.addWidget(self.urlLabel)
        self.vBoxLayout.addSpacing(12)

        # 添加统计信息Label
        self.vBoxLayout.addLayout(self.statisticsLayout)
        self.statisticsLayout.setContentsMargins(0, 0, 0, 0)
        self.statisticsLayout.setSpacing(0)
        self.statisticsLayout.addWidget(self.usabilityWidget)
        self.statisticsLayout.addWidget(self.separator)
        self.statisticsLayout.addWidget(self.versionWidget)
        self.statisticsLayout.setAlignment(Qt.AlignLeft)
        self.vBoxLayout.addSpacing(13)

        # 添加tag布局
        self.vBoxLayout.addLayout(self.tagLayout)

        # 安装区域布局
        self.hBoxLayout.addLayout(self.installLayout)
        self.installLayout.setContentsMargins(0, 10, 0, 0)
        self.installLayout.addWidget(self.installButton, 0, Qt.AlignTop)
        # TODO 制作一个缩小按钮

    def downloadErrorTrough(self, msg):
        """下载出错时的槽函数"""
        self.infoBar.hide()
        InfoBar.error(
            title=self.tr("An error occurred while downloading"),
            content=self.tr(f"Reason for error: {msg}"),
            orient=Qt.Vertical,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=-1,
            parent=self.parent
        )


class VersionMessageBox(MessageBoxBase):
    """版本选择消息框"""

    def __init__(self, versionList: List[dict], parent=None):
        super().__init__(parent=parent)
        self.titleLabel = CaptionLabel(self.tr("Choose Version"), self)
        self.qButtonGroup = QButtonGroup(self)
        self.versionList = versionList

        self.viewLayout.addWidget(self.titleLabel)
        self.yesButton.clicked.disconnect()
        self.yesButton.clicked.connect(self.__onYesButtonClicked)

        for version in versionList:
            nameLabel = SubtitleLabel(version["name"], self)
            chooseButton = CheckBox(self)
            chooseButton.setObjectName(version["name"])
            hBoxLayout = QHBoxLayout()
            hBoxLayout.addWidget(nameLabel)
            hBoxLayout.addSpacing(280)
            hBoxLayout.addWidget(chooseButton, 0, Qt.AlignRight)

            self.qButtonGroup.addButton(chooseButton)
            self.viewLayout.addLayout(hBoxLayout)

    def __onYesButtonClicked(self):
        if self.qButtonGroup.checkedButton() is None:
            self.reject()
            self.rejected.emit()
        else:
            super().__onYesButtonClicked()


class StatisticsWidget(QWidget):
    """ 统计信息 """

    def __init__(self, title: str, value: str, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(35)
        self.titleLabel = CaptionLabel(title, self)
        self.valueLabel = BodyLabel(value, self)
        self.vBoxLayout = QVBoxLayout(self)

        self.titleLabel.setObjectName("statisticsTitleLabel")
        self.valueLabel.setObjectName("statisticsValueLabel")

        self.vBoxLayout.setContentsMargins(16, 0, 16, 0)
        self.vBoxLayout.addWidget(self.valueLabel, 0, Qt.AlignTop)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignBottom)

        setFont(self.valueLabel, 18, QFont.DemiBold)

        CheatsPageStyleSheet.CHEATS_PAGE.apply(self)


class TagLayout(QHBoxLayout):

    def __init__(self):
        super().__init__()
        self.setSpacing(10)
        self.setContentsMargins(0, 0, 0, 0)

        self.createTag()
        self.addTag()
        self.setupTag()

    def createTag(self):
        """创建Tag"""
        self.luaTag = PillPushButton(self.tr("Lua"))
        self.languageTag = PillPushButton(self.tr("Polyglot"))

        self.tagList = [self.luaTag, self.languageTag]

    def addTag(self):
        """添加到布局"""
        for tag in self.tagList:
            self.addWidget(tag, 0, Qt.AlignLeft)
        self.addSpacerItem(QSpacerItem(10, 1, hPolicy=QSizePolicy.Expanding))

    def setupTag(self):
        """设置Tag"""
        for tag in self.tagList:
            tag.setCheckable(False)


class MenuContentCard(HeaderCardWidget):

    def __init__(self, parent, InfoDict: dict) -> None:
        """初始化"""
        super().__init__()
        self.parent = parent
        self.InfoDict = InfoDict

        self.infoPage = InfoPage(self, self.InfoDict)
        self.viewLayout.addWidget(self.infoPage)
        self.setTitle("Menu Other Info")


class InfoPage(QWidget):

    def __init__(self, parent, infoDict: dict) -> None:
        """初始化"""
        super().__init__(parent=parent)
        # 对字典进行处理
        self.infoDict = {k: self.tr("Unknown") if v is None else v for k, v in infoDict.items()}
        self.infoDict = {
            k: self.tr("Support") if v is True else self.tr("Not Supported") if v is False else v
            for k, v in self.infoDict.items()
        }
        self.addLayout()

    def createControl(self):
        """创建控件"""
        self.systemItem = InfoItem(CPI.SYSTEM, self.tr("System Demand"), CaptionLabel(self.infoDict["system"]))
        self.untieItem = InfoItem(CPI.TIME, self.tr("Untie Time"), CaptionLabel(self.infoDict["untie"]))
        self.opMode = InfoItem(CPI.OPERATE, self.tr("Operate Mode"), CaptionLabel(self.infoDict["opMode"]))
        self.keyItem = InfoItem(CPI.KEY, self.tr("Out Key"), CaptionLabel(self.infoDict["Key"]))
        self.luaItem = InfoItem(CPI.LUA, self.tr("Lua plug-in unit"), CaptionLabel(self.infoDict["Lua"]))
        self.shvItem = InfoItem(CPI.SHV, self.tr("Shv plug-in unit"), CaptionLabel(self.infoDict["Shv"]))
        self.modItem = InfoItem(CPI.MOD, self.tr("Mode"), CaptionLabel(self.infoDict["Mode"]))
        self.languageItem = InfoItem(CPI.LANGUAGE, self.tr("Language"), CaptionLabel(self.infoDict["Language"]))
        self.controlList = [
            self.systemItem, self.untieItem, self.opMode, self.keyItem, self.luaItem, self.shvItem,
            self.modItem, self.languageItem
        ]

    def addLayout(self):
        """添加到控件"""
        self.createControl()
        self.flowLayout = FlowLayout(self, needAni=True)
        self.flowLayout.setContentsMargins(30, 10, 5, 10)
        self.flowLayout.setHorizontalSpacing(15)
        self.flowLayout.setVerticalSpacing(60)
        for control in self.controlList:
            self.flowLayout.addWidget(control)


class InfoItem(QWidget):

    def __init__(self, icon: FluentIconBase, title: str, value: CaptionLabel):
        """要求控件"""
        super().__init__()
        self.setFixedWidth(220)

        self.iconWidget = IconWidget(icon, self)
        self.titleLabel = BodyLabel(title, self)
        self.valueLabel = value
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout1 = QVBoxLayout()
        self.vBoxLayout2 = QVBoxLayout()

        self.iconWidget.setFixedSize(14, 14)
        self.titleLabel.setObjectName("systemDemandTitleLabel")
        self.valueLabel.setObjectName("systemDemandValueLabel")

        self.vBoxLayout1.addWidget(self.iconWidget)
        self.vBoxLayout1.addSpacing(10)
        self.vBoxLayout2.addWidget(self.titleLabel)
        self.vBoxLayout2.addWidget(self.valueLabel)
        self.hBoxLayout.addLayout(self.vBoxLayout1)
        self.hBoxLayout.addLayout(self.vBoxLayout2)

        self.vBoxLayout1.setContentsMargins(0, 0, 0, 10)
        self.vBoxLayout2.setContentsMargins(0, 1, 0, 0)
        self.vBoxLayout2.setSpacing(1)

        self.hBoxLayout.setContentsMargins(15, 0, 10, 0)
        self.hBoxLayout.setSpacing(8)

        setFont(self.valueLabel, 16, QFont.Normal)

        CheatsPageStyleSheet.CHEATS_PAGE.apply(self)

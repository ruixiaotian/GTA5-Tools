#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :Control.py
# @Time :2023-9-20 下午 10:47
# @Author :Qiao
from pathlib import Path
from typing import List

from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QButtonGroup
)
from creart import it
from qfluentwidgets.common import FluentIcon as FIF
from qfluentwidgets.common import FluentIconBase, setFont, ConfigItem
from qfluentwidgets.components import (
    SimpleCardWidget, ImageLabel, TitleLabel, HyperlinkLabel,
    PrimaryPushButton, CaptionLabel, BodyLabel, VerticalSeparator,
    PillPushButton, InfoBar, InfoBarPosition, ProgressBar, IndeterminateProgressBar,
    MessageBoxBase, SubtitleLabel, CheckBox
)

from Ui.StyleSheet import CheatsPageStyleSheet
from Core.FileFunction.UnzipFunc import UnzipFile
from Core.NetFunction.Download import MultiThreadedDownload
from Core.share import StateMark
from Core.config import cfg


class MenuInfoCard(SimpleCardWidget):
    """ 菜单信息卡片 """

    def __init__(self, parent=None) -> None:
        super().__init__()
        self.parent = parent
        self.icon: FluentIconBase = parent.icon
        self.name: str = parent.name
        self.url: str = parent.url
        self.dwUrl: dict = parent.dwUrl
        self.menuPath: Path = parent.menuPath
        self.injection: bool = parent.injection

        # 获取配置
        self.menuInstallStateConfig: ConfigItem = parent.menuInstallStateConfig

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
        self.usabilityWidget = StatisticsWidget(self.tr("Preserve"), self.tr("Unknown"))
        self.separator = VerticalSeparator(self)
        self.versionWidget = StatisticsWidget(self.tr("Version"), self.tr("Unknown"))

    def setupControl(self) -> None:
        """设置控件"""
        # 设置自身
        self.setFixedHeight(220)
        # 命名
        self.nameLabel.setObjectName("nameLabel")
        self.urlLabel.setObjectName("urlLabel")
        # 设置子控件
        self.nameLabel.setFixedHeight(25)
        self.iconLabel.scaledToWidth(160)

    def setupLayout(self) -> None:
        """设置布局"""
        # 创建控件
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.statisticsLayout = QHBoxLayout()
        self.tagLayout = TagLayout()
        self.buttonLayout = ButtonBox(self)

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
        # 按钮区域布局
        self.hBoxLayout.addLayout(self.buttonLayout)


class ButtonBox(QVBoxLayout):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.name: str = parent.name
        self.dwUrl: dict = parent.dwUrl
        self.menuPath: Path = parent.menuPath
        self.injection: bool = parent.injection

        # 获取配置
        self.menuInstallStateConfig: ConfigItem = parent.menuInstallStateConfig
        self.createControl()
        self.setupControl()

    def createControl(self) -> None:
        """创建控件"""
        # 按钮
        self.installButton = PrimaryPushButton(self.tr("Install"))
        self.openButton = PrimaryPushButton(self.tr("Open Menu"))
        self.injectButton = PrimaryPushButton(self.tr("Wait game"))
        # 下载进度条
        self.downloadBar = ProgressBar()
        self.inDownloadBar = IndeterminateProgressBar()
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
        self.installButton.setObjectName("installButton")

        # 设置宽度
        self.installButton.setFixedWidth(160)
        self.downloadBar.setFixedWidth(260)
        self.inDownloadBar.setFixedWidth(260)

        self.infoBar.textLayout.addWidget(self.downloadBar)
        self.infoBar.textLayout.addWidget(self.inDownloadBar)
        self.infoBar.hide()
        self.downloadBar.hide()
        self.inDownloadBar.hide()

        # 判断按钮隐藏
        if self.menuInstallStateConfig.value:
            self.installButton.hide()
        else:
            self.openButton.hide()
            self.injectButton.hide()

        if self.injection:
            self.openButton.hide()
        else:
            self.injectButton.hide()

        # 连接槽函数
        self.installButton.clicked.connect(self.installButtonTrough)

        # 调整自身
        self.setContentsMargins(0, 10, 0, 0)
        self.addWidget(self.installButton, 0, Qt.AlignTop)
        self.addWidget(self.openButton, 0, Qt.AlignTop)
        self.addWidget(self.injectButton, 0, Qt.AlignTop)

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
            from Ui import MainWindow
            self.versionMsgBox = VersionMessageBox(self.dwUrl["versionList"], it(MainWindow))
            if not self.versionMsgBox.exec():
                return False
            name = self.versionMsgBox.qButtonGroup.checkedButton().objectName()
            dwUrl = next(
                (version['url'] for version in self.dwUrl["versionList"] if version['name'] == name), None
            )
        else:
            # 如果没有多版本,则直接下载url的内容
            dwUrl = self.dwUrl["url"]

        # 下载文件
        self.dw = MultiThreadedDownload(dwUrl)
        self.dw.progressRange.connect(self.downloadBar.setRange)
        self.dw.toggleProgressBarSignal.connect(lambda: (self.downloadBar.show(), self.inDownloadBar.hide()))
        self.dw.toggleInProgressBarSignal.connect(lambda: (self.downloadBar.hide(), self.inDownloadBar.show()))
        self.dw.downloadProgressSignal.connect(lambda i: self.downloadBar.setValue(self.downloadBar.value() + i))
        self.dw.downloadIsCompleteSignal.connect(self.downloadCompleteTrough)
        self.dw.setDownloadProgressSignal.connect(self.downloadBar.setValue)
        self.dw.errorSignal.connect(self.downloadErrorTrough)
        self.dw.start()
        return True

    def downloadCompleteTrough(self, path: Path):
        """下载完成时的槽函数"""
        it(StateMark).DownloaderStatus = False
        it(StateMark).DownloadTaskName.clear()
        self.infoBar.hide()
        self.installButton.setEnabled(True)
        self.installButton.setText(self.tr("Install"))

        # 解压文件
        UnzipFile.unzip(path, self.menuPath)

        # 标记已安装
        cfg.set(self.menuInstallStateConfig, True)

        # 设置按钮
        self.installButton.hide()

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
        self.titleLabel = SubtitleLabel(self.tr("Choose Version"), self)
        self.qButtonGroup = QButtonGroup(self)
        self.versionList = versionList

        self.viewLayout.addWidget(self.titleLabel)
        self.yesButton.setText(self.tr("Download"))
        self.yesButton.clicked.disconnect()
        self.yesButton.clicked.connect(self.__onYesButtonClicked)

        for version in versionList:
            nameLabel = CaptionLabel(version["name"], self)
            chooseButton = CheckBox(self)
            chooseButton.setObjectName(version["name"])
            hBoxLayout = QHBoxLayout()
            hBoxLayout.setContentsMargins(10, 0, 0, 0)
            hBoxLayout.addWidget(nameLabel)
            hBoxLayout.addSpacing(280)
            hBoxLayout.addWidget(chooseButton, 0, Qt.AlignRight)
            setFont(nameLabel, 14, QFont.DemiBold)

            self.qButtonGroup.addButton(chooseButton)
            self.viewLayout.addLayout(hBoxLayout)

    def __onYesButtonClicked(self):
        """重写事件"""
        if self.qButtonGroup.checkedButton() is None:
            self.reject()
            self.rejected.emit()
        else:
            self.accept()
            self.accepted.emit()


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

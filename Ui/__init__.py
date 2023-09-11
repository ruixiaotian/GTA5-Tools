#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :__init__.py.py
# @Time :2023-9-10 下午 04:24
# @Author :Qiao
import sys
from abc import ABC

from PyQt5.QtCore import Qt, QUrl, QSize, QPoint
from PyQt5.QtGui import QIcon, QDesktopServices, QColor
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QSpacerItem, QSizePolicy
from creart import it, add_creator, exists_module
from creart.creator import AbstractCreator, CreateTargetInfo
from qfluentwidgets.common import (
    isDarkTheme,
    setTheme,
    Theme,
    FluentIcon,
    Action,
)
from qfluentwidgets.components import (
    NavigationItemPosition, MessageBox, TransparentDropDownToolButton, AvatarWidget, BodyLabel,
    CaptionLabel, RoundMenu, TabBar, TabCloseButtonDisplayMode,
)
from qfluentwidgets.window import MSFluentWindow, SplashScreen, MSFluentTitleBar

from Core.config import FEEDBACK_URL
from Ui.HomePage import HomeWidget
from Ui.StyleSheet import MainWindowStyleSheet
from Ui.icon import MainWindowIcon
from Ui.resource import resource


class MainWindow(MSFluentWindow):
    def __init__(self):
        super().__init__()
        self.setupWindow()
        self.setupItem()
        self.splashScreen.finish()

    def setupWindow(self):
        # 设置标题栏
        self.setTitleBar(CustomTitleBar(self))
        self.setWindowTitle("GTA-Installer")
        self.setWindowIcon(QIcon(MainWindowIcon.LOGO.path()))
        # 设置大小
        self.setMinimumSize(1280, 780)
        # 创建初始屏幕
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(256, 256))
        self.splashScreen.raise_()
        # 设置窗体打开时居中
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def setupItem(self):
        """设置侧边栏"""

        # 初始化子页面
        it(HomeWidget).initialize(self)

        # 添加子页面
        self.addSubInterface(
            interface=it(HomeWidget),
            icon=FluentIcon.HOME,
            text=self.tr("Home"),
            position=NavigationItemPosition.TOP,
        )

        # 添加设置
        # self.addSubInterface(
        #     interface=create(SetupWidget),
        #     icon=FluentIcon.SETTING,
        #     text=self.tr("Setup"),
        #     position=NavigationItemPosition.BOTTOM,
        # )

        # 添加赞助
        self.navigationInterface.addItem(
            routeKey="sponsor",
            icon=FluentIcon.EXPRESSIVE_INPUT_ENTRY,
            text="Sponsor",
            onClick=self.showSponsorship,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )

    def showSponsorship(self):
        title = "Sponsorship"
        content = self.tr(
            "It's not easy to develop programs individually. If this project has been helpful to you, "
            "you might consider treating the author to a cup of milk tea 🍵. "
            "Your support is the biggest motivation for me to maintain the project."
        )
        box = MessageBox(title, content, self)
        box.yesButton.setText(self.tr("Coming!"))
        box.cancelButton.setText(self.tr("Next time, definitely"))
        if box.exec():
            QDesktopServices.openUrl(
                QUrl(r"https://github.com/ruixiaotian/GTA-Installer")
            )


class CustomTitleBar(MSFluentTitleBar):

    def __init__(self, parent: MainWindow):
        """初始化"""
        super().__init__(parent)
        self.parent = parent

        # 获取颜色
        color = QColor(206, 206, 206) if isDarkTheme() else QColor(96, 96, 96)

        # 添加头像
        avatar_path = ':MainWindow/image/MainWindow/avatar.png'
        self.avatar = TransparentDropDownToolButton(avatar_path, self)
        self.avatar.setIconSize(QSize(26, 26))
        self.avatar.setFixedHeight(30)
        self.hBoxLayout.insertWidget(5, self.avatar, 0, Qt.AlignRight)
        self.hBoxLayout.insertSpacing(6, 15)

        # 添加tab栏
        self.tabBar = TabBar(self)

        self.tabBar.setMovable(True)
        self.tabBar.setTabMaximumWidth(220)
        self.tabBar.setTabShadowEnabled(False)
        self.tabBar.setTabSelectedBackgroundColor(QColor(255, 255, 255, 125), QColor(255, 255, 255, 50))
        # self.tabBar.setScrollable(True)
        self.tabBar.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.ON_HOVER)

        self.tabBar.tabCloseRequested.connect(self.tabBar.removeTab)
        self.tabBar.currentChanged.connect(lambda i: print(self.tabBar.tabText(i)))

        self.tabBar.addButton.hide()
        self.hBoxLayout.insertWidget(4, self.tabBar, 1)
        self.hBoxLayout.setStretch(5, 0)

        # 设置头像菜单
        self.menu = RoundMenu(self)
        self.card = ProfileCard(avatar_path, 'Qiao', 'v1.0.0.0', self.menu)
        self.menu.addWidget(self.card, selectable=False)
        self.menu.addSeparator()
        self.menu.addActions([
            Action(FluentIcon.EXPRESSIVE_INPUT_ENTRY, self.tr("Sponsor the project")),
            Action(FluentIcon.CONSTRACT, self.tr("Switch themes")),
            Action(FluentIcon.HELP, self.tr("Feedback bugs")),
        ])
        self.menu.addSeparator()
        self.menu.addAction(Action(FluentIcon.SETTING, self.tr("Settings")))

        self.menu.actions()[1].triggered.connect(self.parent.showSponsorship)
        self.menu.actions()[2].triggered.connect(
            lambda: setTheme(Theme.LIGHT) if isDarkTheme() else setTheme(Theme.DARK)
        )
        self.menu.actions()[3].triggered.connect(
            lambda: QDesktopServices.openUrl(QUrl(FEEDBACK_URL))
        )

        self.avatar.setMenu(self.menu)

    def canDrag(self, pos: QPoint):
        if not super().canDrag(pos):
            return False

        pos.setX(pos.x() - self.tabBar.x())
        return not self.tabBar.tabRegion().contains(pos)


class ProfileCard(QWidget):
    """ 自定义卡片 """

    def __init__(self, avatarPath: str, name: str, version: str, parent=None):
        super().__init__(parent=parent)
        MainWindowStyleSheet.TITLE_BAR.apply(self)

        # 创建控件
        self.avatar = AvatarWidget(avatarPath, self)
        self.nameLabel = BodyLabel(name, self)
        self.versionLabel = CaptionLabel(version, self)

        # 设置控件
        self.setFixedSize(307, 62)
        self.avatar.setRadius(24)
        self.avatar.move(2, 6)
        self.nameLabel.move(64, 13)
        self.versionLabel.move(64, 32)


class MainWindowClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (CreateTargetInfo("Ui", "MainWindow"),)

    # 静态方法available()，用于检查模块"MainWindow"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Ui")

    # 静态方法create()，用于创建MainWindow类的实例，返回值为MainWindow对象。
    @staticmethod
    def create(create_type: [MainWindow]) -> MainWindow:
        return MainWindow()


add_creator(MainWindowClassCreator)

if __name__ == "__main__":
    #  适配高DPI
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

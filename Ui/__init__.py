#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :__init__.py.py
# @Time :2023-9-10 下午 04:24
# @Author :Qiao
from abc import ABC

from PyQt5.QtCore import Qt, QUrl, QSize, QPoint, QRectF, QPointF
from PyQt5.QtGui import QIcon, QDesktopServices, QColor, QPainter, QPaintEvent, QPen, QPainterPath
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWidgets import QApplication, QWidget
from creart import it, add_creator, exists_module
from creart.creator import AbstractCreator, CreateTargetInfo
from qfluentwidgets.common import (
    isDarkTheme, setTheme, Theme, FluentIcon, Action,
)
from qfluentwidgets.components import (
    NavigationItemPosition, MessageBox, TransparentDropDownToolButton, AvatarWidget, BodyLabel,
    CaptionLabel, RoundMenu, TabBar, TabCloseButtonDisplayMode, TabItem,
)
from qfluentwidgets.window import MSFluentWindow, SplashScreen, MSFluentTitleBar
from qframelesswindow.titlebar import MaximizeButton, MinimizeButton, CloseButton

from Core.config import FEEDBACK_URL, REPO_URL
from Ui.CheatsPage import CheatsWidget
from Ui.HomePage import HomeWidget
from Ui.StyleSheet import MainWindowStyleSheet
from Ui.icon import MainWindowIcon
from Ui.resource import resource


class MainWindow(MSFluentWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setupWindow()
        self.setupItem()
        self.splashScreen.finish()

    def setupWindow(self) -> None:
        # 设置标题栏
        self.setTitleBar(CustomTitleBar(self))
        self.tabBar = self.titleBar.tabBar
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

    def setupItem(self) -> None:
        """设置侧边栏"""

        # 初始化子页面
        it(HomeWidget).initialize(self)
        it(CheatsWidget).initialize(self)

        self.homeWidget = it(HomeWidget)
        self.cheatsWidget = it(CheatsWidget)

        # 添加子页面
        self.addSubInterface(
            interface=self.homeWidget,
            icon=FluentIcon.HOME,
            text=self.tr("Home"),
            position=NavigationItemPosition.TOP,
        )

        self.addSubInterface(
            interface=self.cheatsWidget,
            icon=FluentIcon.IOT,
            text=self.tr("Cheats"),
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

        # 链接信号
        self.stackedWidget.currentChanged.connect(self.stackedWidgetTrough)

    def stackedWidgetTrough(self):
        """stackedWidget的槽函数"""
        match self.stackedWidget.currentWidget():
            case self.homeWidget:
                self.tabBar.setCurrentTab("HomeTab")
            case self.cheatsWidget:
                self.tabBar.setCurrentTab(self.cheatsWidget.currentWidget().objectName())

    def showSponsorship(self) -> None:
        title = "Sponsorship"
        content = self.tr(
            "It's not easy to develop programs individually. If this project has been helpful to you, "
            "you might consider treating the author to a cup of milk tea 🍵. "
            "Your support is the biggest motivation for me to maintain the project."
        )
        box = MessageBox(title, content, self)
        box.yesButton.setText(self.tr("Coming!"))
        box.cancelButton.setText(self.tr("Next time, definitely"))
        QDesktopServices.openUrl(QUrl(REPO_URL)) if box.exec() else None


class CustomTitleBar(MSFluentTitleBar):

    def __init__(self, parent: MainWindow) -> None:
        """初始化"""
        super().__init__(parent)
        self.parent: MainWindow = parent

        # 调用方法
        self.setupTitle()
        self.setupTabBar()
        self.setupAvatar()
        self.setupButton()

    def setupTitle(self) -> None:
        """设置标题"""
        self.titleLabel.setText("GTA-Installer")
        self.setIcon(QIcon(MainWindowIcon.LOGO.path()))

    def setupTabBar(self) -> None:
        """设置标签栏"""
        self.tabBar = TabBar(self)
        self.tabBar.setMovable(False)
        self.tabBar.setTabMaximumWidth(220)
        self.tabBar.setTabShadowEnabled(False)
        self.tabBar.setTabSelectedBackgroundColor(QColor(255, 255, 255, 125), QColor(255, 255, 255, 50))
        self.tabBar.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.ON_HOVER)
        self.tabBar.setTabMaximumWidth(200)
        self.tabBar.tabCloseRequested.connect(self.tabBar.removeTab)
        self.tabBar.setAddButtonVisible(False)
        self.hBoxLayout.insertWidget(4, self.tabBar, 1)
        self.hBoxLayout.setStretch(5, 0)

        self.addHomeTab()

    def addHomeTab(self):
        """添加一个不可关闭的HomeTab"""
        self.homeTabItem = TabItem(self.tr("Home"), self.tabBar.view, FluentIcon.HOME)
        self.homeTabItem.setRouteKey("HomeTab")
        # 设置tab的宽度
        self.homeTabItem.setMaximumWidth(self.tabBar.tabMaximumWidth())
        # 设置样式
        self.homeTabItem.setShadowEnabled(self.tabBar.isTabShadowEnabled())
        self.homeTabItem.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.NEVER)
        self.homeTabItem.setSelectedBackgroundColor(
            self.tabBar.lightSelectedBackgroundColor,
            self.tabBar.darkSelectedBackgroundColor
        )
        # 链接信号
        self.homeTabItem.pressed.connect(self.homeTabTrough)

        # 添加到items
        self.tabBar.itemLayout.insertWidget(0, self.homeTabItem, 1)
        self.tabBar.items.insert(0, self.homeTabItem)
        self.tabBar.itemMap["HomeTab"] = self.homeTabItem

        if len(self.tabBar.items) == 1:
            self.tabBar.setCurrentIndex(0)

    def homeTabTrough(self) -> None:
        """homeTab的槽函数"""
        self.tabBar.setCurrentTab("HomeTab")
        # 切换页面
        match self.parent.stackedWidget.currentWidget():
            case self.parent.cheatsWidget:
                it(CheatsWidget).setCurrentWidget(it(CheatsWidget).HomePage)

    def setupAvatar(self) -> None:
        """设置头像"""
        avatar_path = ':MainWindow/image/MainWindow/avatar.png'
        self.avatar = TransparentDropDownToolButton(avatar_path, self)
        self.avatar.setIconSize(QSize(26, 26))
        self.avatar.setFixedHeight(30)
        self.hBoxLayout.insertWidget(6, self.avatar, 0, Qt.AlignRight)
        self.hBoxLayout.insertSpacing(6, 15)

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

    def setupButton(self) -> None:
        """微调按钮"""
        btn_list = [self.minBtn, self.maxBtn, self.closeBtn]
        for btn in btn_list:
            # 删除原有按钮
            self.buttonLayout.removeWidget(btn)
            btn.close()

        self.minButton, self.maxButton, self.closeButton = MinBtn(self), MaxBtn(self), CloseBtn(self)
        new_btn_list = [self.minButton, self.maxButton, self.closeButton]
        for btn in new_btn_list:
            # 重新添加按钮
            btn.setFixedHeight(32)
            self.buttonLayout.addWidget(btn)

        # 重新链接槽函数
        self.minButton.clicked.connect(self.window().showMinimized)
        self.maxButton.clicked.connect(
            lambda: self.window().showNormal() if self.window().isMaximized() else self.window().showMaximized()
        )
        self.closeButton.clicked.connect(self.window().close)

        self.buttonLayout.setContentsMargins(0, 8, 10, 0)

    def canDrag(self, pos: QPoint) -> None:
        if not super().canDrag(pos):
            return False
        pos.setX(pos.x() - self.tabBar.x())
        return not self.tabBar.tabRegion().contains(pos)


class ProfileCard(QWidget):
    """ 自定义卡片 """

    def __init__(self, avatarPath: str, name: str, version: str, parent=None) -> None:
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


class MaxBtn(MaximizeButton):
    def __init__(self, parent) -> None:
        super().__init__(parent=parent)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        color, bgColor = self._getColors()

        # draw background
        painter.setBrush(bgColor)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 4, 4)

        # draw icon
        painter.setBrush(Qt.NoBrush)
        pen = QPen(color, 1)
        pen.setCosmetic(True)
        painter.setPen(pen)

        r = self.devicePixelRatioF()
        painter.scale(1 / r, 1 / r)
        if not self._isMax:
            painter.drawRect(int(18 * r), int(11 * r), int(10 * r), int(10 * r))
        else:
            painter.drawRect(int(18 * r), int(13 * r), int(8 * r), int(8 * r))
            x0 = int(18 * r) + int(2 * r)
            y0 = 13 * r
            dw = int(2 * r)
            path = QPainterPath(QPointF(x0, y0))
            path.lineTo(x0, y0 - dw)
            path.lineTo(x0 + 8 * r, y0 - dw)
            path.lineTo(x0 + 8 * r, y0 - dw + 8 * r)
            path.lineTo(x0 + 8 * r - dw, y0 - dw + 8 * r)
            painter.drawPath(path)


class MinBtn(MinimizeButton):
    def __init__(self, parent) -> None:
        super().__init__(parent=parent)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        color, bgColor = self._getColors()

        # draw background
        painter.setBrush(bgColor)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 4, 4)

        # draw icon
        painter.setBrush(Qt.NoBrush)
        pen = QPen(color, 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(18, 16, 28, 16)


class CloseBtn(CloseButton):

    def __init__(self, parent) -> None:
        super().__init__(parent=parent)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        color, bgColor = self._getColors()

        # draw background
        painter.setBrush(bgColor)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 4, 4)

        # draw icon
        color = color.name()
        pathNodes = self._svgDom.elementsByTagName('path')
        for i in range(pathNodes.length()):
            element = pathNodes.at(i).toElement()
            element.setAttribute('stroke', color)

        renderer = QSvgRenderer(self._svgDom.toByteArray())
        renderer.render(painter, QRectF(self.rect()))


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

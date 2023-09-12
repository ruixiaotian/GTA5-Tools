#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :CheatsPage.py
# @Time :2023-9-11 下午 09:47
# @Author :Qiao
from PyQt5.QtWidgets import QWidget, QLabel


class TwoTakeOnePage(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("2take1")

        self.label = QLabel("2take1", self)


class StandPage(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("Stand")

        self.label = QLabel("stand", self)



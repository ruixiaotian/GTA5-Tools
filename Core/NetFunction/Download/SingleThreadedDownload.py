#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :SingleThreadedDownload.py
# @Time :2023-10-25 下午 11:47
# @Author :Qiao
from pathlib import Path
from queue import Queue

import requests
from PyQt5.QtCore import QThread, pyqtSignal
from creart import it

from Core.FileFunction.PathFunc import PathFunc


class SingleThreadedDownload(QThread):
    progressRange = pyqtSignal(int, int)
    downloadProgressSignal = pyqtSignal(int)
    setDownloadProgressSignal = pyqtSignal(int)
    downloadIsCompleteSignal = pyqtSignal(Path)
    toggleProgressBarSignal = pyqtSignal()
    toggleInProgressBarSignal = pyqtSignal()
    errorSignal = pyqtSignal(str)

    def __init__(self, url: str) -> None:
        super().__init__()
        self.url = url

    def run(self) -> None:
        """启动函数"""
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            self.progressRange.emit(0, int(self.getFileSize() / 1024))  # 设置进度条范围，并且转为kb
            self.toggleProgressBarSignal.emit()
            with open(it(PathFunc).tmp_path / Path(self.file_name), "wb") as f:
                for chunk in requests.get(self.url, headers=headers, stream=True).iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        self.downloadProgressSignal.emit(1)
            self.downloadIsCompleteSignal.emit(it(PathFunc).tmp_path / self.file_name)
            self.setDownloadProgressSignal(0)
            self.toggleInProgressBarSignal.emit()
        except Exception as error:
            self.errorSignal.emit(error.__str__())

    def getFileSize(self) -> int:
        """获取文件大小"""
        # 处理一些参数
        self.url = requests.head(self.url).headers["Location"]
        requestsHeaders = requests.head(self.url).headers
        self.file_name = requestsHeaders["Content-Disposition"].split(';')[2].replace('filename=', '').strip('"')
        # 返回长度
        return int(requestsHeaders["Content-Length"])
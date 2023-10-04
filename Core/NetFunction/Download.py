#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :Download.py
# @Time :2023-10-3 下午 01:49
# @Author :Qiao
"""
下载模块
"""
from pathlib import Path
from queue import Queue

import requests
from PyQt5.QtCore import QThread, pyqtSignal
from creart import it

from Core.FileFunction.PathFunc import PathFunc


class Download(QThread):
    progressRange = pyqtSignal(int, int)
    downloadProgressSignal = pyqtSignal(int)
    setDownloadProgressSignal = pyqtSignal(int)
    downloadIsCompleteSignal = pyqtSignal()
    toggleProgressBarSignal = pyqtSignal()
    toggleInProgressBarSignal = pyqtSignal()
    errorSignal = pyqtSignal(str)

    def __init__(self, url: str) -> None:
        super().__init__()
        self.url = url
        self.thread_count = 16  # 下载线程数量
        self.copies_count = 32  # 下载分块数量

    def run(self) -> None:
        """启动函数"""
        try:
            self.getDownloadThread()
            self.createThread()
            self.mergeFiles()
            self.downloadIsCompleteSignal.emit()
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

    def getDownloadThread(self) -> None:
        """获取下载线程的列队"""
        self.bytes_queue = Queue(self.copies_count)  # 创建字节队列
        file_length = self.getFileSize()  # 将文件大小赋值
        start_bytes = -1  # 开始字节为-1
        for i in range(self.copies_count):
            bytes_size = int(file_length / self.copies_count) * i  # 计算目前字节

            # 最后一个时 末尾字节为文件大小 避免落下一些字节未下载
            if i == self.copies_count - 1:
                bytes_size = file_length

            # start_bytes用来保存上一次的字节末尾
            bytes_length = f"{start_bytes + 1}-{bytes_size}"
            self.bytes_queue.put([i, bytes_length])  # 加入队列 并赋予编号（i）
            start_bytes = bytes_size  # 将开始字节重新赋值

    def createThread(self) -> None:
        """创建下载线程"""
        self.end_queue = Queue(maxsize=1000)
        # 创建线程并启动
        thread_list = []
        self.toggleProgressBarSignal.emit()
        self.progressRange.emit(0, self.thread_count)
        for i in range(self.thread_count):
            thread = DownloadThread(self.bytes_queue, self.end_queue, self.url)
            thread_list.append(thread)
        # 启动线程
        for thread in thread_list:
            thread.start()
        # 等待结束
        for thread in thread_list:
            thread.wait()
            self.downloadProgressSignal.emit(1)

    def mergeFiles(self) -> None:
        """合并下载好的文件"""
        self.setDownloadProgressSignal.emit(0)
        self.progressRange.emit(0, self.copies_count)
        with open(it(PathFunc).tmp_path / self.file_name, "ab") as f:
            for i in range(self.copies_count):
                with open(it(PathFunc).tmp_path / f"{i}.tmp", "rb") as bytes_f:
                    f.write(bytes_f.read())
                # 删除临时文件
                Path(it(PathFunc).tmp_path / f"{i}.tmp").unlink()
                # 返回信号
                self.downloadProgressSignal.emit(1)


class DownloadThread(QThread):
    """下载线程"""

    def __init__(self, bytes_queue: Queue, end_queue: Queue, url: str) -> None:
        super().__init__()
        self.end_queue = end_queue
        self.bytes_queue = bytes_queue
        self.url = url
        self.path = it(PathFunc).tmp_path

    def run(self) -> None:
        while not self.bytes_queue.empty():
            bytes_range = self.bytes_queue.get()
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Range": f"bytes={bytes_range[1]}"
            }
            with open(self.path / Path(f"{bytes_range[0]}.tmp"), "wb") as f:
                f.write(requests.get(self.url, headers=headers).content)
            self.end_queue.put(1)

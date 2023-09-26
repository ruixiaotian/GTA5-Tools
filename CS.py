#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :CS.py
# @Time :2023-9-21 下午 10:48
# @Author :Qiao


# def apply_operator(x, op):
#     return {'x': x * 10, '//': x * 2, '中': x}[op]
#
#
# def find_operations(a, b, c, target):
#     operators = ['x', '//', '中']
#
#     for op1, op2, op3 in [(op1, op2, op3) for op1 in operators for op2 in operators for op3 in operators]:
#         if apply_operator(a, op1) + apply_operator(b, op2) + apply_operator(c, op3) == target:
#             return f"{a}连接{op1}\n{b}连接{op2}\n{c}连接{op3}\n"
#
#
# print(find_operations(7, 6, 9, 85))


class A:

    def __init__(self):
        self.infoDict = {
            "system": "Windows10",  # 系统要求
            "untie": "3小时",  # 解绑时间
            "opMode": "键盘",  # 操作方式
            "Key": "F4",  # 呼出键
            "Lua": True,  # Lua支持性
            "Shv": True,  # Shv插件支持性
            "Mode": True,  # Mod支持性
            "Language": True  # 是否支持多语言
        }
        print(self.infoDict)

        self.infoDict = {k: "Unknown" if v is None else v for k, v in self.infoDict.items()}

        print(self.infoDict)

        self.infoDict = {
            k: self.tr("Support") if v is True else self.tr("Not Supported") if v is False else v
            for k, v in self.infoDict.items()
        }

        print(self.infoDict)


A()

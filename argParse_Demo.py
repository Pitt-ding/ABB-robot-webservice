#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : PR
# @Time     : 2023/5/13 1:52
# @File     : argParse_Demo.py
# @Project  : WebService

import math
import argparse  # 导入argparse模块
# 用来装载参数的容器
parser = argparse.ArgumentParser(description='Calculate volume of a cylinder')
# 给这个解析对象添加命令行参数
parser.add_argument('radius', type=int, help='Radius of cylinder')
parser.add_argument('height', type=int, help='Height of cylinder')
args = parser.parse_args()  # 获取所有参数


def cylinder_volume(radius, height):
    vol = (math.pi) * (radius**2) * (height)
    return vol


if __name__ == '__main__':
    print(cylinder_volume(args.radius, args.height))

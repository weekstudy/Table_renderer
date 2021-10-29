#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
"""
@AUTHOR:
@FILE:TextString.py
@NAME:Table_renderer
@TIME:2021/07/16
@IDE: PyCharm
@Ref:
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw, features
import pickle
import argparse
from argparse import RawTextHelpFormatter
import fnmatch
import os
import json
import random
import shutil
import traceback
import copy


class TextString(object):
    def __init__(self, text_string=None, font=None, color=(163, 131, 80),
                 char_size=10, direction=None, line_space=0, char_space=0):
        """
        :param text_string: 字符串
        :param coord_xy: 首字符坐标
        :param font: 字体文件路径
        :param color: 字体颜色
        :param char_size: 字大小
        :param direction: 文字书写方向,It can be 'rtl' (right to left), 'ltr' (left to right)
                          or 'ttb' (top to bottom) or 'btt'(bottom to top).
        :param line_space: 行间距
        :param char_space: 字间距
        """
        if isinstance(text_string, str):
            self.text = text_string
            self.direction = direction
        elif isinstance(text_string, (int, float)):
            self.text = str(text_string)
            self.direction = None

        self.coord_xy = None
        if font is None:
            font = "./fonts/simhei.ttf"
        self.font_file = font
        # 这里需要确定多行高度是不是也是跟单行一样
        # self.font = ImageFont.truetype(self.font_file, char_size)
        # print(self.font_file)
        self.font = ImageFont.truetype(self.font_file, char_size)

        self.char_w = char_size
        self.char_h = self.getsize()[1]
        self.line_space = abs(line_space)
        self.char_space = char_space
        self.color = color

        self.bbox = None
        self.vaild_text_bbox = None
        self.multi_line = []
        # self.direction = direction

    def set_direction(self):
        pass

    def get_length(self):
        return self.font.getlength(self.text)

    def get_single_bbox(self):

        pass


    def get_bbox(self):

        """
        这里得到的是单行的文本框，并没有得到多行的整个文本框
        :return:
        """
        if not self.coord_xy:
            self.coord_xy = (1, 1)
        coord_xy = self.coord_xy
        assert len(coord_xy) == 2

        # 这里切割时会多一个空格,因此去掉
        sub_str_lists = self.text.split('\n')

        cnt_str = 0
        bboxes = []
        if self.direction == 'ltr' or self.direction is None:
            lt_x = self.coord_xy[0]
            lt_y = self.coord_xy[1]
            for sub_str in sub_str_lists:
                if sub_str != '':
                    cnt_str += 1
                    # print("The string is %s " % sub_str)
                    sub_str_len = len(sub_str)
                    # self.draw.text((lt_x, lt_y), char, text_string.color, font=text_string.font)
                    # # 记下写了几个字
                    # vaild_text += char
                    # cnt_char += 1
                    # lt_x = lt_x + text_string.char_space + text_string.char_w
                    # todo 空格是占一个字节大小，汉字2个字节大小
                    width = sub_str_len * self.char_w + (sub_str_len - 1) * self.char_space
                    width = self.font.getsize(sub_str)[0]+(sub_str_len - 1) * self.char_space
                    # if self.char_space
                    height = self.char_h

                    rb_x = lt_x + width
                    rb_y = lt_y + height
                    bbox = (lt_x, lt_y, rb_x, rb_y)
                    bboxes.append(bbox)
                    lt_y = rb_y + self.line_space

        elif self.direction == 'ttb':
            lt_x = self.coord_xy[0]
            lt_y = self.coord_xy[1]
            for sub_str in sub_str_lists:
                if sub_str == '':
                    continue
                elif sub_str != '':
                    cnt_str += 1
                    # print("The string is %s " % sub_str)
                    sub_str_len = len(sub_str)
                    height = sub_str_len * self.char_h + (sub_str_len - 1) * self.char_space
                    # height = self.font.getsize(sub_str)[1]+(sub_str_len - 1) * self.char_space
                    width = self.char_w

                    rb_x = lt_x + width
                    rb_y = lt_y + height
                    bbox = (lt_x, lt_y, rb_x, rb_y)
                    bboxes.append(bbox)
                    lt_x = rb_x + self.line_space
        self.bbox = bboxes
        return bboxes
        # return self.font.getbbox(self.text)

    def getoffset(self):
        return self.font.getoffset(self.text)

    def getsize(self):

        return self.font.getsize(self.text)

    def split_string(self):
        """
        将多行切成单行
        :return:
        """
        res = []
        text_list = self.text.split('\n')
        for sub_str in text_list:
            if sub_str != '':
                res.append(sub_str)

        self.multi_line = res
        return res

    def draw_single_bbox(self, xy, enter):
        pass




if __name__ == '__main__':
    # char_str1 = '\n\n白日依山尽\n黄河入海流\n欲穷千里目\n更上一层楼'
    #
    # char_str2 = '文字：不能\n34347989\n334444\n123345\n'
    # print(len(char_str1))
    # # char_size = 60
    # font_path = "/Users/zhouli/YaSpeed/Table_renderer/fonts/simhei.ttf"
    # font = ImageFont.truetype(font_path, 40)
    # # font = ImageFont.FreeTypeFont(font_path, 50)
    # s = '是是'
    # print(font.getlength(s))
    # print(font.getsize(s))
    # print(font.getoffset(s))
    # print(font.getbbox(s))

    # font_color = (163, 131, 80)
    # text_str1 = TextString(text_string=char_str1, font=font_path, char_size=40,
    #                        color=font_color, direction=None, line_space=60, char_space=10)
    #
    # print(text_str1.getsize())

    q = ' '
    print(q.split('\n'))
    print(len(q.split('\n')))
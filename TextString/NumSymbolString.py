#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
"""
@AUTHOR:
@FILE:NumSymbolString.py
@NAME:Table_renderer
@TIME:2021/08/02
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


class NumSymbolString(object):
    def __init__(self, num_string=None, font=None, color=(163, 131, 80),
                 char_size=10, direction=None,line_space=0):
        """

        :param num_string:
        :param font:
        :param color:
        :param char_size:
        :param direction:
        """
        if isinstance(num_string, str):
            self.text = num_string
            self.direction = direction
        elif isinstance(num_string, (int, float)):
            self.text = str(num_string)
            self.direction = None

        self.coord_xy = None
        self.char_w = char_size
        self.line_space = line_space
        self.font_file = font
        self.font = ImageFont.truetype(self.font_file, char_size)
        # self.font = ImageFont.FreeTypeFont(self.font_file, char_size)
        self.color = color
        self.bbox = None
        self.vaild_text_bbox = None
        self.multi_line = []

    def get_bbox(self):
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



if __name__ == '__main__':
    pass

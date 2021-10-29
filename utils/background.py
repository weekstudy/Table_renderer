#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
"""
@AUTHOR:
@FILE:background.py
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


def bg_image(h=720, w=1280):
    """
    生成背景图
    :param h:
    :param w:
    :return:
    """
    img_h = h
    img_w = w
    # RGB
    bg_img = Image.new("RGB", (img_w, img_h), "white")
    img_arr = np.array(bg_img)
    # print(img_arr)

    return img_arr






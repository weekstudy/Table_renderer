#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
"""
@author:zhouqiang
@file:placechar.py
@NAME:Table_renderer
@time:2021/08/29
@IDE: PyCharm
 
"""

import cv2
import numpy as np
import random
import json

import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw, features

from TextString.TextString import TextString


def place():
    with open('images/CCI138.txt', 'r') as fr:
        lines = fr.readlines()
    for line in lines:
        content = line.split('\t')[1]
        content = json.loads(content)
    img_path = 'images/CC138.jpg'
    fp = "../fonts/simhei.ttf"
    font = ImageFont.truetype(fp,size=40)
    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)
    for points in content:
        xy = points['points']
        draw.text(xy[0],'你的时间你觉得呢',font=font,fill='black')
    img.save('./aa.jpg')



if __name__ == '__main__':
    place()



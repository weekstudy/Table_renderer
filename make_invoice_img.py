# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 17:47:21 2021

@author: songy
"""

import cv2
# import freetype
from PIL import Image, ImageDraw, ImageFont
import numpy as np


def cv2AddChineseText(img, text, position, textColor=(0, 255, 0), textSize=30):
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype(
        "./fonts/simsun.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text(position, text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def InitCanvas(width, height, color=(255, 255, 255)):
    canvas = np.ones((height, width, 3), dtype="uint8")
    canvas[:] = color
    return canvas


img = cv2.imread("R-C.jpg")

roi = InitCanvas(603, 33, color=(255, 255, 255))
frame0 = cv2AddChineseText(img, "有限公司", (925, 350), (81, 86, 86), 34)
frame = cv2AddChineseText(roi, "称:洋达国际货运代理（上海）有限公司", (0, 0), (81, 86, 86), 34)  # 169,169,169;;88,87,86;;41,36,36
# roi_rect=cv2.Rect(322,355,roi.cols, roi.rows)
img[350:383, 322:925] = frame

cv2.imshow('发票', frame)
cv2.waitKey(0)
cv2.imwrite("r-c-add.jpg", frame0)

cv2.namedWindow('最后', cv2.WINDOW_NORMAL)
cv2.imshow('最后', img)
cv2.waitKey(0)
cv2.imwrite("r-c-repalce.jpg", img)

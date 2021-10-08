#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
"""
@author:zhouqiang
@file:gen_noise.py
@NAME:Table_renderer
@time:2021/09/09
@IDE: PyCharm
 
"""

import cv2
import numpy as np
from PIL import Image
from PIL.ImageDraw import ImageDraw
import imutils


def ext(num):
    if num > 255:
        return 255
    if num < 0:
        return 0
    else:
        return num

def gen_noise():
    bg = cv2.imread('../receipts/receipts_train_1_v2/00000.jpg')
    # bg = np.ones((400, 400, 3), dtype=np.uint8)*255

    width = bg.shape[1]
    height = bg.shape[0]
    img = np.zeros((height, width, 3), dtype=np.uint8)
    # 绘制圆
    cX = 300
    cY = 800
    radius = 10
    cv2.rectangle(img, (int(cX), int(cY)), (int(cX+50), int(cY+50)), (175, 0, 0), -1)

    # cv2.imwrite('./tmp.jpg', img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    x_index, y_index = np.where(gray != 0)

    h, w, ch = img.shape
    for row in range(h):
        for col in range(w):
            if row in x_index and col in y_index:

                s = np.random.normal(0, 100, 10)
                # 去除每一个像素的三个通道值
                b = img[row, col, 0]
                g = img[row, col, 1]
                r = img[row, col, 2]
                # 在每一个像素的三个通道值上加上高斯噪声
                img[row, col, 0] = ext(b + s[0])
                img[row, col, 1] = ext(g + s[1])
                img[row, col, 2] = ext(r + s[2])

    for i in range(len(x_index)):
        bg[x_index[i], y_index[i], :] = img[x_index[i], y_index[i], :]
    bg = cv2.cvtColor(bg, cv2.COLOR_BGR2RGB)
    res = Image.fromarray(bg)
    res.save('./bg.jpg')
    print(2)


if __name__ == '__main__':
    gen_noise()

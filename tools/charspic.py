#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
"""
@author:zhouqiang
@file:charspic.py
@NAME:Table_renderer
@time:2021/08/27
@IDE: PyCharm
 
"""

import cv2
import numpy as np
import random
import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw, features

from TextString.TextString import TextString


class CharsPic(object):
    def __init__(self, text_string: TextString):
        self.text_string = text_string
        self.text = text_string.text
        self.font = text_string.font
        self.bbox = None
        self.size = None
        self.pic = None

    def gen_pic(self, isblur=True, isnosie=True, bboxon=True):
        a = random.randint(0, 50)
        color = (a, a, a)
        subtext_list = self.text.strip().split('\n')
        subtext_list2 = sorted(subtext_list, key=lambda x: len(x))
        # max_len = len(subtext_list2[-1])
        if self.size is None:
            # 如果没有字间距，没有行间距
            if self.text_string.char_space == 0 and self.text_string.line_space == 0:
                w, h = self.font.getsize(subtext_list2[-1])
                self.size = (w, int(h*len(subtext_list)))
            else:
                w, h = 0, 0
                for char in subtext_list2[-1]:
                    # draw.text((x, y), char, font=self.font, fill=(79, 141, 190))
                    char_w = self.font.getsize(char)[0]
                    w += char_w + self.text_string.char_space
                h = len(subtext_list)*(self.font.getsize(self.text)[1])\
                    + self.text_string.line_space*(len(subtext_list)-1)
                self.size = (w, h)
        pil_img = Image.new('RGB', (self.size[0] + 2, self.size[1] + 2), 'white')
        draw = ImageDraw.Draw(pil_img)
        x, y = 1, 1
        for subtext in subtext_list:
            if self.text_string.char_space == 0 and self.text_string.line_space==0:
                draw.text((x, y), subtext, font=self.font, fill=(79, 141, 190))
            else:
                for char in subtext:
                    draw.text((x, y), char, font=self.font, fill=(79, 141, 190))
                    char_w = self.font.getsize(char)[0]
                    x += char_w + self.text_string.char_space
                x = 1
            y += self.font.getsize(self.text)[1] + self.text_string.line_space

        if bboxon:
            draw.rectangle([(1, 1), (self.size[0], self.size[1])], fill=None, outline='red')
        if isnosie:
            tmp = np.array(pil_img)
            res = self.gauss_noise(tmp)
            pil_img = Image.fromarray(res)
        if isblur:
            new_pic = cv2.GaussianBlur(np.array(pil_img), (5, 5), 0)
            pil_img = Image.fromarray(new_pic)
        self.pic = pil_img
        # pil_img.save('./test.jpg')

    # 定义一个各通道值 0-255范围 超出按截断处理
    @staticmethod
    def ext(num):
        if num > 255:
            return 255
        if num < 0:
            return 0
        else:
            return num

    # 高斯噪点的生成
    def gauss_noise(self, image):
        h, w, ch = image.shape
        for row in range(h):
            for col in range(w):
                # numpy.random.normal(loc, scale, size)生成高斯分布的概率密度随机数
                # loc：float代表生成的高斯分布的随机数的均值
                # scale：float 代表这个分布的方差
                # size：int or tuple of ints 输出的shape，默认为None，只输出一个值
                # 当指定整数时，输出整数个值，也可以输出（a, b）→ a 行 b 列
                s = np.random.normal(0, 5, 3)
                # 去除每一个像素的三个通道值
                b = image[row, col, 0]
                g = image[row, col, 1]
                r = image[row, col, 2]
                # 在每一个像素的三个通道值上加上高斯噪声
                image[row, col, 0] = self.ext(b + s[0])
                image[row, col, 1] = self.ext(g + s[1])
                image[row, col, 2] = self.ext(r + s[2])

        return image

    def save(self, fp):
        if self.pic is None:
            self.gen_pic()
        self.pic.save(fp)

    def concatenate(self, pic, direction='ltr'):
        w, h = self.pic.size
        w2, h2 = pic.size
        # print(h, h2)
        # assert h == h2, 'the size should be equally'
        pil_img = Image.new('RGB', (w + w2 + 3, max(h, h2)), 'white')
        pil_img.paste(self.pic, (0, 0))
        pil_img.paste(pic, (w + 3, 0))
        return pil_img


if __name__ == '__main__':
    # font = "../fonts/simhei.ttf"
    # text = TextString('黄金二阿胶粉借款金额', font, char_size=40)
    # a = CharsPic(text)
    # a.gen_pic(isblur=False, isnosie=False, bboxon=False)
    # bg = Image.open('../test/receipt.jpg')
    # bg.paste(a.pic, (570, 375))
    # bg.save('./ss.jpg')

    text = 'sddddddjsj\nshdushdu'
    sub = text.strip().split('\n')
    sub2 = sorted(sub, key=lambda x: len(x))
    print(sub2)

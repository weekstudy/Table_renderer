#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
"""
@AUTHOR:
@FILE:TextImage.py
@NAME:Table_renderer
@TIME:2021/07/19
@IDE: PyCharm
@Ref:
"""

import random

from TextString.TextString import *
from Canvas.Canvas import *


class TextToImage(object):
    def __init__(self, text_string):
        self.text_string = text_string


def text2image(text_string, ext='jpg'):
    canvas = CanvasImage(size=(1000, 800), color='white')
    canvas.draw_text_string(text_string, (0, 0))
    bboxes = canvas.get_bbox(text_string)
    # todo 这里可能有问题
    cover_bbox = (bboxes[0][0], bboxes[0][1], bboxes[-1][2], bboxes[-1][3])
    new_bboxes = []
    if text_string.direction == 'rtl':
        cover_bbox = (cover_bbox[2], cover_bbox[1], cover_bbox[0], cover_bbox[3])
        for bbox in bboxes:
            new_bbox = (bbox[2], bbox[1], bbox[0], bbox[3])
            new_bboxes.append(new_bbox)
    elif text_string.direction == 'btt':
        cover_bbox = (cover_bbox[0], cover_bbox[3], cover_bbox[2], cover_bbox[1])
        for bbox in bboxes:
            new_bbox = (bbox[0], bbox[3], bbox[1], bbox[2])
            new_bboxes.append(new_bbox)
    else:
        new_bboxes = bboxes
    bboxes = new_bboxes
    cover_text_image = canvas.crop(cover_bbox)
    print('line 42:saved ./CoverImages/cover.jpg')
    cover_text_image.save('./CoverImages/cover.jpg')

    text_imgs = []
    for i, bbox in enumerate(bboxes):
        assert len(bbox) == 4
        text_img = canvas.crop(bbox)
        size = (bbox[2] - bbox[0], bbox[3] - bbox[1])
        text_imgs.append((text_img, size))
        if text_string.direction == 'ltr' or text_string.direction == 'rtl' or text_string.direction is None:
            text_img.save('./HorizontalTextImage/%02d.%s' % (i, ext))
            print('line 52:', i)
        if text_string.direction == 'ttb' or text_string.direction == 'bbt':
            text_img.save('./VerticalTextImage/%02d.%s' % (i, ext))
            print('line 55:', i)
    del canvas
    return text_imgs, cover_text_image


def get_coordxy(text_strings: dict):
    """
    得到随机文本框左上角的xy坐标
    :param text_strings:
    :return: nx2
    """
    n = len(text_strings)
    bboxes = []
    tmp = []
    text_strs = text_strings['ltr']
    for text in text_strs:
        bbox = text.get_bbox()
        size = (bbox[0][2] - bbox[0][0], bbox[0][3] - bbox[0][1])
        tmp.append((text, size))

    tmp = sorted(tmp, key=lambda x: x[1][0], reverse=True)
    x1 = random.randint(50, 100)
    y1 = random.randint(50, 80)
    assert len(tmp) == len(text_strings['ltr'])

    # 修改文本坐标

    for ele in tmp:
        ele[0].coord_xy = (x1, y1)
        y1 = y1 + ele[1][1] + random.randint(20, 50)
        x1 = x1 - random.randint(-10, 10)

    tmp2 = []
    text_strs2 = text_strings['ttb']
    for text2 in text_strs2:
        bbox2 = text2.get_bbox()
        size = (bbox2[0][2] - bbox2[0][0], bbox2[0][3] - bbox2[0][1])
        tmp2.append((text2, size))
    # index1 = np.array(tmp).argmax(axis=0)
    tmp2 = sorted(tmp2, key=lambda x: x[1][1], reverse=True)
    x2 = random.randint(1200, 1250)
    y2 = random.randint(630, 680)
    assert len(tmp2) == len(text_strings['ttb'])

    # 修改文本坐标
    for ele in tmp2:
        ele[0].coord_xy = (x2 - ele[1][0], y2 - ele[1][1])
        x2 = x2 - ele[1][0] - random.randint(50, 80)
        y2 = y2 - random.randint(-15, 25)

    tmp2 = tmp + tmp2

    return tmp2






import hashlib


def get_md5(url):
    """
    由于hash不处理unicode编码的字符串（python3默认字符串是unicode）
     所以这里判断是否字符串，如果是则进行转码
     初始化md5、将url进行加密、然后返回加密字串
    """
    if isinstance(url, str):
        url = url.encode("utf-8")
    md = hashlib.md5()
    # hashlib.
    print(md)
    md.update(url)
    return md.hexdigest()


if __name__ == '__main__':
    # urls = "1"
    # print(get_md5(urls))
    # print(get_md5('1'))
    a = [(10, 0, 100, 10), (10, 0, 90, 10)]
    print(max([(b[2] - b[0]) for b in a]))

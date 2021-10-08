#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
"""
@author:zhouqiang
@file:utils.py
@NAME:Table_renderer
@time:2021/09/11
@IDE: PyCharm
 
"""


import os
import random


def get_dict(fp=None):
    char_dict = {}
    if fp:
        with open(fp, 'r') as fr:
            lines = fr.readlines()
    for i, char in enumerate(lines):
        char_dict[i + 1] = char.strip()
    return char_dict


def get_length(n: int, direction, kind='text'):
    """
    得到随机字符串的长度
    :param n:
    :param direction:
    :param kind: symbol or char
    :return:
    """
    max_len, min_len = 0, 0
    if kind == 'text':
        if direction == 'ltr':
            max_len = 20
            min_len = 3
        elif direction == 'ttb':
            max_len = 9
            min_len = 2
    elif kind == 'sym':
        max_len = 25
        min_len = 10
    leng_list = []
    for i in range(n):
        length = random.randint(min_len, max_len)
        # length = 10
        leng_list.append(length)
    return leng_list


def get_string(char_dict: dict, length: int, range_t=(400, 800)) -> str:
    """
    得到随机字符串
    :param char_dict:
    :param length:
    :param range_t:
    :return:
    """
    if isinstance(range_t, int):
        range_t = (1, range_t)
    t = len(char_dict)
    if range_t is None:
        range_t = (1, t)
    t1, t2 = range_t[0], range_t[1]
    assert 1 <= t1 <= int(t), "can't find the key"
    assert 1 <= t2 <= int(t), "can't find the key"
    str_n = length
    text_str = ''
    for i in range(str_n):
        key = random.randint(t1, t2)
        # if char_dict[key]==' ':
        #     print(key)
        text_str += char_dict[key]
    # print(text_str)
    return text_str


def get_coordxy2(text_strings: dict):
    """
    得到随机文本的xy坐标
    :param text_strings:
    :return: nx2-array
    """
    n = len(text_strings)
    bboxes = []
    tmp = []
    tmp2 = []
    text_strs = text_strings['ltr']
    for text in text_strs:
        # 这里的bbox是整个文本的大小，不是写在画布上的大小
        # 写在画布的文本框大小，要用Canvas.get_bbox
        # todo 这里有点问题，万一是多行文本怎么办
        bbox = text.get_bbox()
        # bbox = text.getsize()
        size = (bbox[0][2] - bbox[0][0], bbox[0][3] - bbox[0][1])
        # text_h = len(bbox) * text.char_h + (len(bbox) - 1) * text.line_space
        # text_w = max([(b[2] - b[0]) for b in bbox])
        # text_bbox_size = (text_w, text_h)

        tmp.append((text, size))

    tmp = sorted(tmp, key=lambda x: x[1][0], reverse=True)

    text_strs2 = text_strings['ttb']
    for text2 in text_strs2:
        bbox2 = text2.get_bbox()
        size = (bbox2[0][2] - bbox2[0][0], bbox2[0][3] - bbox2[0][1])
        tmp2.append((text2, size))
    # index1 = np.array(tmp).argmax(axis=0)
    tmp2 = sorted(tmp2, key=lambda x: x[1][1], reverse=True)
    assert len(tmp) == len(text_strings['ltr'])

    # 随机决定文本框排在哪个位置0-横向文本，
    # 随机产生0(left - top)，1(right - top)，2(left - bottom)，3(right - bottom)
    seed = random.randint(0, 3)
    # 随机产生0(left-top)，1(right-top)，2(left-bottom)，3(right-bottom)
    # seed2 = random.randint(0, 3)
    # ,横向文本写在左上角,竖向右下,
    if seed == 0:
        x1 = random.randint(50, 100)
        y1 = random.randint(50, 80)
        assert len(tmp) == len(text_strings['ltr'])

        # 修改文本坐标
        for ele in tmp:
            # 这里只考虑了单行文本，而且一定在画布内
            ele[0].coord_xy = (x1, y1)
            y1 = y1 + ele[1][1] + random.randint(30, 50)
            x1 = x1 - random.randint(-5, 5)

        x2 = random.randint(1200, 1250)
        y2 = random.randint(630, 680)
        # assert len(tmp2) == len(text_strings['ttb'])

        # 修改文本坐标
        for ele in tmp2:
            ele[0].coord_xy = (x2 - ele[1][0], y2 - ele[1][1])
            x2 = x2 - ele[1][0] - random.randint(50, 80)
            y2 = y2 - random.randint(0, 5)

    elif seed == 1:
        x1 = random.randint(1200, 1250)
        y1 = random.randint(50, 80)
        # assert len(tmp) == len(text_strings['ltr'])

        # 修改文本坐标
        for ele in tmp:
            ele[0].coord_xy = (x1 - ele[1][0], y1)
            y1 = y1 + ele[1][1] + random.randint(30, 50)
            x1 = x1 - random.randint(0, 5)

        x2 = random.randint(50, 100)
        y2 = random.randint(630, 680)
        # assert len(tmp2) == len(text_strings['ttb'])

        # 修改文本坐标
        for ele in tmp2:
            ele[0].coord_xy = (x2, y2 - ele[1][1])
            x2 = x2 + ele[1][0] + random.randint(50, 80)
            y2 = y2 - random.randint(0, 5)

    elif seed == 2:
        x1 = random.randint(1200, 1250)
        y1 = random.randint(630, 680)
        assert len(tmp) == len(text_strings['ltr'])

        # 修改文本坐标
        for ele in tmp:
            ele[0].coord_xy = (x1 - ele[1][0], y1 - ele[1][1])
            y1 = y1 - ele[1][1] - random.randint(30, 50)
            x1 = x1 - random.randint(0, 5)

        x2 = random.randint(50, 100)
        y2 = random.randint(50, 80)
        # assert len(tmp2) == len(text_strings['ttb'])

        # 修改文本坐标
        for ele in tmp2:
            ele[0].coord_xy = (x2, y2)
            x2 = x2 + ele[1][0] + random.randint(50, 80)
            y2 = y2 + random.randint(0, 5)

    elif seed == 3:
        x1 = random.randint(50, 100)
        y1 = random.randint(630, 680)
        assert len(tmp) == len(text_strings['ltr'])

        # 修改文本坐标
        for ele in tmp:
            ele[0].coord_xy = (x1, y1 - ele[1][1])
            y1 = y1 - ele[1][1] - random.randint(30, 50)
            x1 = x1 + random.randint(0, 5)

        x2 = random.randint(1200, 1250)
        y2 = random.randint(50, 80)
        # assert len(tmp2) == len(text_strings['ttb'])

        # 修改文本坐标
        for ele in tmp2:
            ele[0].coord_xy = (x2 - ele[1][0], y2)
            x2 = x2 - ele[1][0] - random.randint(30, 50)
            y2 = y2 + random.randint(0, 5)

    tmp2 = tmp + tmp2

    return tmp2


def get_labels(bboxes, filename, fp='./Labels/'):
    if not os.path.exists(fp):
        os.makedirs(fp)
    # todo 要不要把字也写进label
    fp = fp + filename + '.txt'

    labels = []
    # 将bbox的坐标偏移2
    margin = 2
    with open(fp, 'w') as fw:
        for text_bbox in bboxes:
            char, bbox = text_bbox
                # char,bbox = text_bbox
            bbox = (bbox[0] - margin, bbox[1] - margin, bbox[2] + margin, bbox[3] + margin)
            bbox = list(map(str, bbox))
            label = bbox[0] + ',' + bbox[1] + ',' + bbox[2] + ',' + bbox[1] + ',' + bbox[2] + ',' + bbox[3] + ',' + \
                    bbox[0] + ',' + bbox[3] + ',' + char + '\n'

            fw.write(label)
                # points = [[bbox[0],bbox[1]], [bbox[2], bbox[1]], [bbox[2], bbox[3]],[bbox[0], bbox[3]]]
                # result = {"transcription": char,"points": points}
                # labels.append(result)

        # result = {"transcription": tmp[8], "points": s}
        #            label.append(result)
        #
        # fw.write(img_path + '\t' + json.dumps(labels, ensure_ascii=False) + '\n')


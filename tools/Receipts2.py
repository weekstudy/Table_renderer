#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
"""
@author:zhouqiang
@file:Receipts2.py
@NAME:Table_renderer
@time:2021/09/15
@IDE: PyCharm
 
"""

# ! /usr/bin/python3
# -*- coding:UTF-8 -*-

import os
import sys
import random
import yaml
import pdb
import re
import logging
import jsonlines

sys.path.append('..')
sys.path.append('.')

from TextString.TextString import *
from Canvas.Canvas import *
from tools.TextImage import *
from utils.utils import *
from tools.charspic import *


def receipt2(imgs_dir, basename, img_name, rows, logger):
    font_path = "./fonts/KaitiGB2312.ttf"
    font_path2 = './fonts/Times New Roman.ttf'
    char_dict_path = './utils/dict/cht_usually_dict.txt'
    char_dict_path2 = './utils/dict/nums_dict2.txt'

    font_color = (163, 131, 80)
    rec_color = (163, 131, 80)
    # s = 0.9
    s = 0.3 + random.random()
    # s = 1
    if s > 1.0:
        s = 1
    # s = 0.5
    bbox_offset = int(10 * s)
    char_size = int(random.randint(35, 38) * s)
    label = []
    char_dict = get_dict(fp=char_dict_path)
    char_dict_num2 = get_dict(fp=char_dict_path2)

    def scales(num):
        return int(num * s)

    if s >= 0.5:
        width = 2
    else:
        width = 1

    # 返回PIL.Image对象
    canvas = CanvasImage(size=tuple(map(scales, (2835, 1620))), color='white')
    # 两边虚竖线
    canvas.draw_line((int(90 * s), 0, int(90 * s), int(2800 * s)), rec_color, width=width)
    canvas.draw_line(tuple(map(scales, (2700, 0, 2700, 1620))), rec_color, width=width)

    # 整个大框
    canvas.draw_rectangle(tuple(map(scales, (200, 360, 2600, 1500))), fill='white', outline=rec_color,
                          width=width)

    # 第一行
    canvas.draw_rectangle(tuple(map(int, (200 * s, 360 * s, 290 * s, 620 * s))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(int, (290 * s, 360 * s, 1580 * s, 620 * s))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(int, (1580 * s, 360 * s, 1640 * s, 620 * s))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(int, (1640 * s, 360 * s, 2600 * s, 620 * s))), outline=rec_color, width=width)

    str1_1 = '购买方'
    text_str1_1 = TextString(text_string=str1_1, font=font_path, char_size=char_size,
                             color=font_color, direction='ttb', line_space=0, char_space=int(s*40))

    canvas.draw_text_string(text_str1_1, tuple(map(int, (s * 230, s * 400))))
    bbox1 = text_str1_1.get_bbox()

    tmp = {'transcription': str1_1,
           'points': [[bbox1[0][0] - bbox_offset, bbox1[0][1] - bbox_offset],
                      [bbox1[0][2] + bbox_offset, bbox1[0][1] - bbox_offset],
                      [bbox1[0][2] + bbox_offset, bbox1[0][3] + bbox_offset],
                      [bbox1[0][0] - bbox_offset, bbox1[0][3] + bbox_offset]]}
    # canvas.draw_rectangle(bbox[0], outline='red', width=3)
    label.append(tmp)

    str1_2_1 = '名'

    text_str1_2_1 = TextString(text_string=str1_2_1, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str1_2_1, tuple(map(scales, (305, 375))))
    bbox1 = text_str1_2_1.get_bbox()

    str1_2_1_2 = '称：'
    text_str1_2_1_2 = TextString(text_string=str1_2_1_2, font=font_path, char_size=char_size,
                                 color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str1_2_1_2, tuple(map(scales, (495, 375))))

    bbox2 = text_str1_2_1_2.get_bbox()
    tmp_str = get_string(char_dict, random.randint(8, 20), 300)
    val_text = TextString(tmp_str, font_path, char_size=char_size)
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox2[0][2] + 1, bbox2[0][1]))

    tmp = {'transcription': str1_2_1 + str1_2_1_2 + val_text.text,
           'points': [[bbox1[0][0] - bbox_offset, bbox1[0][1] - bbox_offset],
                      [bbox2[0][2] + val.pic.size[0] + bbox_offset, bbox1[0][1] - bbox_offset],
                      [bbox2[0][2] + val.pic.size[0] + bbox_offset, max(bbox1[0][3], bbox2[0][3]) + bbox_offset],
                      [bbox1[0][0] - bbox_offset, max(bbox1[0][3], bbox2[0][3]) + bbox_offset]]}
    label.append(tmp)

    str1_3_1 = '密码区'
    text_str1_3_1 = TextString(text_string=str1_3_1, font=font_path, char_size=char_size,
                               color=font_color, direction='ttb', line_space=0, char_space=int(s*40))
    canvas.draw_text_string(text_str1_3_1, tuple(map(int, (s * 1590, s * 400))))

    bbox1 = canvas.get_bbox(text_str1_3_1)[0]

    offset2 = random.randint(45, 55)
    x, y = (bbox1[0][2] + int(s * offset2), int(bbox1[0][1] - s * 5))

    tmp = {'transcription': str1_3_1,
           'points': [[bbox1[0][0] - bbox_offset, bbox1[0][1] - bbox_offset],
                      [bbox1[0][2] + bbox_offset, bbox1[0][1] - bbox_offset],
                      [bbox1[0][2] + bbox_offset, bbox1[0][3] + bbox_offset],
                      [bbox1[0][0] - bbox_offset, bbox1[0][3] + bbox_offset]]}
    label.append(tmp)

    char_dict_num = get_dict(fp="./utils/dict/nums_dict.txt")
    # font = '../fonts/Times New Roman.ttf'
    tmp_str = get_string(char_dict_num, 27, (1, 22)) + '\n'
    tmp_str += get_string(char_dict_num, 27, (1, 22)) + '\n'
    tmp_str += get_string(char_dict_num, 27, (1, 22)) + '\n'
    tmp_str += get_string(char_dict_num, 27, (1, 22))
    val_text = TextString(tmp_str, font_path, char_size=int(char_size * 1.2),
                          char_space=int(s * 10), line_space=int(s * 5))
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (x, y))
    w, h = val.pic.size
    tmp = {'transcription': tmp_str,
           'points': [[x - bbox_offset, y - bbox_offset],
                      [x + w + bbox_offset, y - bbox_offset],
                      [x + w + bbox_offset, y + h + bbox_offset],
                      [x - bbox_offset, y + h + bbox_offset]]}
    label.append(tmp)

    str1_2_2 = '纳税人识别号：'
    text_str1_2_2 = TextString(text_string=str1_2_2, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str1_2_2, tuple(map(scales, (305, 440))))
    bbox = text_str1_2_2.get_bbox()

    tmp_str = get_string(char_dict_num2, 18, (1, 10))
    val_text = TextString(tmp_str, font_path, char_size=int(char_size * 0.8))
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][2], bbox[0][1]))

    bbox2 = [[bbox[0][0] - bbox_offset, bbox[0][1] - bbox_offset],
             [bbox[0][2] + val.pic.size[0] + bbox_offset, bbox[0][1] - bbox_offset],
             [bbox[0][2] + val.pic.size[0] + bbox_offset, max(bbox[0][3], val.pic.size[1]) + bbox_offset],
             [bbox[0][0] - bbox_offset, max(bbox[0][3], val.pic.size[1]) + bbox_offset]]
    tmp = {'transcription': str1_2_2 + val_text.text, 'points': bbox2}

    label.append(tmp)

    str1_2_3 = '地址、电话：'
    text_str1_2_3 = TextString(text_string=str1_2_3, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=int(s * 8))
    canvas.draw_text_string(text_str1_2_3, tuple(map(scales, (305, 500))))

    bbox = text_str1_2_3.get_bbox()
    tmp_str1 = get_string(char_dict, 15, (1, 100))

    val_text1 = TextString(tmp_str1, font_path, char_size=int(char_size * 0.8))
    val1 = CharsPic(val_text1)
    val1.gen_pic(isblur=False, isnosie=True, bboxon=False)
    w, h = val1.pic.size
    canvas.paste_img(val1.pic, (bbox[0][2], bbox[0][1]))

    tmp_str = get_string(char_dict_num2, 11, (1, 10))
    val_text = TextString(tmp_str, font_path, char_size=int(char_size * 0.8))
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    offset = int(s * random.randint(5, 10))
    offset2 = int(s * random.randint(40, 55))
    canvas.paste_img(val.pic, (bbox[0][2] + int(s * offset2) + w, bbox[0][1] + int(s * offset)))

    tmp = {'transcription': str1_2_3 + tmp_str1 + tmp_str,
           'points': [[bbox[0][0] - bbox_offset, bbox[0][1] - bbox_offset],
                      [bbox[0][2] + int(s * offset2) + w + val.pic.size[0] + bbox_offset, bbox[0][1] - bbox_offset],
                      [bbox[0][2] + + int(s * offset2) + w + val.pic.size[0] + bbox_offset,
                       bbox[0][1] + int(s * offset) + val.pic.size[1] + bbox_offset],
                      [bbox[0][0] - bbox_offset, bbox[0][1] + int(s * offset) + val.pic.size[1] + bbox_offset]]}
    label.append(tmp)

    str1_2_4 = '开户行及账号：'
    text_str1_2_4 = TextString(text_string=str1_2_4, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str1_2_4, tuple(map(int, (s * 305, s * 565))))

    bbox = text_str1_2_4.get_bbox()

    tmp_str1 = get_string(char_dict, random.randint(12, 20), (1, 100))
    val_text1 = TextString(tmp_str1, font_path, char_size=int(char_size * 0.8))
    val1 = CharsPic(val_text1)
    val1.gen_pic(isblur=False, isnosie=True, bboxon=False)
    w, h = val1.pic.size
    canvas.paste_img(val1.pic, (bbox[0][2] + 1, bbox[0][1]))

    tmp_str = get_string(char_dict_num2, 11, (1, 10))
    val_text = TextString(tmp_str, font_path, char_size=int(char_size * 0.8))
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    offset = int(s * random.randint(5, 10))
    offset2 = int(s * random.randint(45, 55))
    canvas.paste_img(val.pic, (bbox[0][2] + int(s * offset2) + w, bbox[0][1] + int(s * offset)))

    tmp = {'transcription': str1_2_4 + tmp_str1 + tmp_str,
           'points': [[bbox[0][0] - bbox_offset, bbox[0][1] - bbox_offset],
                      [bbox[0][2] + int(s * offset2) + w + val.pic.size[0] + bbox_offset, bbox[0][1] - bbox_offset],
                      [bbox[0][2] + int(s * offset2) + w + val.pic.size[0] + bbox_offset,
                       bbox[0][1] + int(s * offset) + val.pic.size[1] + bbox_offset],
                      [bbox[0][0] - bbox_offset, bbox_offset + bbox[0][1] + int(s * offset) + val.pic.size[1]]]}
    label.append(tmp)

    # 第二行
    canvas.draw_rectangle(tuple(map(scales, (200, 620, 820, 1140))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(scales, (820, 620, 1130, 1140))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(scales, (1130, 620, 1280, 1140))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(int, (s * 1280, s * 620, s * 1520, s * 1140))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(int, (s * 1520, s * 620, s * 1760, s * 1140))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(int, (s * 1760, s * 620, s * 2120, s * 1140))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(int, (s * 2120, s * 620, s * 2250, s * 1140))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(int, (s * 2250, s * 620, s * 2600, s * 1140))), outline=rec_color, width=width)

    middle_rows = rows
    middle_cols = 8
    strs_list = ['货物或应税劳务、服务名称', '规格型号', '单位',
                 '数量', '单价', '金额', '税率', '税额']
    x_list = list(map(scales,[250, 900, 1170, 1350, 1580, 1860, 2150, 2340]))
    y = int(s*630)
    for j in range(middle_cols):
        tmp_str1 = strs_list[j]
        x = x_list[j]
        text_str2_1_1 = TextString(text_string=tmp_str1, font=font_path, char_size=char_size,
                                   color=font_color, direction='ltr', line_space=0, char_space=0)
        canvas.draw_text_string(text_str2_1_1, (x, y))
        bbox = canvas.get_bbox(text_str2_1_1)[0]
        tmp = {'transcription': text_str2_1_1.text,
               'points': [[bbox[0][0] - bbox_offset, bbox[0][1] - bbox_offset],
                          [bbox[0][2] + bbox_offset, bbox[0][1] - bbox_offset],
                          [bbox[0][2] + bbox_offset, bbox[0][3] + bbox_offset],
                          [bbox[0][0] - bbox_offset, bbox[0][3] + bbox_offset]]}
        # canvas.draw_rectangle(bbox[0][0], outline='red', width=width)
        label.append(tmp)

    for i in range(middle_rows):
        tmp_str = get_string(char_dict, 10, (1, 100)) + '\n' + \
                    get_string(char_dict, random.randint(0,3), (1, 100))
        val_text = TextString(tmp_str, font_path, char_size=char_size)
        val = CharsPic(val_text)
        val.gen_pic(isblur=False, isnosie=True, bboxon=False)
        offset2 = 50
        canvas.paste_img(val.pic, (x_list[0] + int(offset2 * s), y + int(offset2 * s)))
        tmp = {'transcription': val_text.text,
               'points': [[x_list[0] + int(offset2 * s) - bbox_offset, y + int(offset2 * s) - bbox_offset],
                          [x_list[0] + int(offset2 * s) + val.pic.size[0] + bbox_offset,
                           y + int(offset2 * s) - bbox_offset],
                          [x_list[0] + int(offset2 * s) + val.pic.size[0] + bbox_offset,
                           y + int(offset2 * s) + val.pic.size[1] + bbox_offset],
                          [x_list[0] + int(offset2 * s) - bbox_offset,
                           bbox_offset + y + int(offset2 * s) + val.pic.size[1]]]}
        label.append(tmp)

        tmp_str = "-" + get_string(char_dict_num2, 1, (1, 10)) + '.' + get_string(char_dict_num2, 1, (1, 10))
        val_text = TextString(tmp_str, font_path, char_size=char_size)
        val = CharsPic(val_text)
        val.gen_pic(isblur=False, isnosie=True, bboxon=False)
        offset2 = 50
        canvas.paste_img(val.pic, (x_list[1] + int(offset2 * s), y + int(offset2 * s)))
        tmp = {'transcription': val_text.text,
               'points': [
                   [x_list[1] + int(offset2 * s) - bbox_offset, y + int(offset2 * s) - bbox_offset],
                   [x_list[1] + int(offset2 * s) + val.pic.size[0] + bbox_offset,
                    y + int(offset2 * s) - bbox_offset],
                   [x_list[1] + int(offset2 * s) + val.pic.size[0] + bbox_offset,
                    y + int(offset2 * s) + val.pic.size[1] + bbox_offset],
                   [x_list[1] + int(offset2 * s) - bbox_offset,
                    bbox_offset + y + int(offset2 * s) + val.pic.size[1]]]}
        label.append(tmp)

        tmp_str = '1'
        val_text = TextString(tmp_str, font_path2, char_size=int(char_size * 0.6))
        val = CharsPic(val_text)
        val.gen_pic(isblur=False, isnosie=True, bboxon=False)
        offset2 = 55
        canvas.paste_img(val.pic, (x_list[2] + int(s * offset2), y + int(s * offset2)))

        tmp = {'transcription': val_text.text,
               'points': [[x_list[2] + int(s * offset2) - bbox_offset, y + int(s * offset2) - bbox_offset],
                          [x_list[2] + int(s * offset2) + val.pic.size[0] + bbox_offset,
                           y + int(s * offset2) - bbox_offset],
                          [x_list[2] + int(s * offset2) + val.pic.size[0] + bbox_offset,
                           y + int(s * offset2) + val.pic.size[1] + bbox_offset],
                          [x_list[2] + int(s * offset2) - bbox_offset,
                           y + int(s * offset2) + val.pic.size[1] + bbox_offset]]}
        label.append(tmp)

        tmp_str = get_string(char_dict_num2, 1, (1, 10))
        val_text = TextString(tmp_str, font_path2, char_size=int(char_size * 0.8))
        val = CharsPic(val_text)
        val.gen_pic(isblur=False, isnosie=True, bboxon=False)
        offset2 = 55
        canvas.paste_img(val.pic, (x_list[3] + int(s * offset2), y + int(s * offset2)))

        tmp = {'transcription': val_text.text,
               'points': [[x_list[3] + int(s * offset2) - bbox_offset, y + int(s * offset2) - bbox_offset],
                          [x_list[3] + int(s * offset2) + val.pic.size[0] + bbox_offset,
                           y + int(s * offset2) - bbox_offset],
                          [x_list[3] + int(s * offset2) + val.pic.size[0] + bbox_offset,
                           y + int(s * offset2) + val.pic.size[1] + bbox_offset],
                          [x_list[3] + int(s * offset2) - bbox_offset,
                           y + int(s * offset2) + val.pic.size[1] + bbox_offset]]}
        label.append(tmp)

        tmp_str1 = get_string(char_dict_num2, random.randint(2, 3), (1, 10))
        tmp_str2 = get_string(char_dict_num2, 2, (1, 10))
        tmp_str = tmp_str1 + '.' + tmp_str2
        val_text = TextString(tmp_str, font_path2, char_size=int(char_size * 0.8))
        val = CharsPic(val_text)
        val.gen_pic(isblur=False, isnosie=True, bboxon=False)
        offset2 = 55
        offset = random.randint(15, 25)
        canvas.paste_img(val.pic, (x_list[4] - int(s * offset), y + int(s * offset2)))
        tmp = {'transcription': val_text.text,
               'points': [[x_list[4] - int(s * offset) - bbox_offset, y + int(s * offset2) - bbox_offset],
                          [x_list[4] - int(s * offset) + val.pic.size[0] + bbox_offset,
                           y + int(s * offset2) - bbox_offset],
                          [x_list[4] - int(s * offset) + val.pic.size[0] + bbox_offset,
                           y + int(s * offset2) + val.pic.size[1] + bbox_offset],
                          [x_list[4] - int(s * offset) - bbox_offset,
                           y + int(s * offset2) + val.pic.size[1] + bbox_offset]]}
        label.append(tmp)

        tmp_str1 = get_string(char_dict_num2, random.randint(2, 5), (1, 10))
        tmp_str2 = get_string(char_dict_num2, 2, (1, 10))
        tmp_str = tmp_str1 + '.' + tmp_str2
        val_text = TextString(tmp_str, font_path2, char_size=int(char_size * 0.8))
        val = CharsPic(val_text)
        val.gen_pic(isblur=False, isnosie=True, bboxon=False)
        offset2 = 55
        offset = random.randint(25, 35)
        canvas.paste_img(val.pic, (x_list[5] + int(s * offset), y + int(s * offset2)))
        tmp = {'transcription': val_text.text,
               'points': [[x_list[5] + int(s * offset) - bbox_offset,
                           y + int(s * offset2) - bbox_offset],
                          [x_list[5] + int(s * offset) + val.pic.size[0] + bbox_offset,
                           y + int(s * offset2) - bbox_offset],
                          [x_list[5] + int(s * offset) + val.pic.size[0] + bbox_offset,
                           y + int(s * offset2) + val.pic.size[1] + bbox_offset],
                          [x_list[5] + int(s * offset) - bbox_offset,
                           y + int(s * offset2) + val.pic.size[1] + bbox_offset]]}
        label.append(tmp)

        tmp_str = get_string(char_dict_num2, random.randint(1, 2), (1, 10)) + '%'
        val_text = TextString(tmp_str, font_path, char_size=int(char_size * 0.8))
        val = CharsPic(val_text)
        val.gen_pic(isblur=False, isnosie=True, bboxon=False)
        offset2 = 55
        offset = random.randint(20, 30)
        canvas.paste_img(val.pic, (x_list[6] + int(s * offset), y + int(s * offset2)))
        tmp = {'transcription': val_text.text,
               'points': [[x_list[6] + int(s * offset) - bbox_offset, y + int(s * offset2) - bbox_offset],
                          [x_list[6] + int(s * offset) + val.pic.size[0] + bbox_offset,
                           y + int(s * offset2) - bbox_offset],
                          [x_list[6] + int(s * offset) + val.pic.size[0] + bbox_offset,
                           y + int(s * offset2) + val.pic.size[1] + bbox_offset],
                          [x_list[6] + int(s * offset) - bbox_offset,
                           y + int(s * offset2) + val.pic.size[1] + bbox_offset]]}
        label.append(tmp)

        tmp_str1 = get_string(char_dict_num2, random.randint(2, 5), (1, 10))
        tmp_str2 = get_string(char_dict_num2, 2, (1, 10))
        tmp_str = tmp_str1 + '.' + tmp_str2
        val_text = TextString(tmp_str, font_path2, char_size=int(char_size * 0.8))
        val = CharsPic(val_text)
        val.gen_pic(isblur=False, isnosie=True, bboxon=False)
        offset2 = 55
        offset = random.randint(25, 35)
        canvas.paste_img(val.pic, (x_list[7] + int(s * offset), y + int(s * offset2)))

        tmp = {'transcription': val_text.text,
               'points': [[x_list[7] + int(s * offset) - bbox_offset,
                           y + int(s * offset2) - bbox_offset],
                          [x_list[7] + int(s * offset) + val.pic.size[0] + bbox_offset,
                           y + int(s * offset2) - bbox_offset],
                          [x_list[7] + int(s * offset) + val.pic.size[0] + bbox_offset,
                           y + int(s * offset2) + val.pic.size[1] + bbox_offset],
                          [x_list[7] + int(s * offset) - bbox_offset,
                           y + int(s * offset2) + val.pic.size[1] + bbox_offset]]}
        label.append(tmp)
        y = y + val.pic.size[1] +int(s * offset2)

    str2_1_2 = '合计'
    text_str2_1_2 = TextString(text_string=str2_1_2, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=int(s*120))
    canvas.draw_text_string(text_str2_1_2, tuple(map(scales, (365, 1080))))

    bbox1 = text_str2_1_2.get_bbox()
    tmp = {'transcription': str2_1_2,
           'points': [[bbox1[0][0] - bbox_offset, bbox1[0][1] - bbox_offset],
                      [bbox1[0][2] + bbox_offset, bbox1[0][1] - bbox_offset],
                      [bbox1[0][2] + bbox_offset, bbox1[0][3] + bbox_offset],
                      [bbox1[0][0] - bbox_offset, bbox1[0][3] + bbox_offset]]}
    label.append(tmp)
    label.extend([{'transcription': []}] * 4)

    y = int(s*1080)
    tmp_str1 = '￥' + get_string(char_dict_num2, random.randint(2, 5), (1, 10))
    tmp_str2 = '.' + get_string(char_dict_num2, 2, (1, 10))
    val_text1 = TextString(tmp_str1, font_path, char_size=char_size)
    val_text2 = TextString(tmp_str2, font_path, char_size=char_size)
    val1 = CharsPic(val_text1)
    val2 = CharsPic(val_text2)
    val1.gen_pic(isblur=False, isnosie=True, bboxon=False)
    val2.gen_pic(isblur=False, isnosie=True, bboxon=False)
    val = val1.concatenate(val2.pic)
    canvas.paste_img(val, (x_list[5], y))
    tmp = {'transcription': val_text1.text + val_text2.text,
           'points': [[x_list[5] - bbox_offset, y - bbox_offset],
                      [x_list[5] + val.size[0] + bbox_offset, y - bbox_offset],
                      [x_list[5] + val.size[0] + bbox_offset, y + val.size[1] + bbox_offset],
                      [x_list[5] - bbox_offset, y + val.size[1] + bbox_offset]]}
    label.append(tmp)
    label.append({'transcription': []})

    tmp_str1 = '￥' + get_string(char_dict_num2, random.randint(2, 5), (1, 10))
    tmp_str2 = '.' + get_string(char_dict_num2, 2, (1, 10))
    val_text1 = TextString(tmp_str1, font_path, char_size=char_size)
    val_text2 = TextString(tmp_str2, font_path, char_size=char_size)
    val1 = CharsPic(val_text1)
    val2 = CharsPic(val_text2)
    val1.gen_pic(isblur=False, isnosie=True, bboxon=False)
    val2.gen_pic(isblur=False, isnosie=True, bboxon=False)
    val = val1.concatenate(val2.pic)
    canvas.paste_img(val, (x, y))
    tmp = {'transcription': val_text1.text + val_text2.text,
           'points': [[x_list[7] - bbox_offset, y - bbox_offset], [x + val.size[0] + bbox_offset, y - bbox_offset],
                      [x_list[7] + val.size[0] + bbox_offset, y + val.size[1] + bbox_offset],
                      [x_list[7] - bbox_offset, y + val.size[1] + bbox_offset]]}
    label.append(tmp)

    # 第三行
    canvas.draw_rectangle(tuple(map(scales, (200, 1140, 820, 1240))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(scales, (820, 1140, 2600, 1240))), outline=rec_color, width=width)

    str3_1_1 = '价税合计（大写）'
    text_str3_1_1 = TextString(text_string=str3_1_1, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=int(s * 10))
    canvas.draw_text_string(text_str3_1_1, tuple(map(scales, (330, 1160))))

    bbox = text_str3_1_1.get_bbox()
    tmp = {'transcription': text_str3_1_1.text,
           'points': [[bbox[0][0] - bbox_offset, bbox[0][1] - bbox_offset],
                      [bbox[0][2] + bbox_offset, bbox[0][1] - bbox_offset],
                      [bbox[0][2] + bbox_offset, bbox[0][3] + bbox_offset],
                      [bbox[0][0] - bbox_offset, bbox[0][3] + bbox_offset]]}
    label.append(tmp)

    tmp_dict = get_dict('./utils/dict/fanti_nums.txt')
    tmp_str = get_string(tmp_dict, random.randint(12, 20), (1, 19))
    val_text = TextString(tmp_str, font_path, char_size=int(char_size * 0.8))
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    offset2 = random.randint(820, 870)
    canvas.paste_img(val.pic, (int(s * offset2), bbox[0][1]))
    tmp = {'transcription': val_text.text,
           'points': [[int(s * offset2) - bbox_offset, bbox[0][1] - bbox_offset],
                      [int(s * offset2) + val.pic.size[0] + bbox_offset, bbox[0][1] - bbox_offset],
                      [int(s * offset2) + val.pic.size[0] + bbox_offset,
                       bbox_offset + bbox[0][1] + val.pic.size[1]],
                      [int(s * offset2) - bbox_offset, bbox[0][1] + val.pic.size[1] + bbox_offset]]}
    label.append(tmp)

    str3_2_1 = '（小写）'
    text_str3_2_1 = TextString(text_string=str3_2_1, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=int(s * 10))
    canvas.draw_text_string(text_str3_2_1, tuple(map(scales, (1920, 1160))))
    bbox = text_str3_2_1.get_bbox()


    tmp_str1 = get_string(char_dict_num2, random.randint(2, 5), (1, 10))
    tmp_str2 = get_string(char_dict_num2, 2, (1, 10))
    tmp_str = '￥' + tmp_str1 + '.' + tmp_str2
    val_text = TextString(tmp_str, font_path, char_size=int(char_size * 0.8))
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][2], bbox[0][1]))
    tmp = {'transcription': str3_2_1 + val_text.text,
           'points': [[bbox[0][0] - bbox_offset, bbox[0][1] - bbox_offset],
                      [bbox[0][2] + val.pic.size[0] + bbox_offset, bbox[0][1] - bbox_offset],
                      [bbox[0][2] + val.pic.size[0] + bbox_offset, bbox[0][3] + bbox_offset],
                      [bbox[0][0] - bbox_offset, bbox[0][3] + bbox_offset]]}
    label.append(tmp)

    # 第四行
    canvas.draw_rectangle(tuple(map(scales, (200, 1240, 290, 1500))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(scales, (290, 1240, 1580, 1500))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(scales, (1580, 1240, 1640, 1500))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(scales, (1640, 1240, 2600, 1500))), outline=rec_color, width=width)

    str4_1 = '销售方'
    text_str4_1 = TextString(text_string=str4_1, font=font_path, char_size=char_size,
                             color=font_color, direction='ttb', line_space=0, char_space=int(s*40))
    canvas.draw_text_string(text_str4_1, tuple(map(scales, (230, 1280))))

    bbox1 = text_str4_1.get_bbox()

    tmp = {'transcription': str4_1,
           'points': [[bbox1[0][0] - bbox_offset, bbox1[0][1] - bbox_offset],
                      [bbox1[0][2] + bbox_offset, bbox1[0][1] - bbox_offset],
                      [bbox1[0][2] + bbox_offset, bbox1[0][3] + bbox_offset],
                      [bbox1[0][0] - bbox_offset, bbox1[0][3] + bbox_offset]]}
    # canvas.draw_rectangle(bbox[0], outline='red', width=3)
    label.append(tmp)

    str4_2_1 = '名'
    text_str4_2_1 = TextString(text_string=str4_2_1, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str4_2_1, tuple(map(scales, (305, 1250))))
    bbox1 = text_str4_2_1.get_bbox()

    str4_2_1_2 = '称：'
    text_str4_2_1_2 = TextString(text_string=str4_2_1_2, font=font_path, char_size=char_size,
                                 color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str4_2_1_2, tuple(map(scales, (495, 1250))))

    bbox = text_str4_2_1_2.get_bbox()
    tmp_str = get_string(char_dict, random.randint(10, 20), (1, 100))
    val_text = TextString(tmp_str, font_path, char_size=int(char_size))
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][2] + 1, bbox[0][1]))
    tmp = {'transcription': str4_2_1 + str4_2_1_2 + val_text.text,
           'points': [[bbox1[0][0] + 1 - bbox_offset, bbox1[0][1] - bbox_offset],
                      [bbox[0][2] + 1 + val.pic.size[0] + bbox_offset, bbox1[0][1] - bbox_offset],
                      [bbox[0][2] + 1 + val.pic.size[0] + bbox_offset, bbox[0][1] + val.pic.size[1] + bbox_offset],
                      [bbox1[0][0] + 1 - bbox_offset, bbox[0][1] + val.pic.size[1] + bbox_offset]]}
    label.append(tmp)

    str5_1 = '备注'
    text_str5_1 = TextString(text_string=str5_1, font=font_path, char_size=char_size,
                             color=font_color, direction='ttb', line_space=0, char_space=int(s*90))
    canvas.draw_text_string(text_str5_1, tuple(map(scales, (1590, 1280))))

    bbox1 = text_str5_1.get_bbox()

    tmp = {'transcription': str5_1,
           'points': [[bbox1[0][0] - bbox_offset, bbox1[0][1] - bbox_offset],
                      [bbox1[0][2] + bbox_offset, bbox1[0][1] - bbox_offset],
                      [bbox1[0][2] + bbox_offset, bbox1[0][3] + bbox_offset],
                      [bbox1[0][0] - bbox_offset, bbox1[0][3] + bbox_offset]]}
    label.append(tmp)
    label.append({'transcription': []})

    str4_2_2 = '纳税人识别号：'
    text_str4_2_2 = TextString(text_string=str4_2_2, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str4_2_2, tuple(map(scales, (305, 1315))))

    bbox = text_str4_2_2.get_bbox()

    tmp_str = get_string(char_dict_num2, 18, (1, 10))
    val_text = TextString(tmp_str, font_path2, char_size=int(char_size * 0.8))
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][2], bbox[0][1]))
    tmp = {'transcription': str4_2_2 + val_text.text,
           'points': [[bbox[0][0] - bbox_offset, bbox[0][1] - bbox_offset],
                      [bbox[0][2] + val.pic.size[0] + bbox_offset, bbox[0][1] - bbox_offset],
                      [bbox[0][2] + val.pic.size[0] + bbox_offset, max(bbox[0][3], val.pic.size[1]) + bbox_offset],
                      [bbox[0][0] - bbox_offset, max(bbox[0][3], val.pic.size[1]) + bbox_offset]]}
    label.append(tmp)

    str4_2_3 = '地址、电话:'
    text_str4_2_3 = TextString(text_string=str4_2_3, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=8)
    canvas.draw_text_string(text_str4_2_3, tuple(map(scales, (305, 1375))))
    bbox = text_str4_2_3.get_bbox()

    tmp_str = get_string(char_dict, random.randint(8, 16), (1, 100))
    val_text1 = TextString(tmp_str, font_path, char_size=int(char_size * 0.8))
    # val_text1 = TextString('电动机我记得叫我定位', font_path, char_size=int(s * 40))
    val1 = CharsPic(val_text1)
    val1.gen_pic(isblur=False, isnosie=True, bboxon=False)
    w, h = val1.pic.size
    canvas.paste_img(val1.pic, (bbox[0][2], bbox[0][1]))

    tmp_str = get_string(char_dict_num2, random.randint(10, 16), (1, 10))
    val_text = TextString(tmp_str, font_path2, char_size=int(char_size * 0.8))
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    offset2 = random.randint(45, 55)
    offset = 0
    canvas.paste_img(val.pic, (bbox[0][2] + int(s * offset2) + w, bbox[0][1] + int(s * offset)))

    tmp = {'transcription': str4_2_3 + val_text1.text + val_text.text,
           'points': [[bbox[0][0] - bbox_offset, bbox[0][1] - bbox_offset],
                      [bbox[0][2] + int(s * offset2) + w + val.pic.size[0] + bbox_offset,
                       bbox[0][1] - bbox_offset],
                      [bbox[0][2] + int(s * offset2) + w + val.pic.size[0] + bbox_offset,
                       bbox[0][3] + bbox_offset],
                      [bbox[0][0] - bbox_offset, bbox[0][3] + bbox_offset]]}
    label.append(tmp)

    str4_2_4 = '开户行及账号：'
    text_str4_2_4 = TextString(text_string=str4_2_4, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str4_2_4, tuple(map(scales, (305, 1440))))

    bbox = text_str4_2_4.get_bbox()

    tmp_str = get_string(char_dict, random.randint(8, 20), (1, 100))
    val_text1 = TextString(tmp_str, font_path, char_size=int(char_size * 0.8))
    val1 = CharsPic(val_text1)
    val1.gen_pic(isblur=False, isnosie=True, bboxon=False)
    w, h = val1.pic.size
    canvas.paste_img(val1.pic, (bbox[0][2], bbox[0][1]))

    tmp_str = get_string(char_dict_num2, random.randint(10, 16), (1, 10))
    val_text = TextString(tmp_str, font_path2, char_size=int(char_size * 0.8))
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    offset2 = random.randint(45, 55)
    offset = 0
    canvas.paste_img(val.pic, (bbox[0][2] + int(s * offset2) + w, bbox[0][1] + int(s * offset)))

    tmp = {'transcription': str4_2_4 + val_text1.text + val_text.text,
           'points': [[bbox[0][0] - bbox_offset, bbox[0][1] - bbox_offset],
                      [bbox[0][2] + int(s * offset2) + w + val.pic.size[0] + bbox_offset, bbox[0][1] - bbox_offset],
                      [bbox[0][2] + int(s * offset2) + w + val.pic.size[0] + bbox_offset,
                       bbox[0][3] + bbox_offset],
                      [bbox[0][0] - bbox_offset, bbox[0][3] + bbox_offset]]}
    label.append(tmp)

    del str1_2_1, text_str1_2_1_2, str1_2_1_2
    del str1_2_2, text_str1_2_2, str1_2_3, text_str1_2_3, text_str1_2_4
    del text_str1_3_1, text_str2_1_2, text_str2_1_1
    del text_str3_2_1, text_str3_1_1,text_str4_1,
    del text_str4_2_4, text_str4_2_3, text_str4_2_2, text_str4_2_1, text_str4_2_1_2
    del text_str1_1, text_str1_2_1, text_str5_1,
    del tmp, val_text, val_text1, val_text2, val, val1, val2
    del bbox, bbox1, bbox2,

    output_dir = imgs_dir + basename
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        os.chmod(output_dir, 0o777)
        os.chmod(imgs_dir, 0o777)
    img_name = '%05d.jpg' % img_name
    img_path = os.path.join(imgs_dir, basename, img_name)
    # print(img_path)
    logger.info(img_path)
    # 校验文本框坐标位置
    for tmp_label in label:
        tmp_bbox = tmp_label.get('points', None)
        if tmp_bbox is None:
            continue
        tmp1 = tmp_bbox[1][0] - tmp_bbox[0][0]
        tmp2 = tmp_bbox[2][0] - tmp_bbox[3][0]
        h1 = tmp_bbox[3][1] - tmp_bbox[0][1]
        h2 = tmp_bbox[2][1] - tmp_bbox[1][1]
        try:
            assert tmp1 == tmp2, '%s the width of bbox should be equally' % tmp_label['transcription']
        except:
            print(tmp_label['transcription'], tmp_bbox)
            break
        try:
            assert h1 == h2, '%s the height of bbox should be equally' % tmp_label['transcription']
        except:
            print(tmp_label['transcription'], tmp_bbox)
            break
    # canvas = rectangle(canvas, label)
    canvas.save(img_path)

    # print(label)
    return [basename + img_name, label]


def gen_recepits_html(labels, dt='train', index=None):
    # label_jsonl = './test_receipts.jsonl'
    # print('saved in ',fp)
    # label_jsonl = fp
    lines = []

    for i, label in enumerate(labels):
        line = {}
        structure = get_html_ele(index[i])
        filename = os.path.basename(label[0])
        line['filename'] = filename
        line['split'] = dt
        line['imgid'] = i
        cells = []
        for item in label[1]:
            content = item['transcription']
            points = item.get('points', None)
            if points != None:
                tmp_ = {"tokens": [char for char in content],
                        "bbox": [points[0][0], points[0][1], points[2][0], points[2][1]]}
            elif points is None:
                tmp_ = {"tokens": [char for char in content]}

            cells.append(tmp_)
        html = {"cells": cells,
                "structure": {"tokens": structure}
                }
        line['html'] = html

        lines.append(line)

    return lines


def rectangle(canvas, labels):
    for label in labels:
        bbox = label.get('points', None)
        if bbox is None:
            continue
        canvas.draw_rectangle([(bbox[0][0], bbox[0][1]), (bbox[2][0], bbox[2][1])], outline='red', width=2)
    return canvas


def get_html_ele(i):
    # html = '../utils/dict/receipts_html_dict.txt'
    # html = './tools/receipts.html'
    html = './tools/receipt_std_htmls/receipts%d.html' % i
    with open(html, 'r') as fr:
        ele_str = fr.readlines()
    html_string = ''
    for i, ele in enumerate(ele_str):
        tmp_ele = ele.strip(' ').strip('\n')
        html_string += tmp_ele

    thead_list = list(re.finditer(r'(<thead>).*(</thead>)', html_string))
    tbody_list = list(re.finditer(r'(<tbody>).*(</tbody>)', html_string))
    thead_structure = get_eles(thead_list, kind='<thead>')
    tbody_structure = get_eles(tbody_list, kind='<tbody>')

    html_structure = thead_structure + tbody_structure

    return html_structure


def get_eles(thead_list, kind='<thead>'):
    structure = [kind, ]
    thead_strs = ''.join(l.group() for l in thead_list)
    thead_rows = list(re.finditer(r'<tr>([\s\S]*?)</tr>', thead_strs))
    tr_list = []
    s1 = '<td'
    s2 = '>'
    s3 = '</td>'
    for row in thead_rows:
        tmp_tr_list = ['<tr>']
        row = ''.join(row.group())
        tmp_cells = list(re.finditer(r'(<td[^<>]*>)(</td>)', row))
        for cell in tmp_cells:
            is_colspan = list(re.finditer(r'( colspan="\d)"', cell.group(1)))
            is_rowspan = list(re.finditer(r'( rowspan="\d)"', cell.group(1)))
            if len(is_rowspan) == 1 and len(is_colspan) == 0:
                span = is_rowspan[0].group()
                tmp_tr_list.extend([s1, span, s2, s3])
            elif len(is_colspan) == 1 and len(is_rowspan) == 0:
                span = is_colspan[0].group()
                tmp_tr_list.extend([s1, span, s2, s3])
            elif len(is_colspan) == 1 and len(is_rowspan) == 1:
                rowspan_indx = is_rowspan[0].span()
                colspan_indx = is_colspan[0].span()
                colspan = is_colspan[0].group()
                rowspan = is_rowspan[0].group()
                if rowspan_indx[0] < colspan_indx[0]:
                    tmp_tr_list.extend([s1, rowspan, colspan, s2, s3])
                else:
                    tmp_tr_list.extend([s1, colspan, rowspan, s2, s3])
            else:
                tmp_tr_list.extend([cell.group(1), cell.group(2)])
        tmp_tr_list.append('</tr>')
        tr_list.extend(tmp_tr_list)

    structure.extend(tr_list)
    if kind == '<thead>':
        structure.append('</thead>')
    elif kind == '<tbody>':
        structure.append('</tbody>')

    return structure


def format_html():
    """
    Formats HTML code from tokenized annotation of img
    测试表格标注是否正确
    """
    from bs4 import BeautifulSoup as bs
    import jsonlines
    f = '/Users/zhouqiang/YaSpeed/Table_renderer/receipts/receipts_train_labels_2_v3.jsonl'
    htmls_dir = '/Users/zhouqiang/YaSpeed/Table_renderer/receipts/htmls/'
    if not os.path.exists(htmls_dir):
        os.makedirs(htmls_dir)

    with open(f, 'r') as fp:
        for item in jsonlines.Reader(fp):
            structure = item['html']['structure']['tokens']

            html_string = '''<html>
                             <head>
                             <meta charset="UTF-8">
                             <style>
                             table, th, td {
                               border: 1px solid black;
                               font-size: 10px;
                             }
                             </style>
                             </head>
                             <body>
                             <table frame="hsides" rules="groups" width="100%%">
                                 %s
                             </table>
                             </body>
                             </html>''' % ''.join(structure)
            cell_nodes = list(re.finditer(r'(<td[^<>]*>)(</td>)', html_string))
            assert len(cell_nodes) == len(
                item['html']['cells']), 'Number of cells defined in tags does not match the length of cells'
            cells = [''.join(c['tokens']) for c in item['html']['cells']]
            offset = 0
            for n, cell in zip(cell_nodes, cells):
                # 将数据填入对应单元格，第一个分组的结束，第二个分组的开始
                html_string = html_string[:n.end(1) + offset] + cell + html_string[n.start(2) + offset:]
                offset += len(cell)
            soup = bs(html_string, features="html.parser")
            html_string = soup.prettify()
            filename = item['filename'][:-3]+'html'
            with open(htmls_dir+filename, 'w') as fw:
                fw.write(html_string)


if __name__ == '__main__':
    # get_html_ele(1)
    format_html()

#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
"""
@author:zhouqiang
@file:images.py
@NAME:Table_renderer
@time:2021/09/24
@IDE: PyCharm
 
"""

import random

from Canvas.Canvas import *
from TextString.TextString import *
from utils.utils import *
from configure.Config import *
from log.log import *


def gen_text_strings():
    config = set_config()
    # font2 = './fonts/fangzheng_heiti.ttf'
    font_type = config['font']
    font_color = config['font_color']
    dict_file = config['dict_file']
    char_dict = get_dict(fp=dict_file)
    n = len(char_dict)
    print('字典字符个数为：', n)

    # 字体大小20-22
    char_size = config['char_size']
    h_char_space = config['h_char_size']
    v_char_space = random.randint(25, 40)
    # 一张图随机产生5-20个文本框
    text_str_n = random.randint(10, 20)
    # 汉字按1：3产生
    # h_n = int(text_str_n // 4)
    # 数字符号全是横着的
    v_n = 0
    h_n = text_str_n

    # 水平产生3-20以内的随机长度的字符串,
    h_length_list = get_length(h_n, 'ltr', kind='sym')
    # 垂直产生2-9以内的随机长度的字符串,
    v_length_list = get_length(v_n, 'ttb')
    # v_length_list = 10
    text_strs_dict = {'ltr': h_length_list, 'ttb': v_length_list}
    text_strs = {}
    text_strs1 = []
    # 产生水平的TextString
    for h_length in text_strs_dict['ltr']:
        text_str1 = get_string(char_dict, length=h_length, range_t=(1, 90))

        text_string1 = TextString(text_string=text_str1, font=font_type, char_size=char_size,
                                  color=font_color, direction='ltr', line_space=0, char_space=random.randint(0, 2))
        text_strs1.append(text_string1)
    text_strs['ltr'] = text_strs1

    text_strs2 = []
    # 产生垂直类的TextString
    for v_length in text_strs_dict['ttb']:
        text_str2 = get_string(char_dict, length=v_length, range_t=(1, 89))
        text_string2 = TextString(text_string=text_str2, font=font_type, char_size=char_size,
                                  color=font_color, direction='ttb', line_space=0, char_space=0)
        text_strs2.append(text_string2)

    text_strs['ttb'] = text_strs2
    return text_strs


def gen_image(index=1, img_path=None, label_path=None):
    # 产生字符串
    text_strs = gen_text_strings()
    # 产生随机坐标xy
    tmp = get_coordxy2(text_strs)
    img_size = (1280, 720)

    bg_color = 'white'
    bg_image = CanvasImage(size=img_size, color=bg_color)

    all_bboxes = []
    text_bboxes = []

    for i, ele in enumerate(tmp):
        # print('line 112:the string is', ele[0].text, ele[0].coord_xy)
        bg_image.draw_text_string(ele[0], ele[0].coord_xy, )
        bboxes, char_bbox = bg_image.draw_bbox(ele[0], offset=random.randint(12, 16), color='black')
        # bg_image.draw_bbox(ele[0], offset=2, color='black')
        # all_bboxes.append(bboxes)
        # text_bboxes.append(char_bbox)
        all_bboxes += bboxes
        text_bboxes += char_bbox
    # print(len(all_bboxes))
    # print(len(text_bboxes))

    image_name = '%05d' % index
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    bg_image.save(img_path + image_name + '.jpg')
    print('line 278 ；all_bboxes：', all_bboxes)
    print('line 282 ；text_bboxes：', text_bboxes)
    get_labels(bboxes=text_bboxes, filename=image_name, fp=label_path)


# def gen_batch_images():
#     batch = 10
#     # path1 = './images_%s/' % str(batch)
#     path1 = './images_%s/' % str(batch)
#     path2 = './labels_%s/' % str(batch)
#
#     for i in range(batch):
#         print('line 293 i:', i)
#         gen_image(i, img_path=path1, label_path=path2)





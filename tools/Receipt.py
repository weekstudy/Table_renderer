#! /usr/bin/python3
# -*- coding:UTF-8 -*-

import os
import sys
import random
import yaml
import pdb

sys.path.append('..')
sys.path.append('.')

from TextString.TextString import *
from utils.utils import *
from Canvas.Canvas import *
from tools.TextImage import *
from tools.charspic import *


def receipt(imgs_dir, basename, img_name, logger):
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
    width = 2
    bbox_offset = int(10*s)
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

    # str1 = '湖北增值税专用发票'
    province_dict = get_dict('./utils/dict/provinces.txt')
    str1 = get_string(province_dict, 1, (1, 27)) + '增值税专用发票'

    # str1 = '藹靄聱螯謷鳌鏖'
    text_str1 = TextString(text_string=str1, font=font_path, char_size=int(65 * s),
                           color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str1, tuple(map(int, (1040 * s, 100 * s))))
    bbox = text_str1.get_bbox()
    tmp = {'transcription': text_str1.text,
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][3]+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox[0][3]+bbox_offset]]}
    label.append(tmp)
    canvas.draw_multilines(tuple(map(int, (1000 * s, 220 * s, 1700 * s, 220 * s))), font_color, offset=int(10 * s),
                           width=width)

    text_str_left = TextString('机器编码:', font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str_left, tuple(map(int, (200 * s, 300 * s))))
    bbox = text_str_left.get_bbox()

    tmp_str = get_string(char_dict_num2, 12, (1, 10))
    val_text = TextString(tmp_str, font_path, char_size=int(char_size * 0.8))
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    offset = 0
    canvas.paste_img(val.pic, (bbox[0][2], bbox[0][1] + int(offset * s)))

    tmp = {'transcription': text_str_left.text + val.text,
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + val.pic.size[0]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + val.pic.size[0]+bbox_offset, bbox[0][3] + int(offset * s)+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox[0][3] + int(offset * s)+bbox_offset]]}
    label.append(tmp)

    text_str_right = TextString('校验码:', font=font_path, char_size=char_size,
                                color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str_right, tuple(map(int, (1970 * s, 220 * s))))
    bbox = text_str_right.get_bbox()

    tmp_str = ''
    for i in range(4):
        a = get_string(char_dict_num2, 5, (1, 10)) + ' '
        tmp_str += a
    val_text = TextString(tmp_str, font_path, char_size=int(char_size * 0.8))
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    offset = 0
    canvas.paste_img(val.pic, (bbox[0][2], bbox[0][1] + int(offset * s)))

    tmp = {'transcription': text_str_right.text + val.text,
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + val.pic.size[0]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + val.pic.size[0]+bbox_offset, bbox[0][3] + int(offset * s)+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox[0][3] + int(offset * s)+bbox_offset]]}
    label.append(tmp)

    text_str_right = TextString('发票代码:', font=font_path, char_size=char_size,
                                color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str_right, tuple(map(int, (1970 * s, 160 * s))))
    bbox = text_str_right.get_bbox()
    tmp_str = get_string(char_dict_num2, 12, (1, 10))
    val_text = TextString(tmp_str, font_path, char_size=int(char_size * 0.8))
    val = CharsPic(val_text)
    offset = 0
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][2], bbox[0][1] + int(offset * s)))

    tmp = {'transcription': text_str_right.text + val.text,
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + val.pic.size[0]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + val.pic.size[0]+bbox_offset, bbox[0][3] + int(offset * s)+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox[0][3] + int(offset * s)+bbox_offset]]}
    label.append(tmp)

    text_str_right = TextString('发票号码:', font=font_path, char_size=char_size,
                                color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str_right, tuple(map(int, (1970 * s, 100 * s))))
    bbox = text_str_right.get_bbox()
    tmp_str = get_string(char_dict_num2, 8, (1, 10))
    val_text = TextString(tmp_str, font_path, char_size=int(char_size * 0.8))
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    offset = 0
    canvas.paste_img(val.pic, (bbox[0][2], bbox[0][1] + int(offset * s)))

    tmp = {'transcription': text_str_right.text + val.text,
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + val.pic.size[0]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + val.pic.size[0]+bbox_offset, bbox[0][3] + int(offset * s)+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox[0][3] + int(offset * s)+bbox_offset]]}
    label.append(tmp)

    # 整个大框
    canvas.draw_rectangle(tuple(map(scales, (200, 360, 2600, 1500))), fill='white', outline=rec_color,
                          width=width)
    # str_left = '税总函〔2019〕144号中钞华森实业公司'
    # str_left = Image.open('./r_result.jpg', )
    # str_left.resize()
    # canvas.paste_img(str_left, (150, 510))
    # canvas.paste_img(str_left, (150, 510))

    # str_right = '第三联：发票联 购买方记账凭证'
    # text_str_right = TextString(text_string=str_right, font=font_path, char_size=char_size,
    #                             color=font_color, direction='ttb', line_space=0, char_space=int(s * 10))
    # canvas.draw_text_string(text_str_right, tuple(map(int, (2610 * s, 620 * s))))
    # bbox = text_str_right.get_bbox()
    # tmp = {'transcription': text_str_right.text,
    #        'points': [[bbox[0][0], bbox[0][1]],
    #                   [bbox[0][2], bbox[0][1]],
    #                   [bbox[0][2], bbox[0][3]],
    #                   [bbox[0][0], bbox[0][3]]]}
    # # canvas.draw_rectangle(bbox[0], outline='red', width=3)
    # label.append(tmp)

    str0 = '开票日期：'
    text_str0 = TextString(text_string=str0, font=font_path, char_size=char_size,
                           color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str0, tuple(map(int, (1970 * s, 280 * s))))

    bbox = text_str0.get_bbox()
    m = '年%02d月%02d日' % (random.randint(1, 12), random.randint(1, 31))
    tmp_str = get_string(char_dict_num2, 4, (1, 10)) + m
    val_text = TextString(tmp_str, font_path, char_size=int(char_size * 0.8))
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    offset = 0
    canvas.paste_img(val.pic, (bbox[0][2], bbox[0][1] + int(offset * s)))

    tmp = {'transcription': str0 + val_text.text,
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + val.pic.size[0]+bbox_offset,
                       bbox[0][1]-bbox_offset],
                      [bbox[0][2] + val.pic.size[0]+bbox_offset,
                       bbox[0][1] + int(offset * s) + val.pic.size[1]+bbox_offset],
                      [bbox[0][0]-bbox_offset,
                       bbox[0][1] + int(offset * s) + val.pic.size[1]+bbox_offset]]}
    label.append(tmp)

    # 第一行
    canvas.draw_rectangle(tuple(map(int, (200 * s, 360 * s, 290 * s, 620 * s))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(int, (290 * s, 360 * s, 1580 * s, 620 * s))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(int, (1580 * s, 360 * s, 1640 * s, 620 * s))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(int, (1640 * s, 360 * s, 2600 * s, 620 * s))), outline=rec_color, width=width)

    str2 = '购'
    # str2 = get_string(char_dict,3,(1,100))
    text_str2 = TextString(text_string=str2, font=font_path, char_size=char_size,
                           color=font_color, direction='ttb', line_space=0, char_space=0)

    canvas.draw_text_string(text_str2, tuple(map(int, (s * 230, s * 400))))
    bbox = text_str2.get_bbox()
    tmp = {'transcription': text_str2.text,
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][3]+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox[0][3]+bbox_offset]]}
    # canvas.draw_rectangle(bbox[0], outline='red', width=3)
    label.append(tmp)

    str2 = '买'
    # str2 = get_string(char_dict,3,(1,100))
    text_str2 = TextString(text_string=str2, font=font_path, char_size=char_size,
                           color=font_color, direction='ttb', line_space=0, char_space=0)

    canvas.draw_text_string(text_str2, tuple(map(int, (s * 230, s * 480))))
    bbox = text_str2.get_bbox()
    tmp = {'transcription': text_str2.text,
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][3]+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox[0][3]+bbox_offset]]}
    # canvas.draw_rectangle(bbox[0], outline='red', width=3)
    label.append(tmp)

    str2 = '方'
    # str2 = get_string(char_dict,3,(1,100))
    text_str2 = TextString(text_string=str2, font=font_path, char_size=char_size,
                           color=font_color, direction='ttb', line_space=0, char_space=0)

    canvas.draw_text_string(text_str2, tuple(map(int, (s * 230, s * 550))))
    bbox = text_str2.get_bbox()
    tmp = {'transcription': text_str2.text,
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][3]+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox[0][3]+bbox_offset]]}
    # canvas.draw_rectangle(bbox[0], outline='red', width=3)
    label.append(tmp)

    str1_2_1 = '名'

    text_str1_2_1 = TextString(text_string=str1_2_1, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str1_2_1, tuple(map(scales, (305, 375))))

    bbox = text_str1_2_1.get_bbox()
    tmp = {'transcription': text_str1_2_1.text,
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][3]+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox[0][3]+bbox_offset]]}
    # canvas.draw_rectangle(bbox[0], outline='red', width=3)
    label.append(tmp)

    str1_2_1_2 = '称：'
    text_str1_2_1_2 = TextString(text_string=str1_2_1_2, font=font_path, char_size=char_size,
                                 color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str1_2_1_2, tuple(map(scales, (495, 375))))

    bbox = text_str1_2_1_2.get_bbox()
    tmp_str = get_string(char_dict, random.randint(8, 20), 300)
    val_text = TextString(tmp_str, font_path, char_size=char_size)
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][2] + 1, bbox[0][1]))

    tmp = {'transcription': str1_2_1_2 + val_text.text,
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + val.pic.size[0]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + val.pic.size[0]+bbox_offset, bbox[0][3]+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox[0][3]+bbox_offset]]}
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

    bbox2 = [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
             [bbox[0][2] + val.pic.size[0]+bbox_offset, bbox[0][1]-bbox_offset],
             [bbox[0][2] + val.pic.size[0]+bbox_offset, max(bbox[0][3], val.pic.size[1])+bbox_offset],
             [bbox[0][0]-bbox_offset, max(bbox[0][3], val.pic.size[1])+bbox_offset]]
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
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + int(s * offset2) + w + val.pic.size[0]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + + int(s * offset2) + w + val.pic.size[0]+bbox_offset,
                       bbox[0][1] + int(s * offset) + val.pic.size[1]+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox[0][1] + int(s * offset) + val.pic.size[1]+bbox_offset]]}

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
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + int(s * offset2) + w + val.pic.size[0]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + int(s * offset2) + w + val.pic.size[0]+bbox_offset,
                       bbox[0][1] + int(s * offset) + val.pic.size[1]+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox_offset+bbox[0][1] + int(s * offset) + val.pic.size[1]]]}
    label.append(tmp)

    str3 = '密'
    text_str3 = TextString(text_string=str3, font=font_path, char_size=char_size,
                           color=font_color, direction='ttb', line_space=0, char_space=0)
    canvas.draw_text_string(text_str3, tuple(map(int, (s * 1590, s * 400))))

    bbox = canvas.get_bbox(text_str3)[0]
    tmp = {'transcription': str3,
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][3]+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox[0][3]+bbox_offset]]}
    label.append(tmp)
    offset2 = random.randint(45, 55)
    x, y = (bbox[0][2] + int(s * offset2), int(bbox[0][1] - s * 5))
    str3 = '码'
    text_str3 = TextString(text_string=str3, font=font_path, char_size=char_size,
                           color=font_color, direction='ttb', line_space=0, char_space=0)
    canvas.draw_text_string(text_str3, tuple(map(int, (s * 1590, s * 480))))

    bbox = canvas.get_bbox(text_str3)[0]
    tmp = {'transcription': str3,
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][3]+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox[0][3]+bbox_offset]]}
    label.append(tmp)

    str3 = '区'
    text_str3 = TextString(text_string=str3, font=font_path, char_size=char_size,
                           color=font_color, direction='ttb', line_space=0, char_space=int(s * 35))
    canvas.draw_text_string(text_str3, tuple(map(int, (s * 1590, s * 550))))

    bbox = canvas.get_bbox(text_str3)[0]
    tmp = {'transcription': str3,
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][3]+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox[0][3]+bbox_offset]]}
    label.append(tmp)

    char_dict_num = get_dict(fp="./utils/dict/nums_dict.txt")
    for i in range(4):
        # font = '../fonts/Times New Roman.ttf'
        tmp_str = get_string(char_dict_num, 27, (1, 22))
        val_text = TextString(tmp_str, font_path, char_size=int(char_size * 1.2), char_space=int(s * 5))
        val = CharsPic(val_text)
        val.gen_pic(isblur=False, isnosie=True, bboxon=False)
        canvas.paste_img(val.pic, (x, y))
        w, h = val.pic.size
        tmp = {'transcription': tmp_str,
               'points': [[x-bbox_offset, y-bbox_offset],
                          [x + w+bbox_offset, y-bbox_offset],
                          [x + w+bbox_offset, y + h+bbox_offset],
                          [x-bbox_offset, y + h+bbox_offset]]}
        label.append(tmp)
        y += int(h + s * 15)

    # 第二行
    canvas.draw_rectangle(tuple(map(scales, (200, 620, 820, 1140))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(scales, (820, 620, 1130, 1140))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(scales, (1130, 620, 1280, 1140))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(int, (s * 1280, s * 620, s * 1520, s * 1140))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(int, (s * 1520, s * 620, s * 1760, s * 1140))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(int, (s * 1760, s * 620, s * 2120, s * 1140))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(int, (s * 2120, s * 620, s * 2250, s * 1140))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(int, (s * 2250, s * 620, s * 2600, s * 1140))), outline=rec_color, width=width)

    str2_1_1 = '货物或应税劳务、服务名称'
    text_str2_1_1 = TextString(text_string=str2_1_1, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str2_1_1, tuple(map(scales, (250, 630))))
    bbox = canvas.get_bbox(text_str2_1_1)[0]
    tmp = {'transcription': text_str2_1_1.text,
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][3]+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox[0][3]+bbox_offset]]}
    # canvas.draw_rectangle(bbox[0][0], outline='red', width=width)
    label.append(tmp)

    tmp_str = get_string(char_dict, 10, (1, 100))
    val_text = TextString(tmp_str, font_path, char_size=char_size)
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    offset2 = random.randint(45, 55)
    canvas.paste_img(val.pic, (bbox[0][0] + int(offset2 * s), bbox[0][1] + int(offset2 * s)))
    tmp = {'transcription': val_text.text,
           'points': [[bbox[0][0] + int(offset2 * s)-bbox_offset, bbox[0][1] + int(offset2 * s)-bbox_offset],
                      [bbox[0][0] + int(offset2 * s) + val.pic.size[0]+bbox_offset,
                       bbox[0][1] + int(offset2 * s)-bbox_offset],
                      [bbox[0][0] + int(offset2 * s) + val.pic.size[0]+bbox_offset,
                       bbox[0][1] + int(offset2 * s) + val.pic.size[1]+bbox_offset],
                      [bbox[0][0] + int(offset2 * s)-bbox_offset,
                       bbox_offset+bbox[0][1] + int(offset2 * s) + val.pic.size[1]]]}
    label.append(tmp)

    str2_1_2 = '合'
    text_str2_1_2 = TextString(text_string=str2_1_2, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str2_1_2, tuple(map(scales, (365, 1080))))

    bbox = canvas.get_bbox(text_str2_1_2)[0]
    tmp = {'transcription': text_str2_1_2.text,
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][3]+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox[0][3]+bbox_offset]]}
    # canvas.draw_rectangle(bbox[0][0], outline='red')
    label.append(tmp)

    str2_1_2_2 = '计'
    text_str2_1_2_2 = TextString(text_string=str2_1_2_2, font=font_path, char_size=char_size,
                                 color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str2_1_2_2, tuple(map(scales, (565, 1080))))

    bbox = canvas.get_bbox(text_str2_1_2_2)[0]
    tmp = {'transcription': text_str2_1_2_2.text,
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][3]+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox[0][3]+bbox_offset]]}
    # canvas.draw_rectangle(bbox[0][0], outline='red')
    label.append(tmp)

    str2_2_1 = '规格型号'
    text_str2_2_1 = TextString(text_string=str2_2_1, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str2_2_1, tuple(map(scales, (900, 630))))

    bbox = canvas.get_bbox(text_str2_2_1)[0]
    tmp = {'transcription': text_str2_2_1.text,
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][3]+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox[0][3]+bbox_offset]]}
    label.append(tmp)

    tmpx, tmpy = bbox[0][0], bbox[0][1] + int(s * offset2 + 15) + val.pic.size[1]
    for j in range(2):
        for i in range(5):
            tmp_str = "-" + get_string(char_dict_num2, 1, (1, 10)) + '.' + get_string(char_dict_num2, 1, (1, 10))
            val_text = TextString(tmp_str, font_path2, char_size=int(char_size * 0.8))
            val = CharsPic(val_text)
            val.gen_pic(isblur=False, isnosie=True, bboxon=False)
            offset2 = random.randint(40, 45)
            canvas.paste_img(val.pic, (tmpx, tmpy + int(i * (s * offset2))))

            tmp = {'transcription': val_text.text,
                   'points': [[tmpx-bbox_offset, tmpy + int(i * (s * offset2))-bbox_offset],
                              [tmpx + val.pic.size[0]+bbox_offset, tmpy + int(i * (s * offset2))-bbox_offset],
                              [tmpx + val.pic.size[0]+bbox_offset,
                               tmpy + int(i * (s * offset2)) + val.pic.size[1]+bbox_offset],
                              [tmpx-bbox_offset, tmpy + int(i * (s * offset2)) + val.pic.size[1]+bbox_offset]]}
            label.append(tmp)
            tmpy += int(s*20)
        tmpx, tmpy = bbox[0][0] + int(s * 150), bbox[0][1] + int(s * offset2 + 15) + val.pic.size[1]

    str2_2_1 = '单位'
    text_str2_2_1 = TextString(text_string=str2_2_1, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str2_2_1, tuple(map(scales, (1172, 630))))
    bbox = text_str2_2_1.get_bbox()
    tmp = {'transcription': text_str2_2_1.text,
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][3]+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox[0][3]+bbox_offset]]}

    label.append(tmp)

    tmp_str = '1'
    val_text = TextString(tmp_str, font_path2, char_size=int(char_size * 0.6))
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    offset2 = random.randint(50, 55)
    canvas.paste_img(val.pic, (bbox[0][0] + int(s * offset2), bbox[0][1] + int(s * offset2)))

    tmp = {'transcription': val_text.text,
           'points': [[bbox[0][0] + int(s * offset2)-bbox_offset, bbox[0][1] + int(s * offset2)-bbox_offset],
                      [bbox[0][0] + int(s * offset2) + val.pic.size[0]+bbox_offset, bbox[0][1] + int(s * offset2)-bbox_offset],
                      [bbox[0][0] + int(s * offset2) + val.pic.size[0]+bbox_offset,
                       bbox[0][1] + int(s * offset2) + val.pic.size[1]+bbox_offset],
                      [bbox[0][0] + int(s * offset2)-bbox_offset, bbox[0][1] + int(s * offset2) + val.pic.size[1]+bbox_offset]]}
    label.append(tmp)

    tmpx, tmpy = bbox[0][0], bbox[0][1] + int(s * offset2 + 30) + val.pic.size[1]
    for i in range(5):
        tmp_str = "-" + get_string(char_dict_num2, 1, (1, 10)) + '.' + get_string(char_dict_num2, 1, (1, 10))
        val_text = TextString(tmp_str, font_path, char_size=int(char_size * 0.8))
        val = CharsPic(val_text)
        val.gen_pic(isblur=False, isnosie=True, bboxon=False)
        offset2 = random.randint(50, 55)
        canvas.paste_img(val.pic, (tmpx, tmpy + int(i * (s * offset2))))

        tmp = {'transcription': val_text.text,
               'points': [[tmpx-bbox_offset, tmpy + int(i * (s * offset2))-bbox_offset],
                          [tmpx + val.pic.size[0]+bbox_offset, tmpy + int(i * (s * offset2))-bbox_offset],
                          [tmpx + val.pic.size[0]+bbox_offset,
                           tmpy + int(i * (s * offset2)) + val.pic.size[1]+bbox_offset],
                          [tmpx-bbox_offset, tmpy + int(i * (s * offset2)) + val.pic.size[1]+bbox_offset]]}
        label.append(tmp)

    str2_2_1 = '数量'
    text_str2_2_1 = TextString(text_string=str2_2_1, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=int(s * 25))
    canvas.draw_text_string(text_str2_2_1, tuple(map(scales, (1350, 630))))

    bbox = canvas.get_bbox(text_str2_2_1)[0]
    # bbox = canvas.get_bbox(text_str2_2_1)
    tmp = {'transcription': text_str2_2_1.text,
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][3]+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox[0][3]+bbox_offset]]}
    label.append(tmp)

    tmp_str = get_string(char_dict_num2, 1, (1, 10))
    val_text = TextString(tmp_str, font_path2, char_size=int(char_size * 0.8))
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    offset2 = random.randint(50, 55)
    canvas.paste_img(val.pic, (bbox[0][0] + int(s * offset2), bbox[0][1] + int(s * offset2)))

    tmp = {'transcription': val_text.text,
           'points': [[bbox[0][0] + int(s * offset2)-bbox_offset, bbox[0][1] + int(s * offset2)-bbox_offset],
                      [bbox[0][0] + int(s * offset2) + val.pic.size[0]+bbox_offset, bbox[0][1] + int(s * offset2)-bbox_offset],
                      [bbox[0][0] + int(s * offset2) + val.pic.size[0]+bbox_offset,
                       bbox[0][1] + int(s * offset2) + val.pic.size[1]+bbox_offset],
                      [bbox[0][0] + int(s * offset2)-bbox_offset,
                       bbox[0][1] + int(s * offset2) + val.pic.size[1]+bbox_offset]]}
    label.append(tmp)

    tmpx, tmpy = bbox[0][0] + int(s * offset2), 5+bbox[0][1] + int(s * (offset2 + 15)) + val.pic.size[1]
    for i in range(5):
        tmp_str = get_string(char_dict_num2, 1, (1, 10))
        val_text = TextString(tmp_str, font_path2, char_size=int(char_size * 0.6))
        val = CharsPic(val_text)
        val.gen_pic(isblur=False, isnosie=True, bboxon=False)
        offset2 = random.randint(50, 55)
        canvas.paste_img(val.pic, (tmpx, tmpy + int(i * (s * offset2))))

        tmp = {'transcription': val_text.text,
               'points': [[tmpx-bbox_offset, tmpy + int(i * (s * offset2))-bbox_offset],
                          [tmpx + val.pic.size[0]+bbox_offset, tmpy + int(i * (s * offset2))-bbox_offset],
                          [tmpx + val.pic.size[0]+bbox_offset,
                           tmpy + int(i * (s * offset2)) + val.pic.size[1]+bbox_offset],
                          [tmpx-bbox_offset, tmpy + int(i * (s * offset2)) + val.pic.size[1]+bbox_offset]]}
        label.append(tmp)

    str2_3_1 = '单价'
    text_str2_3_1 = TextString(text_string=str2_3_1, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=int(s * 25))
    canvas.draw_text_string(text_str2_3_1, tuple(map(scales, (1580, 630))))

    bbox = canvas.get_bbox(text_str2_3_1)[0]
    tmp = {'transcription': text_str2_3_1.text,
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][3]+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox[0][3]+bbox_offset]]}
    # canvas.draw_rectangle(bbox[0][0], outline='red', width=3)
    label.append(tmp)

    tmp_str1 = get_string(char_dict_num2, random.randint(2, 3), (1, 10))
    tmp_str2 = get_string(char_dict_num2, 2, (1, 10))
    tmp_str = tmp_str1 + '.' + tmp_str2
    val_text = TextString(tmp_str, font_path2, char_size=int(char_size * 0.8))
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    offset2 = random.randint(50, 55)
    offset = random.randint(15, 25)
    canvas.paste_img(val.pic, (bbox[0][0] - int(s * offset), bbox[0][1] + int(s * offset2)))
    tmp = {'transcription': val_text.text,
           'points': [[bbox[0][0] - int(s * offset)-bbox_offset, bbox[0][1] + int(s * offset2)-bbox_offset],
                      [bbox[0][0] - int(s * offset) + val.pic.size[0]+bbox_offset,
                       bbox[0][1] + int(s * offset2)-bbox_offset],
                      [bbox[0][0] - int(s * offset) + val.pic.size[0]+bbox_offset,
                       bbox[0][1] + int(s * offset2) + val.pic.size[1]+bbox_offset],
                      [bbox[0][0] - int(s * offset)-bbox_offset,
                       bbox[0][1] + int(s * offset2) + val.pic.size[1]+bbox_offset]]}
    label.append(tmp)

    tmpx, tmpy = bbox[0][0] + int(s * 20), bbox[0][1] + int(s * (offset2 + 30)) + val.pic.size[1]
    for i in range(5):
        tmp_str = "-" + get_string(char_dict_num2, 1, (1, 10)) + '.' + get_string(char_dict_num2, 1, (1, 10))
        val_text = TextString(tmp_str, font_path2, char_size=int(char_size * 0.8))
        val = CharsPic(val_text)
        val.gen_pic(isblur=False, isnosie=True, bboxon=False)
        offset2 = random.randint(50, 55)
        canvas.paste_img(val.pic, (tmpx, tmpy + int(i * (s * offset2))))

        tmp = {'transcription': val_text.text,
               'points': [[tmpx-bbox_offset, tmpy + int(i * (s * offset2))-bbox_offset],
                          [tmpx + val.pic.size[0]+bbox_offset, tmpy + int(i * (s * offset2))-bbox_offset],
                          [tmpx + val.pic.size[0]+bbox_offset,
                           tmpy + int(i * (s * offset2)) + val.pic.size[1]+bbox_offset],
                          [tmpx-bbox_offset, tmpy + int(i * (s * offset2)) + val.pic.size[1]+bbox_offset]]}
        label.append(tmp)

    str2_4_1 = '金额'
    text_str2_4_1 = TextString(text_string=str2_4_1, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=int(s * 65))
    canvas.draw_text_string(text_str2_4_1, tuple(map(scales, (1860, 630))))
    bbox = text_str2_4_1.get_bbox()
    tmp = {'transcription': text_str2_4_1.text,
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][3]+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox[0][3]+bbox_offset]]}
    label.append(tmp)

    tmp_str1 = get_string(char_dict_num2, random.randint(2, 5), (1, 10))
    tmp_str2 = get_string(char_dict_num2, 2, (1, 10))
    tmp_str = tmp_str1 + '.' + tmp_str2
    val_text = TextString(tmp_str, font_path2, char_size=int(char_size * 0.8))
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    offset2 = random.randint(45, 55)
    offset = random.randint(25, 35)
    canvas.paste_img(val.pic, (bbox[0][0] + int(s * offset), bbox[0][1] + int(s * offset2)))
    tmp = {'transcription': val_text.text,
           'points': [[bbox[0][0] + int(s * offset)-bbox_offset,
                       bbox[0][1] + int(s * offset2)-bbox_offset],
                      [bbox[0][0] + int(s * offset) + val.pic.size[0]+bbox_offset,
                       bbox[0][1] + int(s * offset2)-bbox_offset],
                      [bbox[0][0] + int(s * offset) + val.pic.size[0]+bbox_offset,
                       bbox[0][1] + int(s * offset2) + val.pic.size[1]+bbox_offset],
                      [bbox[0][0] + int(s * offset)-bbox_offset,
                       bbox[0][1] + int(s * offset2) + val.pic.size[1]+bbox_offset]]}
    label.append(tmp)
    tmpx, tmpy = bbox[0][0] + int(s), bbox[0][1] + int(s * offset2 + 15) + val.pic.size[1]
    for j in range(2):
        for i in range(4):
            tmp_str = "-" + get_string(char_dict_num2, 1, (1, 10))
            val_text = TextString(tmp_str, font_path2, char_size=int(char_size * 0.6))
            val = CharsPic(val_text)
            val.gen_pic(isblur=False, isnosie=True, bboxon=False)
            offset2 = random.randint(50, 55)
            canvas.paste_img(val.pic, (tmpx, tmpy + int(i * (s * offset2))))

            tmp = {'transcription': val_text.text,
                   'points': [[tmpx-bbox_offset, tmpy + int(i * (s * offset2))-bbox_offset],
                              [tmpx + val.pic.size[0]+bbox_offset,
                               tmpy + int(i * (s * offset2))-bbox_offset],
                              [tmpx + val.pic.size[0]+bbox_offset,
                               tmpy + int(i * (s * offset2)) + val.pic.size[1]+bbox_offset],
                              [tmpx-bbox_offset, tmpy + int(i * (s * offset2)) + val.pic.size[1]+bbox_offset]]}
            label.append(tmp)
        tmpx, tmpy = bbox[0][0] + int(s * 150), bbox[0][1] + int(s * offset2 + 15) + val.pic.size[1]

    bbox = canvas.get_bbox(text_str2_4_1)[0]
    offset2 = random.randint(355, 360)
    offset = random.randint(5, 15)
    x, y = bbox[0][0] + int(s * offset), bbox[0][1] + int(s * offset2)
    for i in range(2):
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
               'points': [[x-bbox_offset, y-bbox_offset], [x + val.size[0]+bbox_offset, y-bbox_offset],
                          [x + val.size[0]+bbox_offset, y + val.size[1]+bbox_offset],
                          [x-bbox_offset, y + val.size[1]+bbox_offset]]}
        label.append(tmp)
        y += (int(s * 30) + val.size[1])

    str2_5_1 = '税率'
    text_str2_5_1 = TextString(text_string=str2_5_1, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str2_5_1, tuple(map(scales, (2150, 630))))

    bbox = text_str2_5_1.get_bbox()
    tmp = {'transcription': text_str2_5_1.text,
         'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                  [bbox[0][2]+bbox_offset, bbox[0][1]-bbox_offset],
                  [bbox[0][2]+bbox_offset, bbox[0][3]+bbox_offset],
                  [bbox[0][0]-bbox_offset, bbox[0][3]+bbox_offset]]}
    # canvas.draw_rectangle(bbox[0], outline='red', width=3)
    label.append(tmp)
    tmpx, tmpy = bbox[0][0], bbox[0][1]
    for i in range(5):
        tmp_str = get_string(char_dict_num2, random.randint(1, 2), (1, 10)) + '%'
        val_text = TextString(tmp_str, font_path, char_size=int(char_size * 0.8))
        val = CharsPic(val_text)
        val.gen_pic(isblur=False, isnosie=True, bboxon=False)
        offset2 = random.randint(50, 55)
        offset = random.randint(20, 30)
        canvas.paste_img(val.pic, (tmpx + int(s * offset), tmpy + int(s * offset2)))
        tmp = {'transcription': val_text.text,
               'points': [[tmpx + int(s * offset)-bbox_offset, tmpy + int(s * offset2)-bbox_offset],
                          [tmpx + int(s * offset) + val.pic.size[0]+bbox_offset, tmpy + int(s * offset2)-bbox_offset],
                          [tmpx + int(s * offset) + val.pic.size[0]+bbox_offset,
                           tmpy + int(s * offset2) + val.pic.size[1]+bbox_offset],
                          [tmpx + int(s * offset)-bbox_offset, tmpy + int(s * offset2) + val.pic.size[1]+bbox_offset]]}
        label.append(tmp)
        tmpy += int(s * offset2) + val.pic.size[1]

    str2_2_1 = '税额'
    text_str2_2_1 = TextString(text_string=str2_2_1, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=int(s * 60))
    canvas.draw_text_string(text_str2_2_1, tuple(map(scales, (2340, 630))))

    bbox = text_str2_2_1.get_bbox()
    tmp = {'transcription': text_str2_2_1.text,
         'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                  [bbox[0][2]+bbox_offset, bbox[0][1]-bbox_offset],
                  [bbox[0][2]+bbox_offset, bbox[0][3]+bbox_offset],
                  [bbox[0][0]-bbox_offset, bbox[0][3]+bbox_offset]]}
    # canvas.draw_rectangle(bbox[0], outline='red', width=3)
    label.append(tmp)

    tmp_str1 = get_string(char_dict_num2, random.randint(2, 5), (1, 10))
    tmp_str2 = get_string(char_dict_num2, 2, (1, 10))
    tmp_str = tmp_str1 + '.' + tmp_str2
    val_text = TextString(tmp_str, font_path2, char_size=int(char_size * 0.8))
    # val_text = TextString('9999.00', font_path2, char_size=int(s * 50))
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    offset2 = random.randint(45, 55)
    offset = random.randint(25, 35)
    canvas.paste_img(val.pic, (bbox[0][0] + int(s * offset), bbox[0][1] + int(s * offset2)))

    tmp = {'transcription': val_text.text,
           'points': [[bbox[0][0] + int(s * offset)-bbox_offset,
                       bbox[0][1] + int(s * offset2)-bbox_offset],
                      [bbox[0][0] + int(s * offset) + val.pic.size[0]+bbox_offset,
                       bbox[0][1] + int(s * offset2)-bbox_offset],
                      [bbox[0][0] + int(s * offset) + val.pic.size[0]+bbox_offset,
                       bbox[0][1] + int(s * offset2) + val.pic.size[1]+bbox_offset],
                      [bbox[0][0] + int(s * offset)-bbox_offset,
                       bbox[0][1] + int(s * offset2) + val.pic.size[1]+bbox_offset]]}
    label.append(tmp)

    tmpx, tmpy = bbox[0][0] + int(s), bbox[0][1] + int(s * offset2 + 15) + val.pic.size[1]
    for j in range(2):
        for i in range(4):
            tmp_str = "-" + get_string(char_dict_num2, 1, (1, 10))
            val_text = TextString(tmp_str, font_path2, char_size=int(char_size * 0.6))
            val = CharsPic(val_text)
            val.gen_pic(isblur=False, isnosie=True, bboxon=False)
            offset2 = random.randint(50, 55)
            canvas.paste_img(val.pic, (tmpx, tmpy + int(i * (s * offset2))))

            tmp = {'transcription': val_text.text,
                   'points': [[tmpx-bbox_offset, tmpy + int(i * (s * offset2))-bbox_offset],
                              [tmpx + val.pic.size[0]+bbox_offset, tmpy + int(i * (s * offset2))-bbox_offset],
                              [tmpx + val.pic.size[0]+bbox_offset,
                               tmpy + int(i * (s * offset2)) + val.pic.size[1]+bbox_offset],
                              [tmpx-bbox_offset, tmpy + int(i * (s * offset2)) + val.pic.size[1]+bbox_offset]]}
            label.append(tmp)
        tmpx, tmpy = bbox[0][0] + int(s * 150), bbox[0][1] + int(s * offset2 + 15) + val.pic.size[1]

    offset2 = random.randint(350, 355)
    offset = random.randint(5, 15)
    x, y = bbox[0][0] + int(s * offset), bbox[0][1] + int(s * offset2)
    for i in range(2):
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
               'points': [[x-bbox_offset, y-bbox_offset], [x + val.size[0]+bbox_offset, y-bbox_offset],
                          [x + val.size[0]+bbox_offset, y + val.size[1]+bbox_offset],
                          [x-bbox_offset, y + val.size[1]+bbox_offset]]}
        label.append(tmp)
        y += (int(s * 30) + val.size[1])


    # 第三行
    canvas.draw_rectangle(tuple(map(scales, (200, 1140, 820, 1240))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(scales, (820, 1140, 2600, 1240))), outline=rec_color, width=width)

    str3_1_1 = '价税合计（大写）'
    text_str3_1_1 = TextString(text_string=str3_1_1, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=int(s * 10))
    canvas.draw_text_string(text_str3_1_1, tuple(map(scales, (330, 1160))))

    bbox = text_str3_1_1.get_bbox()
    tmp = {'transcription': text_str3_1_1.text,
         'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                  [bbox[0][2]+bbox_offset, bbox[0][1]-bbox_offset],
                  [bbox[0][2]+bbox_offset, bbox[0][3]+bbox_offset],
                  [bbox[0][0]-bbox_offset, bbox[0][3]+bbox_offset]]}
    label.append(tmp)

    tmp_dict = get_dict('./utils/dict/fanti_nums.txt')
    tmp_str = get_string(tmp_dict, random.randint(12, 20), (1, 19))
    val_text = TextString(tmp_str, font_path, char_size=int(char_size * 0.8))
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    offset2 = random.randint(820, 870)
    canvas.paste_img(val.pic, (int(s * offset2), bbox[0][1]))
    tmp = {'transcription': val_text.text,
           'points': [[int(s * offset2)-bbox_offset, bbox[0][1]-bbox_offset],
                      [int(s * offset2) + val.pic.size[0]+bbox_offset, bbox[0][1]-bbox_offset],
                      [int(s * offset2) + val.pic.size[0]+bbox_offset,
                       bbox_offset+bbox[0][1] + val.pic.size[1]],
                      [int(s * offset2)-bbox_offset, bbox[0][1] + val.pic.size[1]+bbox_offset]]}
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
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + val.pic.size[0]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + val.pic.size[0]+bbox_offset, bbox[0][3]+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox[0][3]+bbox_offset]]}
    label.append(tmp)

    # 第四行
    canvas.draw_rectangle(tuple(map(scales, (200, 1240, 290, 1500))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(scales, (290, 1240, 1580, 1500))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(scales, (1580, 1240, 1640, 1500))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(scales, (1640, 1240, 2600, 1500))), outline=rec_color, width=width)

    str4 = '销'
    text_str4 = TextString(text_string=str4, font=font_path, char_size=char_size,
                           color=font_color, direction='ttb', line_space=0, char_space=0)
    canvas.draw_text_string(text_str4, tuple(map(scales, (230, 1280))))

    bbox = text_str4.get_bbox()
    tmp = {'transcription': text_str4.text,
       'points': [[bbox[0][0] - bbox_offset, bbox[0][1] - bbox_offset],
                  [bbox[0][2] + bbox_offset, bbox[0][1] - bbox_offset],
                  [bbox[0][2] + bbox_offset, bbox[0][3] + bbox_offset],
                  [bbox[0][0] - bbox_offset, bbox[0][3] + bbox_offset]]}
    label.append(tmp)

    str4 = '售'
    text_str4 = TextString(text_string=str4, font=font_path, char_size=char_size,
                           color=font_color, direction='ttb', line_space=0, char_space=0)
    canvas.draw_text_string(text_str4, tuple(map(scales, (230, 1350))))

    bbox = text_str4.get_bbox()
    tmp = {'transcription': text_str4.text,
         'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                  [bbox[0][2]+bbox_offset, bbox[0][1]-bbox_offset],
                  [bbox[0][2]+bbox_offset, bbox[0][3]+bbox_offset],
                  [bbox[0][0]-bbox_offset, bbox[0][3]+bbox_offset]]}
    # canvas.draw_rectangle(bbox[0], outline='red', width=3)
    label.append(tmp)

    str4 = '方'
    text_str4 = TextString(text_string=str4, font=font_path, char_size=char_size,
                           color=font_color, direction='ttb', line_space=0, char_space=0)
    canvas.draw_text_string(text_str4, tuple(map(scales, (230, 1420))))

    bbox = text_str4.get_bbox()
    tmp = {'transcription': text_str4.text,
         'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                  [bbox[0][2]+bbox_offset, bbox[0][1]-bbox_offset],
                  [bbox[0][2]+bbox_offset, bbox[0][3]+bbox_offset],
                  [bbox[0][0]-bbox_offset, bbox[0][3]+bbox_offset]]}
    # canvas.draw_rectangle(bbox[0], outline='red', width=3)
    label.append(tmp)

    str4_2_1 = '名'
    text_str4_2_1 = TextString(text_string=str4_2_1, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str4_2_1, tuple(map(scales, (305, 1250))))
    bbox = text_str4_2_1.get_bbox()
    tmp = {'transcription': text_str4_2_1.text,
         'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                  [bbox[0][2]+bbox_offset, bbox[0][1]-bbox_offset],
                  [bbox[0][2]+bbox_offset, bbox[0][3]+bbox_offset],
                  [bbox[0][0]-bbox_offset, bbox[0][3]+bbox_offset]]}
    # canvas.draw_rectangle(bbox[0], outline='red', width=3)
    label.append(tmp)

    str4_2_1_2 = '称：'
    text_str4_2_1_2 = TextString(text_string=str4_2_1_2, font=font_path, char_size=char_size,
                                 color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str4_2_1_2, tuple(map(scales, (495, 1250))))

    bbox = text_str4_2_1_2.get_bbox()

    tmp_str = get_string(char_dict, random.randint(10, 20), (1, 100))
    val_text = TextString(tmp_str, font_path, char_size=int(char_size))
    # val_text = TextString('黄金二阿胶粉借款金额', font_path, char_size=int(s * 40))
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][2] + 1, bbox[0][1]))
    tmp = {'transcription': str4_2_1_2 + val_text.text,
           'points': [[bbox[0][0] + 1-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + 1 + val.pic.size[0]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + 1 + val.pic.size[0]+bbox_offset, bbox[0][1] + val.pic.size[1]+bbox_offset],
                      [bbox[0][0] + 1-bbox_offset, bbox[0][1] + val.pic.size[1]+bbox_offset]]}
    label.append(tmp)

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
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + val.pic.size[0]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + val.pic.size[0]+bbox_offset, max(bbox[0][3], val.pic.size[1])+bbox_offset],
                      [bbox[0][0]-bbox_offset, max(bbox[0][3], val.pic.size[1])+bbox_offset]]}
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
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + int(s * offset2) + w + val.pic.size[0]+bbox_offset,
                       bbox[0][1]-bbox_offset],
                      [bbox[0][2] + int(s * offset2) + w + val.pic.size[0]+bbox_offset,
                       bbox[0][3]+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox[0][3]+bbox_offset]]}
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
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + int(s * offset2) + w + val.pic.size[0]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + int(s * offset2) + w + val.pic.size[0]+bbox_offset,
                       bbox[0][3]+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox[0][3]+bbox_offset]]}
    label.append(tmp)

    str5 = '备'
    text_str5 = TextString(text_string=str5, font=font_path, char_size=char_size,
                           color=font_color, direction='ttb', line_space=0, char_space=0)
    canvas.draw_text_string(text_str5, tuple(map(scales, (1590, 1280))))

    bbox = text_str5.get_bbox()
    tmp = {'transcription': text_str5.text,
         'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                  [bbox[0][2]+bbox_offset, bbox[0][1]-bbox_offset],
                  [bbox[0][2]+bbox_offset, bbox[0][3]+bbox_offset],
                  [bbox[0][0]-bbox_offset, bbox[0][3]+bbox_offset]]}
    label.append(tmp)

    str5 = '注'
    text_str5 = TextString(text_string=str5, font=font_path, char_size=char_size,
                           color=font_color, direction='ttb', line_space=0, char_space=0)
    canvas.draw_text_string(text_str5, tuple(map(scales, (1590, 1420))))

    bbox = text_str5.get_bbox()
    tmp = {'transcription': text_str5.text,
         'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                  [bbox[0][2]+bbox_offset, bbox[0][1]-bbox_offset],
                  [bbox[0][2]+bbox_offset, bbox[0][3]+bbox_offset],
                  [bbox[0][0]-bbox_offset, bbox[0][3]+bbox_offset]]}
    label.append(tmp)

    str5_1 = '收款人：'
    text_str5_1 = TextString(text_string=str5_1, font=font_path, char_size=char_size,
                             color=font_color, direction='ltr', line_space=0, char_space=int(s * 10))
    canvas.draw_text_string(text_str5_1, tuple(map(scales, (245, 1510))))

    bbox = text_str5_1.get_bbox()

    tmp_str = get_string(char_dict, random.randint(2, 4), (1, 100))
    val_text = TextString(tmp_str, font_path, char_size=char_size)
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][2], bbox[0][1]))

    tmp = {'transcription': str5_1 + val_text.text,
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + val.pic.size[0]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + val.pic.size[0]+bbox_offset, bbox[0][1] + val.pic.size[1]+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox[0][1] + val.pic.size[1]+bbox_offset]]}
    label.append(tmp)

    str5_2 = '复核：'
    text_str5_2 = TextString(text_string=str5_2, font=font_path, char_size=char_size,
                             color=font_color, direction='ltr', line_space=0, char_space=int(s * 10))
    canvas.draw_text_string(text_str5_2, tuple(map(scales, (910, 1510))))

    bbox = text_str5_2.get_bbox()
    tmp_str = get_string(char_dict, random.randint(2, 4), (1, 100))
    val_text = TextString(tmp_str, font_path, char_size=char_size)
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][2] + 1, bbox[0][1]))

    tmp = {'transcription': str5_2 + val_text.text,
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + val.pic.size[0]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + val.pic.size[0]+bbox_offset, bbox[0][1] + val.pic.size[1]+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox[0][1] + val.pic.size[1]+bbox_offset]]}
    label.append(tmp)

    str5_3 = '开票人：'
    text_str5_3 = TextString(text_string=str5_3, font=font_path, char_size=char_size,
                             color=font_color, direction='ltr', line_space=0, char_space=int(s * 10))
    canvas.draw_text_string(text_str5_3, tuple(map(scales, (1430, 1510))))
    bbox = text_str5_3.get_bbox()

    tmp_str = get_string(char_dict, random.randint(2, 4), (1, 100))
    val_text = TextString(tmp_str, font_path, char_size=char_size)
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][2] + 1, bbox[0][1]))

    tmp = {'transcription': str5_3 + val_text.text,
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + val.pic.size[0]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2] + val.pic.size[0]+bbox_offset, bbox[0][1] + val.pic.size[1]+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox[0][1] + val.pic.size[1]+bbox_offset]]}
    label.append(tmp)

    str5_4 = '销售方：（章）'
    text_str5_4 = TextString(text_string=str5_4, font=font_path, char_size=char_size,
                             color=font_color, direction='ltr', line_space=0, char_space=int(s * 10))
    canvas.draw_text_string(text_str5_4, tuple(map(scales, (1990, 1510))))

    bbox = text_str5_4.get_bbox()
    tmp = {'transcription': text_str5_4.text,
           'points': [[bbox[0][0]-bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][1]-bbox_offset],
                      [bbox[0][2]+bbox_offset, bbox[0][3]+bbox_offset],
                      [bbox[0][0]-bbox_offset, bbox[0][3]+bbox_offset]]}
    label.append(tmp)
    output_dir = imgs_dir + basename
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        os.chmod(output_dir, 0o777)
    img_name = '%05d.jpg' % img_name
    img_path = os.path.join(imgs_dir, basename, img_name)
    # print(img_path)
    logger.info(img_path)
    # 校验文本框坐标位置
    for tmp_label in label:
        tmp_bbox = tmp_label['points']
        tmp1 = tmp_bbox[1][0] - tmp_bbox[0][0]
        tmp2 = tmp_bbox[2][0] - tmp_bbox[3][0]
        h1 = tmp_bbox[3][1] - tmp_bbox[0][1]
        h2 = tmp_bbox[2][1] - tmp_bbox[1][1]
        assert tmp1 == tmp2, '%s the width of bbox should be equally' % tmp_label['transcription']
        assert h1 == h2, '%s the height of bbox should be equally' % tmp_label['transcription']

    # canvas = rectangle(canvas, label)
    canvas.save(img_path)

    # print(label)
    return [basename + img_name, label]


def rectangle(canvas, labels):
    for label in labels:
        bbox = label['points']
        canvas.draw_rectangle([(bbox[0][0], bbox[0][1]), (bbox[2][0], bbox[2][1])], outline='red', width=2)
    return canvas

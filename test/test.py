#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
"""
@AUTHOR:
@FILE:test.py
@NAME:Table_renderer
@TIME:2021/07/25
@IDE: PyCharm
@Ref:
"""

import os
import sys
import random
import yaml
import pdb

sys.path.append('..')
sys.path.append('.')

from TextString.TextString import *
from Canvas.Canvas import *
from utils.utils import *
from tools.charspic import *

WIDTH = 2838
HEIGHT = 1627


def set_config(width=2838, height=1627):
    size = (2838, 1627)
    new_size = (int(width), int(height))
    scales = (width / size[0], height / size[1])
    key_char_size = 38
    val_num_size = 35
    val_char_size = 35
    rectangle = [200, 367, 2600, 1487]
    area = []
    row_1 = [[200, 367, 293, 627], [293, 367, 1577, 627],
             [1577, 367, 1638, 627], [1638, 367, 2600, 627]]
    row_2 = [[200, 627, 822, 1151], [822, 627, 1128, 1151],
             [1128, 627, 1276, 1151], [1276, 627, 1518, 1151],
             [1518, 627, 1758, 1151], [1758, 627, 2118, 1151],
             [2118, 627, 2245, 1151], [2245, 627, 2600, 1151],
             ]
    row_3 = [[200, 1151, 822, 1250], [822, 1151, 2600, 1250]]

    row_4 = [[200, 1250, 293, 1487], [293, 1250, 1577, 1487],
             [1577, 1250, 1638, 1487], [1638, 1250, 2600, 1487]]
    rows = [row_1, row_2, row_3, row_4]
    new_rows = []
    x = rectangle[0] * scales[0]
    y = rectangle[1] * scales[1]
    new_rows = []
    for i, row in enumerate(rows):
        new_row = []
        for j, bbox in enumerate(row):
            w = int((bbox[2] - bbox[0]) * scales[0])
            h = int((bbox[3] - bbox[1]) * scales[1])

            # new_row.append(list(map(int, [x, y, x + w, y + h])))
            new_row.append([bbox[0] * scales[0], bbox[1] * scales[0], bbox[2] * scales[0], bbox[3] * scales[0]])
            x = int(x + w)
        y = int(y + h)
        x = rectangle[0] * scales[0]
        new_rows.append(new_row)

    pil_img = Image.new('RGB', size=new_size, color='white')
    draw = ImageDraw.Draw(pil_img)
    for i, row in enumerate(new_rows):
        for bbox in row:
            draw.rectangle(bbox, outline='black', width=1)
    pil_img.save("./aaa.jpg")

    config = {'font': './fonts/fangzheng_heiti.ttf',
              'dict_file': '../utils/dict/cht_std_dict2.txt',
              'char_size': 20,
              'h_char_size': 20,

              }

    char_dict = get_dict(fp=config['dict_file'])
    # print(char_dict)
    # 字体大小20-22
    char_size = config['char_size']
    h_char_space = config['h_char_size']
    with open('../configure/configure.yml', 'w') as fw:
        yaml.dump(config, fw, )

    return config


def receipt():
    font_path = "../fonts/KaitiGB2312.ttf"
    font_path2 = '../fonts/Times New Roman.ttf'
    char_dict_path = '../utils/dict/cht_std_dict2.txt'
    char_dict_path2 = '../utils/dict/nums_dict2.txt'

    font_color = (163, 131, 80)
    rec_color = (163, 131, 80)
    # s = 0.9
    s = 0.5+random.random()
    if s > 1.0:
        s = 1
    width = 2
    char_size = int(random.randint(35, 38) * s)
    label = []
    char_dict = get_dict(fp=char_dict_path)
    char_dict_num2 = get_dict(fp=char_dict_path2)

    def scales(num):
        # scale = s
        return int(num * s)

    # 返回PIL.Image对象
    canvas = CanvasImage(size=tuple(map(scales, (2835, 1620))), color='white')
    # 两边虚竖线
    canvas.draw_line((int(90 * s), 0, int(90 * s), int(2800 * s)), rec_color, width=width)
    canvas.draw_line(tuple(map(scales, (2700, 0, 2700, 1620))), rec_color, width=width)

    str1 = '湖北增值税专用发票'
    # str1 = '藹靄聱螯謷鳌鏖'
    text_str1 = TextString(text_string=str1, font=font_path, char_size=int(65 * s),
                           color=font_color, direction='ltr', line_space=0, char_space=5)
    canvas.draw_text_string(text_str1, tuple(map(int, (1040 * s, 100 * s))))
    bbox = text_str1.get_bbox()
    tmp = {'transcriptions': text_str1.text,
           'points': [[bbox[0][0], bbox[0][1]],
                      [bbox[0][2], bbox[0][1]],
                      [bbox[0][2], bbox[0][3]],
                      [bbox[0][0], bbox[0][3]]]}
    # canvas.draw_rectangle(bbox[0], outline='red', width=3)
    label.append(tmp)
    canvas.draw_multilines(tuple(map(int, (1000 * s, 220 * s, 1700 * s, 220 * s))), font_color, offset=10 * s, width=3)

    text_str_left = TextString('机器编码:', font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str_left, tuple(map(int, (200 * s, 300 * s))))
    bbox = text_str_left.get_bbox()

    tmp_str = get_string(char_dict_num2,12,(1,10))
    val_text = TextString(tmp_str, font_path, char_size=char_size)
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][2], bbox[0][1] + int(10 * s)))

    tmp = {'transcriptions': text_str_left.text+val.text,
           'points': [[bbox[0][0], bbox[0][1]],
                      [bbox[0][2]+val.pic.size[0], bbox[0][1]],
                      [bbox[0][2]+val.pic.size[0], bbox[0][3]+int(10 * s)],
                      [bbox[0][0], bbox[0][3]+int(10 * s)]]}
    # canvas.draw_rectangle([(bbox[0][0], bbox[0][1]),
    #                        (bbox[0][2]+val.pic.size[0], bbox[0][3]+int(10 * s))], outline='red', width=3)
    label.append(tmp)

    text_str_right = TextString('校验码:', font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str_right, tuple(map(int, (1970 * s, 220 * s))))
    bbox = text_str_right.get_bbox()

    tmp_str = ''
    for i in range(4):
        a = get_string(char_dict_num2, 5, (1, 10))+' '
        tmp_str += a
    val_text = TextString(tmp_str, font_path, char_size=char_size)
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][2], bbox[0][1] + int(10 * s)))

    tmp = {'transcriptions': text_str_right.text + val.text,
           'points': [[bbox[0][0], bbox[0][1]],
                      [bbox[0][2] + val.pic.size[0], bbox[0][1]],
                      [bbox[0][2] + val.pic.size[0], bbox[0][3] + int(10 * s)],
                      [bbox[0][0], bbox[0][3] + int(10 * s)]]}
    # canvas.draw_rectangle([(bbox[0][0], bbox[0][1]),
    #                        (bbox[0][2] + val.pic.size[0], bbox[0][3] + int(10 * s))], outline='red', width=3)
    label.append(tmp)

    text_str_right = TextString('发票代码:', font=font_path, char_size=char_size,
                                color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str_right, tuple(map(int, (1970 * s, 160 * s))))
    bbox = text_str_right.get_bbox()
    tmp_str= get_string(char_dict_num2, 12, (1, 10))
    val_text = TextString(tmp_str, font_path, char_size=char_size)
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][2], bbox[0][1] + int(10 * s)))

    tmp = {'transcriptions': text_str_right.text + val.text,
           'points': [[bbox[0][0], bbox[0][1]],
                      [bbox[0][2] + val.pic.size[0], bbox[0][1]],
                      [bbox[0][2] + val.pic.size[0], bbox[0][3] + int(10 * s)],
                      [bbox[0][0], bbox[0][3] + int(10 * s)]]}
    # canvas.draw_rectangle([(bbox[0][0], bbox[0][1]),
    #                        (bbox[0][2] + val.pic.size[0], bbox[0][3] + int(10 * s))], outline='red', width=3)
    label.append(tmp)

    text_str_right = TextString('发票号码:', font=font_path, char_size=char_size,
                                color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str_right, tuple(map(int, (1970 * s, 100 * s))))
    bbox = text_str_right.get_bbox()
    tmp_str = get_string(char_dict_num2, 8, (1, 10))
    val_text = TextString(tmp_str, font_path, char_size=char_size)
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][2], bbox[0][1] + int(10 * s)))

    tmp = {'transcriptions': text_str_right.text + val.text,
           'points': [[bbox[0][0], bbox[0][1]],
                      [bbox[0][2] + val.pic.size[0], bbox[0][1]],
                      [bbox[0][2] + val.pic.size[0], bbox[0][3] + int(10 * s)],
                      [bbox[0][0], bbox[0][3] + int(10 * s)]]}
    # canvas.draw_rectangle([(bbox[0][0], bbox[0][1]),
    #                        (bbox[0][2] + val.pic.size[0], bbox[0][3] + int(10 * s))], outline='red', width=3)
    label.append(tmp)

    # 整个大框
    canvas.draw_rectangle(tuple(map(scales, (200, 360, 2600, 1500))), fill='white', outline=rec_color,
                          width=width)
    # str_left = '税总函〔2019〕144号中钞华森实业公司'
    # str_left = Image.open('./r_result.jpg', )
    # str_left.resize()
    # canvas.paste_img(str_left, (150, 510))
    # canvas.paste_img(str_left, (150, 510))

    str_right = '第三联：发票联 购买方记账凭证'
    text_str_right = TextString(text_string=str_right, font=font_path, char_size=char_size,
                                color=font_color, direction='ttb', line_space=0, char_space=int(s * 10))
    canvas.draw_text_string(text_str_right, tuple(map(int, (2610 * s, 620 * s))))
    bbox = text_str_right.get_bbox()
    tmp = {'transcriptions': text_str_right.text,
           'points': [[bbox[0][0], bbox[0][1]],
                      [bbox[0][2], bbox[0][1]],
                      [bbox[0][2], bbox[0][3]],
                      [bbox[0][0], bbox[0][3]]]}
    # canvas.draw_rectangle(bbox[0], outline='red', width=3)
    label.append(tmp)

    str0 = '开票日期：'
    text_str0 = TextString(text_string=str0, font=font_path, char_size=char_size,
                           color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str0, tuple(map(int, (1970 * s, 280 * s))))

    bbox = text_str0.get_bbox()
    m = '年%02d月%02d日'% (random.randint(1, 12),random.randint(1,31))
    tmp_str = get_string(char_dict_num2, 4, (1,10))+m
    val_text = TextString(tmp_str, font_path, char_size=char_size)
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][2], bbox[0][1] + int(10 * s)))

    tmp = {'transcriptions': str0+val_text.text,
           'points': [[bbox[0][0], bbox[0][1]],
                      [bbox[0][2]+ val.pic.size[0], bbox[0][1]],
                      [bbox[0][2]+ val.pic.size[0], bbox[0][1] + int(10 * s) + val.pic.size[1]],
                      [bbox[0][0], bbox[0][1] + int(10 * s) + val.pic.size[1]]]}
    # canvas.draw_rectangle([(bbox[0][0], bbox[0][1]),
    #                        (bbox[0][2] + val.pic.size[0], bbox[0][1] + int(10 * s) + val.pic.size[1])],
    #                       outline='red', width=3)
    label.append(tmp)

    # 第一行
    canvas.draw_rectangle(tuple(map(int, (200 * s, 360 * s, 290 * s, 620 * s))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(int, (290 * s, 360 * s, 1580 * s, 620 * s))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(int, (1580 * s, 360 * s, 1640 * s, 620 * s))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(int, (1640 * s, 360 * s, 2600 * s, 620 * s))), outline=rec_color, width=width)

    str2 = '购买方'
    # str2 = get_string(char_dict,3,(1,100))
    text_str2 = TextString(text_string=str2, font=font_path, char_size=char_size,
                           color=font_color, direction='ttb', line_space=0, char_space=int(s * 30))

    canvas.draw_text_string(text_str2, tuple(map(int, (s * 230, s * 400))))
    bbox = text_str2.get_bbox()
    tmp = {'transcriptions': text_str2.text,
           'points': [[bbox[0][0], bbox[0][1]],
                      [bbox[0][2], bbox[0][1]],
                      [bbox[0][2], bbox[0][3]],
                      [bbox[0][0], bbox[0][3]]]}
    # canvas.draw_rectangle(bbox[0], outline='red', width=3)
    label.append(tmp)

    str1_2_1 = '名'

    text_str1_2_1 = TextString(text_string=str1_2_1, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str1_2_1, tuple(map(scales, (305, 375))))

    bbox = text_str1_2_1.get_bbox()
    tmp = {'transcriptions': text_str1_2_1.text,
           'points': [[bbox[0][0], bbox[0][1]],
                      [bbox[0][2], bbox[0][1]],
                      [bbox[0][2], bbox[0][3]],
                      [bbox[0][0], bbox[0][3]]]}
    # canvas.draw_rectangle(bbox[0], outline='red', width=3)
    label.append(tmp)

    str1_2_1_2 = '称：'
    text_str1_2_1_2 = TextString(text_string=str1_2_1_2, font=font_path, char_size=char_size,
                                 color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str1_2_1_2, tuple(map(scales, (495, 375))))

    bbox = text_str1_2_1_2.get_bbox()
    tmp_str = get_string(char_dict,random.randint(8,20),(1,100))
    val_text = TextString(tmp_str, font_path, char_size=char_size)
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][2] + 1, bbox[0][1]))

    tmp = {'transcriptions': str1_2_1_2 + val_text.text,
           'points': [[bbox[0][0], bbox[0][1]], [bbox[0][2] + val.pic.size[0], bbox[0][1]],
                      [bbox[0][2] + val.pic.size[0], bbox[0][3]], [bbox[0][0], bbox[0][3]]]}
    # canvas.draw_rectangle([(bbox[0][0], bbox[0][1]), (bbox[0][2] + val.pic.size[0], bbox[0][3])], outline='red',
    #                       width=3)
    label.append(tmp)

    str1_2_2 = '纳税人识别号：'
    text_str1_2_2 = TextString(text_string=str1_2_2, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str1_2_2, tuple(map(scales, (305, 440))))
    bbox = text_str1_2_2.get_bbox()

    tmp_str = get_string(char_dict_num2, 18, (1, 10))
    val_text = TextString(tmp_str, font_path, char_size=char_size)
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][2] + 1, bbox[0][1]))

    bbox2 = [[bbox[0][0], bbox[0][1]], [bbox[0][2] + val.pic.size[0], bbox[0][1]],
             [bbox[0][2] + val.pic.size[0], max(bbox[0][3], val.pic.size[1])],
             [bbox[0][0] + 1, max(bbox[0][3], val.pic.size[1])]]
    tmp = {'transcriptions': str1_2_2 + val_text.text, 'points': bbox2}
    # canvas.draw_rectangle([bbox[0][0] + 1, bbox[0][1],
    #                        bbox[0][2] + val.pic.size[0], max(bbox[0][3], val.pic.size[1])], outline='red', width=2)

    label.append(tmp)

    str1_2_3 = '地址、电话：'
    text_str1_2_3 = TextString(text_string=str1_2_3, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=int(s * 8))
    canvas.draw_text_string(text_str1_2_3, tuple(map(scales, (305, 500))))

    bbox = text_str1_2_3.get_bbox()
    tmp_str1 = get_string(char_dict, 15, (1, 100))

    val_text1 = TextString(tmp_str1, font_path, char_size=char_size)
    val1 = CharsPic(val_text1)
    val1.gen_pic(isblur=False, isnosie=True, bboxon=False)
    w, h = val1.pic.size
    canvas.paste_img(val1.pic, (bbox[0][2] + 1, bbox[0][1]))

    tmp_str = get_string(char_dict_num2, 11, (1, 10))
    val_text = TextString(tmp_str, font_path, char_size=int(char_size * 0.8))
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][2] + int(s * 50) + w, bbox[0][1] + int(s * 10)))

    tmp = {'transcriptions': str1_2_3 + tmp_str1 + tmp_str,
           'points': [[bbox[0][0], bbox[0][1]],
                      [bbox[0][2] + 1 + int(s * 50) + w + val.pic.size[0], bbox[0][1]],
                      [bbox[0][0] + 1 + int(s * 50) + w + val.pic.size[0], bbox[0][1] + int(s * 10) + val.pic.size[1]],
                      [bbox[0][0], bbox[0][1] + int(s * 10) + val.pic.size[1]]]}

    # canvas.draw_rectangle([(bbox[0][0], bbox[0][1]),
    #                        (bbox[0][2] + 1 + int(s * 50) + w + val.pic.size[0],
    #                         bbox[0][1] + int(s * 10) + val.pic.size[1])], outline='red')
    label.append(tmp)

    str1_2_4 = '开户行及账号：'
    text_str1_2_4 = TextString(text_string=str1_2_4, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str1_2_4, tuple(map(int, (s * 305, s * 565))))

    bbox = text_str1_2_4.get_bbox()

    tmp_str1 = get_string(char_dict, random.randint(12, 20), (1, 100))
    val_text1 = TextString(tmp_str1, font_path, char_size=int(char_size))
    val1 = CharsPic(val_text1)
    val1.gen_pic(isblur=False, isnosie=True, bboxon=False)
    w, h = val1.pic.size
    canvas.paste_img(val1.pic, (bbox[0][2] + 1, bbox[0][1]))

    tmp_str = get_string(char_dict_num2, 11, (1, 10))
    val_text = TextString(tmp_str, font_path, char_size=int(char_size*0.8))
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][2] + int(s * 50) + w, bbox[0][1] + int(s * 10)))

    tmp = {'transcriptions': str1_2_4 + tmp_str1 + tmp_str,
           'points': [[bbox[0][0], bbox[0][1]],
                      [bbox[0][2] + int(s * 50) + w + val.pic.size[0], bbox[0][1]],
                      [bbox[0][2] + int(s * 50) + w + val.pic.size[0],
                       bbox[0][1] + int(s * 10) + val.pic.size[1]],
                      [bbox[0][0], bbox[0][1] + int(s * 10) + val.pic.size[1]]]}
    # canvas.draw_rectangle([(bbox[0][0], bbox[0][1]),
    #                        (bbox[0][2] + int(s * 50) + w + val.pic.size[0],
    #                         bbox[0][1] + int(s * 10) + val.pic.size[1]),
    #                        ], outline='red', width=3)
    label.append(tmp)

    str3 = '密码区'
    text_str3 = TextString(text_string=str3, font=font_path, char_size=char_size,
                           color=font_color, direction='ttb', line_space=0, char_space=int(s * 35))
    canvas.draw_text_string(text_str3, tuple(map(int, (s * 1590, s * 400))))

    bbox = canvas.get_bbox(text_str3)
    tmp = {'transcriptions': str3,
           'points': [[bbox[0][0][0], bbox[0][0][1]],
                      [bbox[0][0][2], bbox[0][0][1]],
                      [bbox[0][0][2], bbox[0][0][3]],
                      [bbox[0][0][0], bbox[0][0][3]]]}
    # canvas.draw_rectangle([(bbox[0][0][0], bbox[0][0][1]),
    #                        (bbox[0][0][2], bbox[0][0][3]),
    #                        ], outline='red', width=3)
    label.append(tmp)

    x, y = (bbox[0][0][2] + int(s * 50), bbox[0][0][1])
    char_dict_num = get_dict(fp="../utils/dict/nums_dict.txt")
    for i in range(4):
        # font = '../fonts/Times New Roman.ttf'
        tmp_str = get_string(char_dict_num, 27, (1, 22))
        val_text = TextString(tmp_str, font_path, char_size=int(char_size*1.2), char_space=int(s * 5))
        val = CharsPic(val_text)
        val.gen_pic(isblur=False, isnosie=True, bboxon=False)
        canvas.paste_img(val.pic, (x, y))
        w, h = val.pic.size
        tmp = {'transcriptions': tmp_str,
               'points': [[x, y],
                          [x + w, y],
                          [x + w, y + h],
                          [x, y + h]]}
        # canvas.draw_rectangle([(x, y),
        #                        (x + w, y + h),
        #                        ], outline='red', width=3)
        label.append(tmp)
        y += (h + 0)

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
    bbox = canvas.get_bbox(text_str2_1_1)
    tmp = {'transcriptions': text_str2_1_1.text,
           'points': [[bbox[0][0][0], bbox[0][0][1]],
                      [bbox[0][0][2], bbox[0][0][1]],
                      [bbox[0][0][2], bbox[0][0][3]],
                      [bbox[0][0][0], bbox[0][0][3]]]}
    # canvas.draw_rectangle(bbox[0][0], outline='red', width=width)
    label.append(tmp)

    tmp_str = get_string(char_dict, 10, (1, 100))
    val_text = TextString(tmp_str, font_path, char_size=char_size)
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][0][0] + int(50 * s), bbox[0][0][1] + int(50 * s)))
    tmp = {'transcriptions': val_text.text,
           'points': [[bbox[0][0][0] + int(50 * s), bbox[0][0][1] + int(50 * s)],
                      [bbox[0][0][0] + int(50 * s) + val.pic.size[0], bbox[0][0][1] + int(50 * s)],
                      [bbox[0][0][0] + int(50 * s) + val.pic.size[0], bbox[0][0][1] + int(50 * s) + val.pic.size[1]],
                      [bbox[0][0][0] + int(50 * s), bbox[0][0][1] + int(50 * s) + val.pic.size[1]]]}
    # canvas.draw_rectangle([(bbox[0][0][0] + int(50 * s), bbox[0][0][1] + int(50 * s)),
    #                        (bbox[0][0][0] + int(50 * s) + val.pic.size[0],
    #                         bbox[0][0][1] + int(50 * s) + val.pic.size[1])],
    #                       outline='red', width=3)
    label.append(tmp)

    str2_1_2 = '合'
    text_str2_1_2 = TextString(text_string=str2_1_2, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str2_1_2, tuple(map(scales, (365, 1080))))

    bbox = canvas.get_bbox(text_str2_1_2)
    tmp = {'transcriptions': text_str2_1_2.text,
           'points': [[bbox[0][0][0], bbox[0][0][1]],
                      [bbox[0][0][2], bbox[0][0][1]],
                      [bbox[0][0][2], bbox[0][0][3]],
                      [bbox[0][0][0], bbox[0][0][3]]]}
    # canvas.draw_rectangle(bbox[0][0], outline='red')
    label.append(tmp)

    str2_1_2_2 = '计'
    text_str2_1_2_2 = TextString(text_string=str2_1_2_2, font=font_path, char_size=char_size,
                                 color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str2_1_2_2, tuple(map(scales, (565, 1080))))

    bbox = canvas.get_bbox(text_str2_1_2_2)
    tmp = {'transcriptions': text_str2_1_2_2.text,
           'points': [[bbox[0][0][0], bbox[0][0][1]],
                      [bbox[0][0][2], bbox[0][0][1]],
                      [bbox[0][0][2], bbox[0][0][3]],
                      [bbox[0][0][0], bbox[0][0][3]]]}
    # canvas.draw_rectangle(bbox[0][0], outline='red')
    label.append(tmp)

    str2_2_1 = '规格型号'
    text_str2_2_1 = TextString(text_string=str2_2_1, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str2_2_1, tuple(map(scales, (900, 630))))

    bbox = canvas.get_bbox(text_str2_2_1)
    tmp = {'transcriptions': text_str2_2_1.text,
           'points': [[bbox[0][0][0], bbox[0][0][1]],
                      [bbox[0][0][2], bbox[0][0][1]],
                      [bbox[0][0][2], bbox[0][0][3]],
                      [bbox[0][0][0], bbox[0][0][3]]]}
    # canvas.draw_rectangle([(bbox[0][0][0], bbox[0][0][1]),
    #                        (bbox[0][0][2], bbox[0][0][3])], outline='red', width=3)
    label.append(tmp)

    str2_2_1 = '单位'
    text_str2_2_1 = TextString(text_string=str2_2_1, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str2_2_1, tuple(map(scales, (1172, 630))))
    bbox = text_str2_2_1.get_bbox()
    tmp = {'transcriptions': text_str2_2_1.text,
           'points': [[bbox[0][0], bbox[0][1]],
                      [bbox[0][2], bbox[0][1]],
                      [bbox[0][2], bbox[0][3]],
                      [bbox[0][0], bbox[0][3]]]}
    # canvas.draw_rectangle([(bbox[0][0], bbox[0][1]),
    #                        (bbox[0][2], bbox[0][3])], outline='red', width=3)

    label.append(tmp)

    str2_2_1 = '数量'
    text_str2_2_1 = TextString(text_string=str2_2_1, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=int(s * 25))
    canvas.draw_text_string(text_str2_2_1, tuple(map(scales, (1350, 630))))

    bbox = canvas.get_bbox(text_str2_2_1)
    tmp = {'transcriptions': text_str2_2_1.text,
           'points': [[bbox[0][0][0], bbox[0][0][1]],
                      [bbox[0][0][2], bbox[0][0][1]],
                      [bbox[0][0][2], bbox[0][0][3]],
                      [bbox[0][0][0], bbox[0][0][3]]]}
    # canvas.draw_rectangle([(bbox[0][0][0], bbox[0][0][1]),
    #                        (bbox[0][0][2], bbox[0][0][3])], outline='red', width=3)
    label.append(tmp)

    tmp_str = get_string(char_dict_num2, 1, (1, 10))
    val_text = TextString(tmp_str, font_path2, char_size=char_size)
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][0][0] + int(s * 50), bbox[0][0][1] + int(s * 50)))

    tmp = {'transcriptions': val_text.text,
           'points': [[bbox[0][0][0] + int(s * 50), bbox[0][0][1] + int(s * 50)],
                      [bbox[0][0][0] + int(s * 50) + val.pic.size[0], bbox[0][0][1] + int(s * 50)],
                      [bbox[0][0][0] + int(s * 50) + val.pic.size[0], bbox[0][0][1] + int(s * 50) + val.pic.size[1]],
                      [bbox[0][0][0] + int(s * 50), bbox[0][0][1] + int(s * 50) + val.pic.size[1]]]}
    # canvas.draw_rectangle([(bbox[0][0][0] + int(s * 50), bbox[0][0][1] + int(s * 50)),
    #                        (bbox[0][0][0] + int(s * 50) + val.pic.size[0],
    #                         bbox[0][0][1] + int(s * 50) + val.pic.size[1])], outline='red', width=3)
    label.append(tmp)

    str2_3_1 = '单价'
    text_str2_3_1 = TextString(text_string=str2_3_1, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=int(s * 25))
    canvas.draw_text_string(text_str2_3_1, tuple(map(scales, (1580, 630))))

    bbox = canvas.get_bbox(text_str2_3_1)
    tmp = {'transcriptions': text_str2_3_1.text,
           'points': [[bbox[0][0][0], bbox[0][0][1]],
                      [bbox[0][0][2], bbox[0][0][1]],
                      [bbox[0][0][2], bbox[0][0][3]],
                      [bbox[0][0][0], bbox[0][0][3]]]}
    # canvas.draw_rectangle(bbox[0][0], outline='red', width=3)
    label.append(tmp)
    tmp_str1 = get_string(char_dict_num2,random.randint(2,5),(1,10))
    tmp_str2 = get_string(char_dict_num2,2,(1,10))
    tmp_str = tmp_str1+'.'+tmp_str2
    val_text = TextString(tmp_str, font_path2, char_size=char_size)
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][0][0] - int(s * 20), bbox[0][0][1] + int(s * 50)))
    tmp = {'transcriptions': val_text.text,
           'points': [[bbox[0][0][0] - int(s * 20), bbox[0][0][1] + int(s * 50)],
                      [bbox[0][0][0] - int(s * 20) + val.pic.size[0], bbox[0][0][1] + int(s * 50)],
                      [bbox[0][0][0] - int(s * 20) + val.pic.size[0], bbox[0][0][1] + int(s * 50) + val.pic.size[1]],
                      [bbox[0][0][0] - int(s * 20), bbox[0][0][1] + int(s * 50) + val.pic.size[1]]]}
    # canvas.draw_rectangle([(bbox[0][0][0] - int(s * 20), bbox[0][0][1] + int(s * 50)),
    #                        (bbox[0][0][0] - int(s * 20) + val.pic.size[0],
    #                         bbox[0][0][1] + int(s * 50) + val.pic.size[1])], outline='red', width=3)
    label.append(tmp)

    str2_4_1 = '金额'
    text_str2_4_1 = TextString(text_string=str2_4_1, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=int(s * 60))
    canvas.draw_text_string(text_str2_4_1, tuple(map(scales, (1860, 630))))
    bbox = text_str2_4_1.get_bbox()
    tmp = {'transcriptions': text_str2_4_1.text,
           'points': [[bbox[0][0], bbox[0][1]],
                      [bbox[0][2], bbox[0][1]],
                      [bbox[0][2], bbox[0][3]],
                      [bbox[0][0], bbox[0][3]]]}
    # canvas.draw_rectangle(bbox[0], outline='red', width=3)
    label.append(tmp)
    tmp_str1 = get_string(char_dict_num2, random.randint(2, 5), (1, 10))
    tmp_str2 = get_string(char_dict_num2, 2, (1, 10))
    tmp_str = tmp_str1 + '.' + tmp_str2
    val_text = TextString(tmp_str, font_path2, char_size=char_size)
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][0] + int(s * 30), bbox[0][1] + int(s * 50)))
    tmp = {'transcriptions': val_text.text,
           'points': [[bbox[0][0] + int(s * 30), bbox[0][1] + int(s * 50)],
                      [bbox[0][0] + int(s * 30) + val.pic.size[0], bbox[0][1] + int(s * 50)],
                      [bbox[0][0] + int(s * 30) + val.pic.size[0], bbox[0][1] + int(s * 50) + val.pic.size[1]],
                      [bbox[0][0] + int(s * 30), bbox[0][1] + int(s * 50) + val.pic.size[1]]]}
    # canvas.draw_rectangle([(bbox[0][0] + int(s * 30), bbox[0][1] + int(s * 50)),
    #                        (bbox[0][0] + int(s * 30) + val.pic.size[0],
    #                         bbox[0][1] + int(s * 50) + val.pic.size[1])], outline='red', width=3)
    label.append(tmp)

    bbox = canvas.get_bbox(text_str2_4_1)
    tmp_str1 = get_string(char_dict_num2, random.randint(2, 5), (1, 10))
    tmp_str2 = get_string(char_dict_num2, 2, (1, 10))
    tmp_str = '￥'+tmp_str1 + '.' + tmp_str2
    val_text = TextString(tmp_str, font_path, char_size=char_size)
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][0][0] + int(s * 10), bbox[0][0][1] + int(s * 450)))
    tmp = {'transcriptions': val_text.text,
           'points': [[bbox[0][0][0] + int(s * 10), bbox[0][0][1] + int(s * 450)],
                      [bbox[0][0][0] + int(s * 10) + val.pic.size[0], bbox[0][0][1] + int(s * 450)],
                      [bbox[0][0][0] + int(s * 10) + val.pic.size[0], bbox[0][0][1] + int(s * 450) + val.pic.size[1]],
                      [bbox[0][0][0] + int(s * 10), bbox[0][0][1] + int(s * 450) + val.pic.size[1]]]}
    # canvas.draw_rectangle([(bbox[0][0][0] + int(s * 10), bbox[0][0][1] + int(s * 450)),
    #                        (bbox[0][0][0] + int(s * 10) + val.pic.size[0],
    #                         bbox[0][0][1] + int(s * 450) + val.pic.size[1])], outline='red', width=3)
    label.append(tmp)

    str2_5_1 = '税率'
    text_str2_5_1 = TextString(text_string=str2_5_1, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str2_5_1, tuple(map(scales, (2150, 630))))

    bbox = text_str2_5_1.get_bbox()
    tmp = {'transcriptions': text_str2_5_1.text,
           'points': [[bbox[0][0], bbox[0][1]],
                      [bbox[0][2], bbox[0][1]],
                      [bbox[0][2], bbox[0][3]],
                      [bbox[0][0], bbox[0][3]]]}
    # canvas.draw_rectangle(bbox[0], outline='red', width=3)
    label.append(tmp)
    tmp_str = get_string(char_dict_num2, random.randint(1,2), (1, 10)) + '%'
    val_text = TextString(tmp_str, font_path, char_size=char_size)
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][0] + int(s * 25), bbox[0][1] + int(s * 50)))
    tmp = {'transcriptions': val_text.text,
           'points': [[bbox[0][0] + int(s * 25), bbox[0][1] + int(s * 50)],
                      [bbox[0][0] + int(s * 25) + val.pic.size[0], bbox[0][1] + int(s * 50)],
                      [bbox[0][0] + int(s * 25) + val.pic.size[0], bbox[0][1] + int(s * 50) + val.pic.size[1]],
                      [bbox[0][0] + int(s * 25), bbox[0][1] + int(s * 50) + val.pic.size[1]]]}
    # canvas.draw_rectangle([(bbox[0][0] + int(s * 25), bbox[0][1] + int(s * 50)),
    #                        (bbox[0][0] + int(s * 25) + val.pic.size[0], bbox[0][1] + int(s * 50) + val.pic.size[1])],
    #                       outline='red', width=3)
    label.append(tmp)

    str2_2_1 = '税额'
    text_str2_2_1 = TextString(text_string=str2_2_1, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=int(s * 60))
    canvas.draw_text_string(text_str2_2_1, tuple(map(scales, (2340, 630))))

    bbox = text_str2_2_1.get_bbox()
    tmp = {'transcriptions': text_str2_2_1.text,
           'points': [[bbox[0][0], bbox[0][1]],
                      [bbox[0][2], bbox[0][1]],
                      [bbox[0][2], bbox[0][3]],
                      [bbox[0][0], bbox[0][3]]]}
    # canvas.draw_rectangle(bbox[0], outline='red', width=3)
    label.append(tmp)

    tmp_str1 = get_string(char_dict_num2, random.randint(2, 5), (1, 10))
    tmp_str2 = get_string(char_dict_num2, 2, (1, 10))
    tmp_str = tmp_str1 + '.' + tmp_str2
    val_text = TextString(tmp_str, font_path2, char_size=char_size)
    # val_text = TextString('9999.00', font_path2, char_size=int(s * 50))
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][0] + int(s * 30), bbox[0][1] + int(s * 50)))

    tmp = {'transcriptions': val_text.text,
           'points': [[bbox[0][0] + int(s * 30), bbox[0][1] + int(s * 50)],
                      [bbox[0][0] + int(s * 30) + val.pic.size[0], bbox[0][1] + int(s * 50)],
                      [bbox[0][0] + int(s * 30) + val.pic.size[0], bbox[0][1] + int(s * 50) + val.pic.size[1]],
                      [bbox[0][0] + int(s * 30), bbox[0][1] + int(s * 50) + val.pic.size[1]]]}
    # canvas.draw_rectangle([(bbox[0][0] + int(s * 30), bbox[0][1] + int(s * 50)),
    #                        (bbox[0][0] + int(s * 30) + val.pic.size[0],
    #                         bbox[0][1] + int(s * 50) + val.pic.size[1])], outline='red', width=3)
    label.append(tmp)

    tmp_str1 = get_string(char_dict_num2, random.randint(2, 5), (1, 10))
    tmp_str2 = get_string(char_dict_num2, 2, (1, 10))
    tmp_str = '￥' + tmp_str1 + '.' + tmp_str2
    val_text = TextString(tmp_str, font_path, char_size=char_size)
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][0] + int(s * 10), bbox[0][1] + int(s * 450)))
    tmp = {'transcriptions': val_text.text,
           'points': [[bbox[0][0] + int(s * 10), bbox[0][1] + int(s * 450)],
                      [bbox[0][0] + int(s * 10) + val.pic.size[0], bbox[0][1] + int(s * 450)],
                      [bbox[0][0] + int(s * 10) + val.pic.size[0], bbox[0][1] + int(s * 450) + val.pic.size[1]],
                      [bbox[0][0] + int(s * 10), bbox[0][1] + int(s * 450) + val.pic.size[1]]]}
    # canvas.draw_rectangle([(bbox[0][0] + int(s * 10), bbox[0][1] + int(s * 450)),
    #                        (bbox[0][0] + int(s * 10) + val.pic.size[0], bbox[0][1] + int(s * 450) + val.pic.size[1])],
    #                       outline='red', width=3)
    label.append(tmp)

    # 第三行
    canvas.draw_rectangle(tuple(map(scales, (200, 1140, 820, 1240))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(scales, (820, 1140, 2600, 1240))), outline=rec_color, width=width)

    str3_1_1 = '价税合计（大写）'
    text_str3_1_1 = TextString(text_string=str3_1_1, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=int(s * 10))
    canvas.draw_text_string(text_str3_1_1, tuple(map(scales, (330, 1160))))

    bbox = text_str3_1_1.get_bbox()
    tmp = {'transcriptions': text_str3_1_1.text,
           'points': [[bbox[0][0], bbox[0][1]],
                      [bbox[0][2], bbox[0][1]],
                      [bbox[0][2], bbox[0][3]],
                      [bbox[0][0], bbox[0][3]]]}
    # canvas.draw_rectangle(bbox[0], outline='red', width=3)
    label.append(tmp)
    tmp_str = get_string(char_dict, random.randint(12, 20), (1, 1000))
    val_text = TextString(tmp_str, font_path, char_size=char_size)
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (int(s * 850), bbox[0][1]))
    tmp = {'transcriptions': val_text.text,
           'points': [[int(s * 850), bbox[0][1]],
                      [int(s * 850) + val.pic.size[0], bbox[0][1]],
                      [int(s * 850) + val.pic.size[0], bbox[0][1] + val.pic.size[1]],
                      [int(s * 850), bbox[0][1] + val.pic.size[1]]]}
    # canvas.draw_rectangle([(int(s * 850), bbox[0][1]),
    #                        (int(s * 850) + val.pic.size[0], bbox[0][1] + val.pic.size[1])],
    #                       outline='red', width=3)
    label.append(tmp)

    str3_2_1 = '（小写）'
    text_str3_2_1 = TextString(text_string=str3_2_1, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=int(s * 10))
    canvas.draw_text_string(text_str3_2_1, tuple(map(scales, (1920, 1160))))
    bbox = text_str3_2_1.get_bbox()

    tmp_str1 = get_string(char_dict_num2, random.randint(2, 5), (1, 10))
    tmp_str2 = get_string(char_dict_num2, 2, (1, 10))
    tmp_str = '￥' + tmp_str1 + '.' + tmp_str2
    val_text = TextString(tmp_str, font_path, char_size=char_size)
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][2], bbox[0][1]))
    tmp = {'transcriptions': str3_2_1 + val_text.text,
           'points': [[bbox[0][0], bbox[0][1]],
                      [bbox[0][2] + val.pic.size[0], bbox[0][1]],
                      [bbox[0][2] + val.pic.size[0], bbox[0][1] + val.pic.size[1]],
                      [bbox[0][0], bbox[0][1] + val.pic.size[1]]]}
    # canvas.draw_rectangle([(bbox[0][0], bbox[0][1]),
    #                        (bbox[0][2] + val.pic.size[0], bbox[0][1] + val.pic.size[1])],
    #                       outline='red', width=3)
    label.append(tmp)

    # 第四行
    canvas.draw_rectangle(tuple(map(scales, (200, 1240, 290, 1500))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(scales, (290, 1240, 1580, 1500))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(scales, (1580, 1240, 1640, 1500))), outline=rec_color, width=width)
    canvas.draw_rectangle(tuple(map(scales, (1640, 1240, 2600, 1500))), outline=rec_color, width=width)

    str4 = '销售方'
    text_str4 = TextString(text_string=str4, font=font_path, char_size=char_size,
                           color=font_color, direction='ttb', line_space=0, char_space=int(s * 40))
    canvas.draw_text_string(text_str4, tuple(map(scales, (230, 1280))))

    bbox = text_str4.get_bbox()
    tmp = {'transcriptions': text_str4.text,
           'points': [[bbox[0][0], bbox[0][1]],
                      [bbox[0][2], bbox[0][1]],
                      [bbox[0][2], bbox[0][3]],
                      [bbox[0][0], bbox[0][3]]]}
    # canvas.draw_rectangle(bbox[0], outline='red', width=3)
    label.append(tmp)

    str4_2_1 = '名'
    text_str4_2_1 = TextString(text_string=str4_2_1, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str4_2_1, tuple(map(scales, (305, 1250))))
    bbox = text_str4_2_1.get_bbox()
    tmp = {'transcriptions': text_str4_2_1.text,
           'points': [[bbox[0][0], bbox[0][1]],
                      [bbox[0][2], bbox[0][1]],
                      [bbox[0][2], bbox[0][3]],
                      [bbox[0][0], bbox[0][3]]]}
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
    tmp = {'transcriptions': str4_2_1_2 + val_text.text,
           'points': [[bbox[0][0] + 1, bbox[0][1]],
                      [bbox[0][2] + 1 + val.pic.size[0], bbox[0][1]],
                      [bbox[0][2] + 1 + val.pic.size[0], bbox[0][1] + val.pic.size[1]],
                      [bbox[0][0] + 1, bbox[0][1] + val.pic.size[1]]]}
    # canvas.draw_rectangle([(bbox[0][0] + 1, bbox[0][1]),
    #                        (bbox[0][2] + 1 + val.pic.size[0], bbox[0][1] + val.pic.size[1])], outline='red', width=3)
    label.append(tmp)

    str4_2_2 = '纳税人识别号：'
    text_str4_2_2 = TextString(text_string=str4_2_2, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str4_2_2, tuple(map(scales, (305, 1315))))

    bbox = text_str4_2_2.get_bbox()

    tmp_str = get_string(char_dict_num2, 18, (1, 10))
    val_text = TextString(tmp_str, font_path2, char_size=char_size)
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][2] + 1, bbox[0][1]))
    tmp = {'transcriptions': str4_2_2 + val_text.text,
           'points': [[bbox[0][0] + 1, bbox[0][1]],
                      [bbox[0][2] + 1 + val.pic.size[0], bbox[0][1]],
                      [bbox[0][2] + 1 + val.pic.size[0], bbox[0][1] + val.pic.size[1]],
                      [bbox[0][0] + 1, bbox[0][1] + val.pic.size[1]]]}
    # canvas.draw_rectangle([(bbox[0][0] + 1, bbox[0][1]),
    #                        (bbox[0][2] + 1 + val.pic.size[0], bbox[0][1] + val.pic.size[1])], outline='red', width=3)
    label.append(tmp)

    str4_2_3 = '地址、电话:'
    text_str4_2_3 = TextString(text_string=str4_2_3, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=8)
    canvas.draw_text_string(text_str4_2_3, tuple(map(scales, (305, 1375))))
    bbox = text_str4_2_3.get_bbox()

    tmp_str = get_string(char_dict, random.randint(8, 16), (1, 100))
    val_text1 = TextString(tmp_str, font_path, char_size=char_size)
    # val_text1 = TextString('电动机我记得叫我定位', font_path, char_size=int(s * 40))
    val1 = CharsPic(val_text1)
    val1.gen_pic(isblur=False, isnosie=True, bboxon=False)
    w, h = val1.pic.size
    canvas.paste_img(val1.pic, (bbox[0][2] + 1, bbox[0][1]))

    tmp_str = get_string(char_dict_num2, random.randint(10, 16), (1, 10))
    val_text = TextString(tmp_str, font_path2, char_size=int(char_size*0.8))
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][2] + int(s * 50) + w, bbox[0][1] + int(s * 10)))

    tmp = {'transcriptions': str4_2_3 + val_text1.text + val_text.text,
           'points': [[bbox[0][0], bbox[0][1]],
                      [bbox[0][2] + int(s * 50) + w + val.pic.size[0], bbox[0][1]],
                      [bbox[0][2] + int(s * 50) + w + val.pic.size[0], bbox[0][1] + int(s * 10) + val.pic.size[1]],
                      [bbox[0][0], bbox[0][1] + int(s * 10) + val.pic.size[1]]]}
    # canvas.draw_rectangle([(bbox[0][0], bbox[0][1]),
    #                        (bbox[0][2] + int(s * 50) + w + val.pic.size[0],
    #                         bbox[0][1] + int(s * 10) + val.pic.size[1])],
    #                       outline='red', width=3)
    label.append(tmp)

    str4_2_4 = '开户行及账号：'
    text_str4_2_4 = TextString(text_string=str4_2_4, font=font_path, char_size=char_size,
                               color=font_color, direction='ltr', line_space=0, char_space=0)
    canvas.draw_text_string(text_str4_2_4, tuple(map(scales, (305, 1440))))

    bbox = text_str4_2_4.get_bbox()

    tmp_str = get_string(char_dict, random.randint(8, 20), (1, 100))
    val_text1 = TextString(tmp_str, font_path, char_size=char_size)
    val1 = CharsPic(val_text1)
    val1.gen_pic(isblur=False, isnosie=True, bboxon=False)
    w, h = val1.pic.size
    canvas.paste_img(val1.pic, (bbox[0][2], bbox[0][1]))

    tmp_str = get_string(char_dict_num2, random.randint(10, 16), (1, 10))
    val_text = TextString(tmp_str, font_path2, char_size=int(char_size*0.8))
    val = CharsPic(val_text)
    val.gen_pic(isblur=False, isnosie=True, bboxon=False)
    canvas.paste_img(val.pic, (bbox[0][2] + int(s * 50) + w, bbox[0][1] + int(s * 10)))

    tmp = {'transcriptions': str4_2_4 + val_text1.text + val_text.text,
           'points': [[bbox[0][0], bbox[0][1]],
                      [bbox[0][2] + int(s * 50) + w + val.pic.size[0], bbox[0][1]],
                      [bbox[0][2] + int(s * 50) + w + val.pic.size[0], bbox[0][1] + int(s * 10) + val.pic.size[1]],
                      [bbox[0][0], bbox[0][1] + int(s * 10) + val.pic.size[1]]]}
    # canvas.draw_rectangle([(bbox[0][0], bbox[0][1]),
    #                        (bbox[0][2] + int(s * 50) + w + val.pic.size[0],
    #                         bbox[0][1] + int(s * 10) + val.pic.size[1])],
    #                       outline='red', width=3)
    label.append(tmp)

    str5 = '备注'
    text_str5 = TextString(text_string=str5, font=font_path, char_size=char_size,
                           color=font_color, direction='ttb', line_space=0, char_space=int(s * 90))
    canvas.draw_text_string(text_str5, tuple(map(scales, (1590, 1280))))

    bbox = text_str5.get_bbox()
    tmp = {'transcriptions': text_str5.text,
           'points': [[bbox[0][0], bbox[0][1]],
                      [bbox[0][2], bbox[0][1]],
                      [bbox[0][2], bbox[0][3]],
                      [bbox[0][0], bbox[0][3]]]}
    # canvas.draw_rectangle(bbox[0], outline='red', width=3)
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

    tmp = {'transcriptions': str5_1 + val_text.text,
           'points': [[bbox[0][0], bbox[0][1]],
                      [bbox[0][2] + val.pic.size[0], bbox[0][1]],
                      [bbox[0][2] + val.pic.size[0], bbox[0][1] + val.pic.size[1]],
                      [bbox[0][0], bbox[0][1] + val.pic.size[1]]]}
    # canvas.draw_rectangle([(bbox[0][0], bbox[0][1]),
    #                        (bbox[0][2] + val.pic.size[0], bbox[0][1] + val.pic.size[1])], outline='red', width=3)
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

    tmp = {'transcriptions': str5_2 + val_text.text,
           'points': [[bbox[0][0], bbox[0][1]],
                      [bbox[0][2] + val.pic.size[0], bbox[0][1]],
                      [bbox[0][2] + val.pic.size[0], bbox[0][1] + val.pic.size[1]],
                      [bbox[0][0], bbox[0][1] + val.pic.size[1]]]}
    # canvas.draw_rectangle([(bbox[0][0] + 1, bbox[0][1]),
    #                        (bbox[0][2] + 1 + val.pic.size[0], bbox[0][1] + val.pic.size[1])], outline='red', width=3)
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

    tmp = {'transcriptions': str5_3 + val_text.text,
           'points': [[bbox[0][0], bbox[0][1]],
                      [bbox[0][2] + val.pic.size[0], bbox[0][1]],
                      [bbox[0][2] + val.pic.size[0], bbox[0][1] + val.pic.size[1]],
                      [bbox[0][0], bbox[0][1] + val.pic.size[1]]]}
    # canvas.draw_rectangle([(bbox[0][0] + 1, bbox[0][1]),
    #                        (bbox[0][2] + 1 + val.pic.size[0], bbox[0][1] + val.pic.size[1])], outline='red', width=3)
    label.append(tmp)

    str5_4 = '销售方：（章）'
    text_str5_4 = TextString(text_string=str5_4, font=font_path, char_size=char_size,
                             color=font_color, direction='ltr', line_space=0, char_space=int(s * 10))
    canvas.draw_text_string(text_str5_4, tuple(map(scales, (1990, 1510))))

    bbox = text_str5_4.get_bbox()
    tmp = {'transcriptions': text_str5_4.text,
           'points': [[bbox[0][0], bbox[0][1]],
                      [bbox[0][2], bbox[0][1]],
                      [bbox[0][2], bbox[0][3]],
                      [bbox[0][0], bbox[0][3]]]}
    # canvas.draw_rectangle(bbox[0], outline='red', width=3)
    label.append(tmp)
    print('saved in ./receipt.jpg')
    canvas.save('./receipt.jpg')
    print(label)


def ltr_test():
    font_path = "../fonts/NotoSansHans-Bold.otf"
    font_color = (163, 131, 80)
    rec_color = 'black'
    char_size = 100
    # 返回PIL.Image对象
    canvas = CanvasImage(size=(500, 500), color='white')

    str_right = '第三联发票\n联购买方记账'
    text_str_right = TextString(text_string=str_right, font=font_path, char_size=char_size,
                                color=font_color, direction='ltr', line_space=10, char_space=20)
    canvas.draw_text_string(text_str_right, (10, 10))
    # print('a',text_str_right.vaild_text_bbox)
    # print('b',text_str_right.bbox)
    bboxes, valid_text_bbox = canvas.draw_bbox(text_str_right, offset=5)
    # print('a', text_str_right.vaild_text_bbox)
    # print('b', text_str_right.bbox)
    # _, bbox2 = canvas.get_bbox(text_str_right)
    # print('a', text_str_right.vaild_text_bbox)
    # print('b', text_str_right.bbox)
    print(bboxes)
    print(valid_text_bbox)
    # get_labels(valid_text_bbox, 'test')
    canvas.save('./ltr.jpg')



if __name__ == '__main__':
    # font_color = (163, 131, 80)
    font_color = 'black'
    receipt()
    scale = 1
    set_config(int(1419 * scale), int(813 * scale))
    # ltr_test()

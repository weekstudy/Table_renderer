#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
"""
@author:zhouqiang
@file:PubTabNet_CH.py
@NAME:Table_renderer
@time:2021/09/11
@IDE: PyCharm

"""
import os
import sys
import jsonlines
__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append('.')

from configure.Config import *
from utils.utils import *
from pubtabnet_ch.pubtabnet import *
from log.log import *


def gen_pubtabnet_ch(num, dt, input_dir, output_dir, fp, kind='RARE'):
    config = set_config()
    font_type = config['font']
    font_color = config['font_color']
    dict_file = config['dict_file']
    char_dict = get_dict(fp=dict_file)
    n = len(char_dict)
    print('字典字符个数为：', n)

    end = num
    output_basename = 'pubtabnet_ch_{}_{}/'.format(dt, end)
    output_labels = output_dir + 'pubtabnet_ch{}_labels_{}.txt'.format(dt, end)
    output_jsonl = output_dir + 'pubtabnet_ch_{}_{}.jsonl'.format(dt, end)
    log_file = 'pubtabnet_ch_train_{}_{}.log' .format(dt, end)

    output_images = output_dir + output_basename
    config['input_dir'] = input_dir
    config['jsonlfile'] = fp
    config['output_dir'] = output_dir
    save_config(config)

    if not os.path.exists(output_images):
        os.makedirs(output_images)
        os.chmod(output_images, 0o777)
    logger = Logger(fp=output_dir+log_file)
    logger.info('images saved in ' + output_images)
    logger.info('labels saved in' + output_jsonl)
    logger.info('log file saved in' + output_dir+log_file)
    logger.info('==' * 30)

    items = get_items(jsonl_file=fp, start=0, end=end)
    cnt = 0
    pics = []
    for item in items:
        cnt += 1
        pic = PubTabNet(input_dir, item)
        # if pic.img_name == 'PMC1314922_002_01.png':
        img_path = os.path.join(output_images, pic.img_name)

        pil_img = pic.gen_img(font_type, char_dict, fp=None, scales=1, bboxon=False, lineon=False)
        pics.append(pic)
        # print(img_path)
        logger.info(str(cnt)+':'+img_path)
        pil_img.save(img_path)

    if kind == "DB":
        write_labels(pics, output_labels, output_basename)
    elif kind == "RARE":
        write_jsonl(pics, output_jsonl)

    elif kind == 'ALL':
        write_labels(pics, output_labels, output_basename)
        write_jsonl(pics, output_jsonl)


def gen_pubtabnet_box_img(num, dt, input_dir, output_dir, fp, kind='RARE'):
    config = set_config()
    font_type = config['font']
    font_color = config['font_color']
    dict_file = config['dict_file']
    char_dict = get_dict(fp=dict_file)
    n = len(char_dict)
    print('字典字符个数为：', n)

    end = num
    output_basename = 'pubtabnet_box_{}_{}/'.format(dt, end)
    output_labels = output_dir + 'pubtabnet_{}_labels_{}.txt'.format(dt, end)
    output_jsonl = output_dir + 'PubTabNet_box_{}_{}.jsonl'.format(dt, end)

    output_images = output_dir + output_basename
    config['input_dir'] = input_dir
    config['jsonlfile'] = fp
    config['output_dir'] = output_dir
    save_config(config)

    if not os.path.exists(output_images):
        os.makedirs(output_images)
        os.chmod(output_images, 0o777)

    items = get_items(jsonl_file=fp, start=0, end=end)
    cnt = 0
    pics = []
    for item in items:
        cnt += 1
        pic = PubTabNet(input_dir, item)
        # if pic.img_name == 'PMC1802082_003_00.png':
        img_path = os.path.join(output_images, pic.img_name)
        print('line 207 :', cnt, '->', img_path)
        # 表格结构
        pic.get_structure()
        pil_img = pic.draw_structure()
        pics.append(pic)
        pil_img.save(img_path)

    if kind == "RARE":
        write_jsonl(pics, output_jsonl)

    elif kind == 'ALL':
        write_labels(pics, output_labels, output_basename)
        write_jsonl(pics, output_jsonl)

    print(cnt)


def write_labels(pics, output_labels, output_basename):
    with open(output_labels, 'w') as fw:
        for pic in pics:
            lables = []
            pic_path = output_basename + pic.img_name
            for token_bbox in pic.tokens_bboxes:
                tmp = token_bbox['bbox']
                points = [[tmp[0], tmp[1]], [tmp[2], tmp[1]],
                          [tmp[2], tmp[3]], [tmp[0], tmp[3]]]
                result = {"transcription": token_bbox['tokens'], "points": points}
                lables.append(result)
            fw.write(pic_path + '\t' + json.dumps(lables, ensure_ascii=False) + '\n')


def write_jsonl(pics, output_jsonl):
    with jsonlines.open(output_jsonl, 'w') as fw:
        for pic in pics:
            structure = {'tokens': pic.cells_structure_elems}
            html = {'cells': pic.cells_content,
                    'structure': structure}
            label = {'filename': pic.img_name,
                     'split': pic.split,
                     'imgid': pic.imgid,
                     'html': html}
            fw.write(label)


def calibrate_structure():
    jsonl_file = '../examples/output_0-10000.jsonl'
    input_dir = '../examples/pubtabnet/train1'
    error_label = './label_err.jsonl'
    dt = 'train'
    end = 'inf'
    items = get_items(jsonl_file=jsonl_file, start=0, end=end)

    cnt = 0
    error = 0
    imgs = []
    for item in items:
        cnt += 1
        pic = PubTabNet(input_dir, item)
        # if pic.img_name == 'PMC3241372_004_00.png':
        # img_path = os.path.join(output_images, pic.img_name)
        # 表格结构
        try:
            pic.get_structure()
        except Exception as e:
            # pil_img = pic.draw_structure()
            print('line 207 :', cnt, '->', pic.img_name)
            imgs.append(item)
            error += 1
            continue
    print('total error', error, end='-->save in ')
    with jsonlines.open(error_label, 'w') as fw:
        for img_name in imgs:
            fw.write(img_name)

    print("%s Done" % error_label)


if __name__ == '__main__':
    calibrate_structure()


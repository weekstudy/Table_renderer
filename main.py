#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from TextString.TextString import *
from Canvas.Canvas import *
from tools.TextImage import *
from tools.Receipt import *
from tools.Receipts2 import *
from tools.PubTabNet_CH import *
from tools.images import *
from configure.Config import *
from log.log import *


def gen_batch_images():
    batch = 1
    # path1 = './images_%s/' % str(batch)
    path1 = './images_%s/images/' % str(batch)
    path2 = './images_%s/labels/' % str(batch)

    for i in range(batch):
        print('line 293 i:', i)
        gen_image(i, img_path=path1, label_path=path2)


def gen_receipts():
    num = 1
    labels = []

    output_dir = './receipts/'
    # output_dir = '../Paddle_OCR/train_data/icdar2015/text_localization/'

    labels_txt = './receipts_train_labels_%d_v3.txt' % num
    output_basename = 'receipts_train_%d_v3/' % num
    output_labels = output_dir + labels_txt

    for i in range(num):
        label = receipt(output_dir, output_basename, i)
        labels.append(label)
    with open(output_labels, 'w') as fw:
        for line in labels:
            fw.write(line[0] + '\t' + json.dumps(line[1], ensure_ascii=False) + '\n')
    print("Done")


def gen_receipts2():
    num = 2
    labels = []

    output_dir = './receipts/'

    # output_dir = '../PaddleOCR2.3/train_data/table/synth_receipts/'
    lables_jsonl = 'receipts_train_labels_%d_v3.jsonl' % num
    output_basename = 'receipts_train_%d_v3/' % num
    log_file = 'receipts_train_%d_v3.log' % num
    output_labels2 = output_dir + lables_jsonl

    html_indx = []
    logger = Logger(fp=output_dir + log_file)
    logger.info('images saved in ' + output_dir + output_basename)
    logger.info('labels saved in ' + output_labels2)
    logger.info('log file saved in ' + output_dir + log_file)
    logger.info('==' * 30)
    for i in range(num):
        tmp_i = random.randint(1, 3)
        label = receipt2(output_dir, output_basename, i, tmp_i, logger)
        labels.append(label)
        html_indx.append(tmp_i)

    jsonl_lines = gen_recepits_html(labels=labels, dt='train', index=html_indx)
    with jsonlines.open(output_labels2, 'w') as fw:
        print('saved in ', output_labels2)
        for item in jsonl_lines:
            fw.write(item)
    os.chmod(output_labels2, 0o777)
    print("Done")


def gen_pubtabnet():
    input_dir = './examples/pubtabnet/train1'
    jsonl_file = './examples/output_0-10000.jsonl'
    # jsonl_file = '/Users/zhouqiang/YaSpeed/Table_renderer/examples/PubTabNet_2.0.0_val.jsonl'
    output_dir = './pubtabnet/'

    # DB label
    # output_dir = '../Paddle_OCR/train_data/icdar2015/text_localization/'
    # jsonl_file = '../Paddle_OCR/train_data/pubtabnet/PubTabNet_2.0.0.jsonl'
    # input_dir = '../Paddle_OCR/train_data/pubtabnet/train'

    # RARE label
    # output_dir = '../PaddleOCR2.3/train_data/table/pubtabnet_ch/'
    # jsonl_file = '../Paddle_OCR/train_data/pubtabnet/PubTabNet_2.0.0.jsonl'
    # input_dir = '../Paddle_OCR/train_data/pubtabnet/train'

    gen_pubtabnet_ch(num=1, dt='train', input_dir=input_dir,
                     output_dir=output_dir, fp=jsonl_file, kind='ALL')


def gen_pubtabnet_box():
    input_dir = './examples/pubtabnet/train1'
    jsonl_file = './examples/output_0-10000.jsonl'
    # jsonl_file = '/Users/zhouqiang/YaSpeed/Table_renderer/examples/PubTabNet_2.0.0_val.jsonl'
    output_dir = './pubtabnet/'
    gen_pubtabnet_box_img(num=10, dt='train', input_dir=input_dir,
                          output_dir=output_dir, fp=jsonl_file, kind='RARE')


if __name__ == '__main__':
    # font = "./fonts/simhei.ttf"
    # font_color = (163, 131, 80)
    # font_color = 'black'

    # gen_image()
    # gen_batch_images()
    gen_pubtabnet()
    # gen_pubtabnet_box()
    # gen_receipts()
    # gen_receipts2()

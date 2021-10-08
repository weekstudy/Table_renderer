#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
"""
@author:zhouqiang
@file:split_pubtabnet.py
@NAME:Table_renderer
@time:2021/09/11
@IDE: PyCharm
 
"""


import jsonlines


def split_dataset():

    jsonl_file = '/home/hadoop/workspace/zhouqiang/Paddle_OCR/train_data/pubtabnet/PubTabNet_2.0.0.jsonl'
    train_jsonl = '/home/hadoop/workspace/zhouqiang/Paddle_OCR/train_data/pubtabnet/PubTabNet_2.0.0_train.jsonl'
    test_jsonl = '/home/hadoop/workspace/zhouqiang/Paddle_OCR/train_data/pubtabnet/PubTabNet_2.0.0_test.jsonl'
    val_jsonl = '/home/hadoop/workspace/zhouqiang/Paddle_OCR/train_data/pubtabnet/PubTabNet_2.0.0_val.jsonl'
    fw_train = jsonlines.open(train_jsonl, 'w')
    fw_test = jsonlines.open(test_jsonl, 'w')
    fw_val = jsonlines.open(val_jsonl, 'w')

    with open(jsonl_file, 'r', encoding="utf8") as fr:
        for line in jsonlines.Reader(fr):
            print(line['imgid'])
            if line['split'] == 'train':
                fw_train.write(line)
            elif line['split'] == 'test':
                fw_test.write(line)
            elif line['split'] == 'val':
                fw_val.write(line)
        print("Done")

    fw_train.close()
    fw_test.close()
    fw_val.close()


if __name__ == '__main__':
    split_dataset()
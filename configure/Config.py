#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
"""
@author:zhouqiang
@file:Config.py
@NAME:Table_renderer
@time:2021/09/11
@IDE: PyCharm
 
"""

from argparse import ArgumentParser, RawDescriptionHelpFormatter
import yaml
from addict import Dict


class ArgsParser(ArgumentParser):
    def __init__(self):
        super(ArgsParser, self).__init__(
            formatter_class=RawDescriptionHelpFormatter)
        # self.add_argument("-c", "--config",default='../configs/det/det_mv3_db.yml', help="configuration file to use")
        self.add_argument("--font", default='./fonts/KaitiGB2312.ttf', help="")
        self.add_argument("--font_color", default='black', type=str, help="")
        self.add_argument("--dict_file", default='./utils/dict/cht_usually_dict.txt', help="")
        self.add_argument("--char_size", default=20, type=int, help="")
        self.add_argument("--h_char_size", default=20, type=int, help="")
        self.add_argument("--line_space", default=0, type=int, help="")


def set_config():
    args = ArgsParser().parse_args()

    config = {'font': args.font,
              'font_color': args.font_color,
              'dict_file': args.dict_file,
              'char_size': args.char_size,
              'h_char_size': args.h_char_size,
              'line_space': args.line_space,

              }
    return config


def save_config(config):
    # config = Dict(config)
    # 保存配置
    with open('./configure/configure.yml', 'w') as fw:
        yaml.dump(config, fw, )

    return config

# a = {'1':1}
# a.update()



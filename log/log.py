#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
"""
@author:zhouqiang
@file:logging.py
@NAME:Table_renderer
@time:2021/09/18
@IDE: PyCharm
 
"""

# import logging
import logging.handlers
import traceback


class Logger(object):
    def __init__(self, name='root', fp=None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        f_handler = logging.FileHandler(fp, mode='a')
        f_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
                '[%(asctime)s] %(name)s %(levelname)s: %(message)s',
                datefmt="%Y/%m/%d %H:%M:%S")
        f_handler.setFormatter(formatter)
        self.logger.addHandler(f_handler)

    def info(self, string):
        self.logger.info(string)

        # # print(s)
        # try:
        #     print(s)
        # except Exception as e:
        #     formatted_lines = traceback.format_exc()
        #     # 将异常信息写进日志文件
        #     logger.info(formatted_lines)
        #     logger.info('ss')


if __name__ == '__main__':

    log = Logger(fp='./test.log')




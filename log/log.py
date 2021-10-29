#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
"""
@author:zhouqiang
@file:logging.py
@NAME:Table_renderer
@time:2021/09/18
@IDE: PyCharm
 
"""

import logging
import sys
import logging.handlers
import traceback
import datetime


class Logger(object):
    def __init__(self, name='root', fp=None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '[%(asctime)s] %(name)s %(levelname)s: %(message)s',
            datefmt="%Y/%m/%d %H:%M:%S")
        # 让容器时间与宿主机时间同步
        logging.Formatter.converter = std_time
        # 输出到屏幕
        stream_handler = logging.StreamHandler(stream=sys.stdout)
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)
        # 输出到文件
        f_handler = logging.FileHandler(fp, mode='a')
        f_handler.setLevel(logging.INFO)
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


def std_time(sec, what):
    local_time = datetime.datetime.now() + datetime.timedelta(hours=8)
    return local_time.timetuple()


if __name__ == '__main__':

    log = Logger(fp='./test.log')
    log.info('tetst')




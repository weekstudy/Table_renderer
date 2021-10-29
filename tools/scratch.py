#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
"""
@AUTHOR:
@FILE:scratch_from_search.py
@NAME:my_insightface
@TIME:2021/01/31
@IDE: PyCharm

"""

import os
import json

import requests
import socket
import ssl
import time
import traceback


# 设置请求超时时间，防止长时间停留在同一个请求
socket.setdefaulttimeout(10)
ssl._create_default_https_context = ssl._create_unverified_context


class ScratchImageFromSougou(object):

    def __init__(self, save_urls_txt='./images_urls', save_images_dir='./images_sougou'):
        self.urls_dir = save_urls_txt
        self.images_dir = save_images_dir
        self.pages_num = 1
        # self.headers = {'user-agent': UserAgent(verify_ssl=False).random}
        self.headers = {'user-agent': 'Mozilla/5.0'}

    def get_image_urls(self, name, total_img=8):

        # pname = name[5:]

        pname = '发票'
        imgs_urls = []
        mod = total_img % self.pages_num
        if mod == 0.0:
            pages_num = total_img // self.pages_num
        else:
            pages_num = total_img // self.pages_num + 1
        for i in range(pages_num):
            # url = 'https://pic.sogou.com/pics?query={}' \
            #       '&mode=1&start={}&reqType=ajax&reqFrom=result&tn=0' \
            #     .format(pname, i * self.pages_num)

            url = 'https://pic.sogou.com/napi/pc/searchList?mode=1&start={}&xml_len=48&query={}'.format(i*48, pname)

            try:
                imgs = requests.get(url, headers=self.headers, timeout=10,allow_redirects=False)
                jd = imgs.json()['data']
                # jd = json.loads(imgs.text)
                jd = jd['items']
                for k, pic_url in enumerate(jd):
                    print(k, pname + '_sougou', pic_url['oriPicUrl'])
                    imgs_urls.append(pic_url['oriPicUrl'])
            except Exception as e:
                print(e.__class__.__name__)
                print(traceback.print_exc())
                continue

        # print(len(imgs_urls))
        # write_urls2txt(name, list(set(imgs_urls)), self.urls_dir, 'sougou')
        return list(set(imgs_urls))

    def get_images(self, pname, save_dir):

        dir, name = os.path.split(save_dir)
        if not os.path.exists(dir):
            os.makedirs(dir)

        names = sorted(os.listdir(dir))
        if name in names:
            print(name + 'scratched')
            return None

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        images_urls = self.get_image_urls(pname,)
        # pname = name.split('_')[1]

        for i, url in enumerate(images_urls):
            filename = os.path.join(save_dir, '%04d' % (i + 1) + '_sougou' + '.jpg')
            print(filename)
            with open(filename, 'wb+') as f:
                try:
                    f.write(requests.get(url, timeout=10, allow_redirects=False).content)
                    # time.sleep(0.1)
                except Exception as e:
                    print(e.__class__.__name__)
                    traceback.print_exc()
                    print('【图片无法下载】', url)
                    continue


if __name__ == '__main__':
    name_list = ['发票']
    scratch_sougou = ScratchImageFromSougou()
    for i in range(len(name_list)):
        # images_urls = scratch_sougou.get_image_urls(name_list[i],)

        path = os.path.join(scratch_sougou.images_dir, name_list[i])
        scratch_sougou.get_images(name_list[i], path)


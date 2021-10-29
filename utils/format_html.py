#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
"""
@author:zhouqiang
@file:format_html.py
@NAME:Table_renderer
@time:2021/09/24
@IDE: PyCharm
 
"""

import re
from bs4 import BeautifulSoup as bs
import jsonlines


def format_html(img):
    ''' Formats HTML code from tokenized annotation of img
    '''
    html_string = '''<html>
                     <head>
                     <meta charset="UTF-8">
                     <style>
                     table, th, td {
                       border: 1px solid black;
                       font-size: 10px;
                     }
                     </style>
                     </head>
                     <body>
                     <table frame="hsides" rules="groups" width="100%%">
                         %s
                     </table>
                     </body>
                     </html>''' % ''.join(img['html']['structure']['tokens'])

    td_list =''.join(img['html']['structure']['tokens'])
    cell_nodes = list(re.finditer(r'(<td[^<>]*>)(</td>)', html_string))
    assert len(cell_nodes) == len(
        img['html']['cells']), 'Number of cells defined in tags does not match the length of cells'
    cells = [''.join(c['tokens']) for c in img['html']['cells']]
    offset = 0
    for n, cell in zip(cell_nodes, cells):
        # 将数据填入对应单元格，第一个分组的结束，第二个分组的开始
        html_string = html_string[:n.end(1) + offset] + cell + html_string[n.start(2) + offset:]
        offset += len(cell)
    # prettify the html
    soup = bs(html_string, features="html.parser")
    html_string = soup.prettify()
    return html_string


if __name__ == '__main__':

    # f = './PubTabNet_Examples.json'
    import os
    # f = './output_0-10000.jsonl'
    f = '../pubtabnet/PubTabNet_ch_train_1.jsonl'
    html_dir = '../pubtabnet/htmls/'
    if not os.path.exists(html_dir):
        os.makedirs(html_dir)
    with open(f, 'r') as fp:
        for item in jsonlines.Reader(fp):
            # if item['filename']=='00000.jpg':
            html_string = format_html(item)
            html = item['filename'][:5]+'.html'
            with open(html_dir+html,'w') as fw:
                fw.write(html_string)
            # display(HTML(html_string))
        #     print(html_string)


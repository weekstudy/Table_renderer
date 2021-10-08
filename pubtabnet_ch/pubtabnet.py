#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
"""
@author:zhouqiang
@file:Excel_Pic.py
@NAME:Table_renderer
@time:2021/08/19
@IDE: PyCharm
 
"""

import os
import copy
import cv2
import jsonlines
import math
import numpy as np
import re
import random

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from TextString.TextString import *


class ExcelPic(object):
    def __init__(self, img_dir, item: dict):
        self.item = item
        self.root = img_dir
        self.img_name = self.item.get('filename', None)
        self.split = self.item.get('split', None)
        self.imgid = self.item.get('imgid', None)
        self.html = self.item.get('html', None)
        # self.cells_structure = ''.join(self.html['structure']['tokens'])
        self.cells_structure_elems = self.html['structure']['tokens']
        self.cells_content = self.html['cells']
        self.src_img = self.src_img()
        self.src_size = self.src_img.size
        self.target_img = None
        self.tokens_bboxes = None
        self.structure = None
        self.cells_record = None
        self.row_span_record = None
        self.col_span_record = None
        self.rows = None
        self.cols = None
        self.draw = None

    def src_img(self):
        img_path = os.path.join(self.root, self.img_name)
        # img_path = '/Users/zhouqiang/YaSpeed/Table_renderer/examples/pubtabnet/train1/PMC1802082_003_00.png'
        pil_img = Image.open(img_path)
        return pil_img

    def gen_img(self, font: str, ch_dict: dict, fp, scales=1, bboxon=False, lineon=True):
        img_font = ImageFont.truetype(font, size=9)
        en_font_path = './fonts/Times New Roman.ttf'
        ch_dict = ch_dict
        target_img = Image.new('RGB', (int(self.src_size[0] + 5), int(self.src_size[1] + 5)), 'white')
        self.draw = ImageDraw.Draw(target_img)
        draw = self.draw
        assert self.html is not None, 'html is None'
        cells_structure = ''.join(self.html['structure']['tokens'])
        cell_nodes = list(re.finditer(r'(<td[^<>]*>)(</td>)', cells_structure))
        cells = self.html['cells']
        assert len(cell_nodes) == len(cells), 'Number of cells defined in tags does not match the length of cells'

        bboxes_list = []
        bboxes_hlist = []

        for cell in cells:
            if len(cell['tokens']) == 0:
                bboxes_list.append([])
                # bboxes_hlist.append(None)
                continue
            bbox = cell.get('bbox', None)
            if bbox is None:
                continue
            bboxes_list.append(list(map(int, bbox)))
            bboxes_hlist.append(abs(bbox[3] - bbox[1]))
        # assert len(bboxes_list) == len(bboxes_hlist), 'the No of bboxes should be equal to the No of bbox_hlist'
        # for indx in range(len(bboxes_hlist)):
        #     if bboxes_hlist[indx] is None:
        #         bboxes_hlist.pop(indx)
        # std_h = max(bboxes_hlist, key=bboxes_hlist.count)
        std_h = min(bboxes_hlist)
        assert std_h != 0, 'the height of most bboxes is zero '
        tmp = []
        res = []
        for a, cell in enumerate(cells):
            # if isinstance(cell, dict):
            # print('line 91',a,cell['tokens'])
            if len(cell['tokens']) == 0:
                # res.append([])
                continue
            bbox = cell.get('bbox', None)
            if bbox is None:
                continue

            bbox = list(map(int, bbox))
            iou_list = cal_IOU(bbox, bboxes_list)
            # 如果返回是数，说明有重叠，则当前框不要，并且记下第几个框与当前框重叠
            for key, val in iou_list.items():
                if val != 0 and val != 1.0:
                    tmp.append(key)
                    # bboxes_list[key] = [0, 0, 0, 0]
            if a in tmp:
                continue
            string = ''.join(cell['tokens'])
            num_strs = list(re.finditer(r'\d+\.?\d*', string))
            en_strs = list(re.finditer(r'[A-Za-z ]+', string))
            # label = re.finditer(r'(^.*<[^<>].*>).*(/.*>)', string)
            # 匹配html中元素标签
            l_label = list(re.finditer(r'<[A-Za-z =0-9]*>', string))
            # todo 这里有可能出现一个单元格里面有连续标签的情况，比如<i>'1'</i><i>'2,2'<i>,
            ls = ''.join(s.group() for s in l_label)
            r_label = list(re.finditer(r'</[A-Za-z 0-9]*>', string))
            rs = ''.join(s.group() for s in r_label)

            tmp_num = ''.join(num_str.group() for num_str in num_strs)
            tmp_string = ''.join(en_str.group() for en_str in en_strs)
            tmp_string2 = string
            # 字母字符串，包括特殊字符，不包括标签<>\</>
            for v in tmp_num + ls + rs:
                tmp_string2 = tmp_string2.replace(v, '')

            tmp_num2 = string
            # 数字字符串,包括特殊字符，不包括标签<>\</>
            for k in tmp_string + ls + rs:
                tmp_num2 = tmp_num2.replace(k, '')

            # 如果英文字符的个数多余数字个数，就替换成中文
            if len(tmp_string2) > len(tmp_num2):
                char_w = 7
                # 假设字体大小为最小高
                char_w = std_h - 1
                img_font = ImageFont.truetype(font, size=char_w)
                text, rows = self.get_text2(bbox, ch_dict, char_w=char_w, char_h=char_w, font=img_font)
                # todo 这里有可能返回0行
                # 把label也替换掉
                tmp_label = []
                subtext_list = text.split('\n')
                for subtext in subtext_list:
                    for char in subtext:
                        tmp_label.append(char)
                tmp_label.insert(0, ls)
                tmp_label.append(rs)
                cell['tokens'] = tmp_label
                if rows == 0 and len(subtext_list) == 1:
                    # 说明只有一行且字体太大被删了
                    print(string, a, text, rows)
                    img_font = ImageFont.truetype(font, size=int(char_w * 0.8))
                    rows = 1
                if len(subtext_list) != rows:
                    print(string, "-->", a, "-->", text, '-->', subtext_list, "-->", rows)
                    raise ValueError(len(subtext_list), rows)
                # assert len((subtext_list)) == rows
                subtext_w, subtext_h = img_font.getsize(subtext_list[0])
                x = bbox[0] + subtext_w
                y = bbox[1] + int(rows * subtext_h)
                tmp_x, tmp_y = bbox[0], bbox[1]
                for subtext in subtext_list:
                    # print('line 152 ',img_font.getsize(subtext))
                    # todo 这里存在有的字无法显示的可能性
                    draw.text((tmp_x, tmp_y), subtext, fill='black', font=img_font)
                    tmp_y += subtext_h

                new_bbox = [bbox[0], bbox[1], x, y]
                cell['bbox'] = new_bbox
                res.append({'tokens': text, 'bbox': new_bbox})
            else:
                # 说明单元格是数字多，不改写
                tmp_img = self.src_img.crop(bbox)
                target_img.paste(tmp_img, bbox)
                new_bbox = [bbox[0], bbox[1], bbox[2], bbox[3]]
                res.append({'tokens': tmp_num2, 'bbox': new_bbox})
        if bboxon:
            for ii in res:
                bbox = ii['bbox']
                draw.rectangle([(bbox[0], bbox[1]), (bbox[2], bbox[3])], outline='red')

        self.tokens_bboxes = res
        self.target_img = target_img
        if lineon:
            self.get_structure()
            self.draw_structure()
        # 释放掉内存
        self.html = None
        self.item = None
        if fp:
            self.target_img.save(fp)

        return self.target_img

    def draw_text(self, text, bbox, font, fill='black'):

        bbox_w = bbox[2] - bbox[0]
        text_w, text_h = font.getsize(text)
        res = []
        if text_w <= bbox_w:
            # 宽度小于原本的宽度，不需要换行
            self.draw.text((bbox[0], bbox[1]), text, fill=fill, font=font)
            self.draw.rectangle([(bbox[0], bbox[1]), (bbox[0] + text_w, bbox[1] + text_h)], outline='red')
            res = [bbox[0], bbox[1], bbox[0] + text_w, bbox[1] + text_h]
        else:
            # 需要换行,那就一个字一个字写
            cur_w = 1
            i = 1
            x, y = bbox[0], bbox[1]
            tmp_w = []
            for char in text:
                char_w, char_h = font.getsize(char)
                if cur_w * char_w <= bbox_w:
                    self.draw.text((x, y), char, fill=fill, font=font)
                    x += char_w
                    cur_w += 1
                    # draw=draw
                else:
                    tmp_w.append((cur_w - 1) * char_w)
                    y += char_h
                    x = bbox[0]
                    self.draw.text((x, y), char, fill=fill, font=font)
                    i += 1
                    cur_w = 1
            new_w = max(tmp_w)
            # assert text_h == char_h
            self.draw.rectangle([(bbox[0], bbox[1]), (bbox[0] + new_w, bbox[1] + i * text_h)], outline='red')
            res = [bbox[0], bbox[1], bbox[0] + new_w, bbox[1] + i * text_h]
        self.draw = self.draw
        return res

    @staticmethod
    def get_text(ch_dict, length):
        n_char = length // 2
        text = ''
        for i in range(n_char):
            char_num = random.randint(1, 100)
            text += ch_dict[char_num]
            # text += '你'
        return text

    @staticmethod
    def get_text2(bbox, ch_dict, char_w=10, char_h=9, font=None):
        # import math
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        if h >= 2 * char_h:  # 说明至少2行
            row = h / char_h - h // char_h
            if 0.8 < row:
                rows = h // char_h + 1
            else:
                rows = h // char_h
        else:
            rows = 1

        # n_char = math.ceil(w / char_w)
        n_char = int(np.ceil(w / char_w))
        text = ''
        for j in range(rows):
            for i in range(n_char):
                char_num = random.randint(1, 2500)
                text += ch_dict[char_num]
                # text += '你'
            text += '\n'
        text = text.strip()

        subtexts = text.strip().split('\n')
        text_w, text_h = font.getsize(subtexts[0])

        w += 5
        if text_w <= w and int(rows * text_h) <= h:
            return text, rows
        elif text_w > w and int(rows * text_h) <= h:
            # 如果文本框宽度大于原本的宽度
            s_w = text_w - w
            tmp_n = int(np.ceil(s_w / char_w))
            new_text = ''
            for subtext in subtexts:
                sub = subtext[:len(subtext) - tmp_n]
                new_text = new_text + sub + '\n'
            new_text = new_text.strip()
            return new_text, rows
        elif text_w <= w and int(rows * text_h) > h:
            # 如果文本框高度大于原本的高度
            s_h = int(rows * text_h) - h
            tmp_h = int(np.ceil(s_h / text_h))
            assert len(subtexts) == rows, 'the rows should be equally the No of subtexts'
            new_subtexts = subtexts[:rows - tmp_h]
            new_text = ''
            for sub in new_subtexts:
                new_text += sub + '\n'
            new_text = new_text.strip()
            return new_text, len(new_subtexts)
        elif text_w > w and int(rows * text_h) > h:
            s_w = text_w - w
            tmp_n = int(np.ceil(s_w / char_w))
            s_h = int(rows * text_h) - h
            tmp_h = int(np.ceil(s_h / text_h))
            new_text = ''
            assert len(subtexts) == rows, 'the rows should be equally the No of subtexts'
            for i in range(rows - tmp_h):
                sub = subtexts[i]
                tmp_sub = sub[:len(sub) - tmp_n]
                new_text = new_text + tmp_sub + '\n'
            new_text = new_text.strip()

            return new_text, rows - tmp_h

    def get_structure(self):
        # 画出表结构
        scales = 1
        # target_img = Image.new('RGB', (int(self.src_size[0] * scales), int(self.src_size[1] * scales)), 'white')
        # self.draw = ImageDraw.Draw(target_img)

        # todo
        cells_structure = ''.join(self.cells_structure_elems)
        cells_content = self.cells_content

        thead = list(re.finditer(r'(<thead>).*(</thead>)', cells_structure))
        tbody = list(re.finditer(r'(<tbody>).*(</tbody>)', cells_structure))
        cell_nodes = list(re.finditer(r'(<td[^<>]*>)(</td>)', cells_structure))
        cell_rows = list(re.finditer(r'<tr>([\s\S]*?)</tr>', cells_structure))

        thead_strs = ''.join(l.group() for l in thead)
        thead_cells = list(re.finditer(r'(<td[^<>]*>)(</td>)', thead_strs))
        thead_rows = list(re.finditer(r'<tr>([\s\S]*?)</tr>', thead_strs))

        tbody_strs = ''.join(ll.group() for ll in tbody)
        tbody_cells = list(re.finditer(r'(<td[^<>]*>)(</td>)', tbody_strs))
        tbody_rows = list(re.finditer(r'<tr>([\s\S]*?)</tr>', tbody_strs))
        # print(self.img_name, end=':')
        # print(len(cell_nodes), '=', len(thead_cells), '+', len(tbody_cells), end=',')
        # print(len(cell_rows), '=', len(thead_rows), '+', len(tbody_rows))

        # 计算一共有多少列
        n_cols_list = []
        for tr in tbody_rows:
            cells = list(re.finditer(r'(<td[^<>]*>)(</td>)', tr.group(1)))
            t = 0
            for cell in cells:
                is_colspan = re.findall(r'(colspan)="(\d)"', cell.group())
                if len(is_colspan) > 0:
                    t += int(is_colspan[0][1])
                else:
                    t += 1
            n_cols_list.append(t)
            n_cols_list.append(len(cells))
        n_cols_list2 = []
        for tr in thead_rows:
            # todo 由于有的标签有问题，所以这里也有问题，少算了跨行的
            cells = list(re.finditer(r'(<td[^<>]*>)(</td>)', tr.group(1)))
            t = 0
            for cell in cells:
                is_colspan = re.findall(r'(colspan)="(\d)"', cell.group())
                if len(is_colspan) > 0:
                    t += int(is_colspan[0][1])
                else:
                    t += 1
            n_cols_list2.append(t)
            n_cols_list2.append(len(cells))
        n_cols = max(n_cols_list + n_cols_list2)
        assert len(cell_rows) == len(thead_rows) + len(tbody_rows), 'the total num of rows not equally thead add tbody'
        n_rows = len(cell_rows)
        self.rows = n_rows
        self.cols = n_cols

        x, y = 2, 2
        cnt = 0
        # 一个有多少个单元格
        flag = []
        cells_record = []
        for i in range(n_rows):
            tmp_flag = []
            for j in range(n_cols):
                # cnt = 1
                tmp_flag.append(cnt)
            flag.append(tmp_flag)

        # assert len(cells_content) == n_rows*n_cols
        td_list = []
        count = 0
        a = 1
        flag2 = np.zeros((n_rows, n_cols), dtype=np.int16)
        row_span_record = []
        col_span_record = []
        for i, tr in enumerate(cell_rows):
            tmp_cells = re.findall(r'<td[^<>]*></td>', tr.group(1))
            td_list.append(tmp_cells)
            assert len(tmp_cells) != 0, 'the num of cell is 0'
            for k, tmp_cell in enumerate(tmp_cells):
                is_rowspan = re.findall(r'(rowspan=)"(\d)"', tmp_cell)
                is_colspan = re.findall(r'(colspan)="(\d)"', tmp_cell)

                loc = '%d,%d' % (i, k)
                cells_record.append({loc: (is_rowspan, is_colspan)})
                if len(is_rowspan) > 0 and len(is_colspan) == 0:
                    # row_i=2
                    row_i = int(is_rowspan[0][1])
                    flag[i][k] = [[1]] * row_i
                    index = np.where(flag2[i] == 0)[0][0]
                    for ii in range(row_i):
                        # if flag2[i + ii, index] == 0:
                        flag2[i + ii, index] = a
                    a += 1
                    # 记下当前单元格合并了几行
                    loc = '%d,%d' % (i, k)
                    row_span_record.append({loc: row_i})
                    count += 1
                elif len(is_rowspan) == 0 and len(is_colspan) > 0:
                    # row_i=2
                    # 记录有几个单元格合并
                    col_k = int(is_colspan[0][1])
                    flag[i][k] = [1] * col_k
                    index = np.where(flag2[i] == 0)[0][0]
                    for kk in range(col_k):
                        flag2[i, index + kk] = a
                    a += 1
                    # 记下当前单元格合并了几列
                    loc = '%d,%d' % (i, k)
                    col_span_record.append({loc: col_k})
                    count += 1
                elif len(is_colspan) > 0 and len(is_rowspan) > 0:
                    # print('line 424',self.img_name)
                    # assert 1==2
                    col_k = int(is_colspan[0][1])
                    row_i = int(is_rowspan[0][1])
                    flag[i][k] = [[1] * col_k] * row_i
                    loc = '%d,%d' % (i, k)
                    row_span_record.append({loc: row_i})
                    col_span_record.append({loc: col_k})
                    index = np.where(flag2[i] == 0)[0][0]
                    for ii in range(row_i):
                        for kk in range(col_k):
                            if flag2[i + ii, index + kk] == 0:
                                flag2[i + ii, index + kk] = a
                    a += 1
                    count += 1
                    # print(self.img_name)
                else:
                    index = np.where(flag2[i] == 0)[0][0]
                    flag2[i][index] = a
                    a += 1
                    flag[i][k] = 1
                    count += 1

        assert len(cells_content) == count, 'the num of cells not equally '

        self.structure = flag2
        self.cells_record = cells_record
        self.row_span_record = row_span_record
        self.col_span_record = col_span_record
        # print('line 389', 2)
        # 释放掉内存
        # self.cells_structure = None
        self.cells_content = None
        return flag2

    def draw_structure(self):

        if self.structure is None:
            self.structure = self.get_structure()
        structure = self.structure
        if self.target_img is None:
            self.target_img = Image.new('RGB', (int(self.src_size[0] + 5), int(self.src_size[1] + 5)), 'white')
            self.draw = ImageDraw.Draw(self.target_img)
        bg = np.array(self.target_img)
        assert self.rows is not None, 'the rows is None'
        cell_w = self.src_size[0] // self.cols
        cell_h = (self.src_size[1]) // self.rows
        x, y = 2, 2
        tmp_x, tmp_y = x, y
        cells = []
        tmp_cells = []
        for i in range(self.rows):
            row_cells = []
            for j in range(self.cols):
                tmp = structure[i, j]
                if tmp == 0:
                    tmp_x += cell_w
                    continue
                index = np.where(structure == tmp)
                if len(index[0]) == 1:
                    w, h = cell_w, cell_h
                elif len(index[0]) > 1:
                    if len(np.unique(index[1])) == 1:
                        # 说明是行合并
                        h = len(index[0]) * cell_h
                        w = cell_w
                        structure[index] = 0
                    elif len(np.unique(index[0])) == 1:
                        # 列合并
                        w = len(index[1]) * cell_w
                        h = cell_h
                        structure[index] = 0
                    elif len(np.unique(index[0])) > 1 and len(np.unique(index[1])) > 1:
                        # 既有行合并又有列合并
                        w = len(np.unique(index[1])) * cell_w
                        h = len(np.unique(index[0])) * cell_h
                        structure[index] = 0
                tmp_x2, tmp_y2 = tmp_x + w, tmp_y + h
                bbox = [tmp_x, tmp_y, tmp_x2, tmp_y2]
                cv2.rectangle(bg, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 0, 0), 0)
                tmp_cell = {'tokens': [' '], 'bbox': bbox}
                row_cells.append(bbox)
                cells.append(tmp_cell)
                tmp_x += cell_w

            tmp_cells.append(row_cells)
            tmp_y += cell_h
            tmp_x = x
        # self.html['cells'] = cells
        self.cells_content = cells
        target_img = Image.fromarray(bg)
        self.target_img = target_img
        # print(2)
        return target_img


def cal_IOU(bbox1, bboxes):
    iou_list = {}
    bbox1 = [float(x) for x in bbox1]
    (x0_1, y0_1, x1_1, y1_1) = bbox1
    for i, bbox2 in enumerate(bboxes):
        if len(bbox2) == 0:
            continue
        bbox2 = [float(x) for x in bbox2]
        (x0_2, y0_2, x1_2, y1_2) = bbox2
        # get the overlap rectangle
        overlap_x0 = max(x0_1, x0_2)
        overlap_y0 = max(y0_1, y0_2)
        overlap_x1 = min(x1_1, x1_2)
        overlap_y1 = min(y1_1, y1_2)
        # check if there is an overlap
        if overlap_x1 - overlap_x0 <= 0 or overlap_y1 - overlap_y0 <= 0:
            # iou_list.append(0)
            continue
        # if yes, calculate the ratio of the overlap to each ROI size and the unified size
        size_1 = (x1_1 - x0_1) * (y1_1 - y0_1)
        size_2 = (x1_2 - x0_2) * (y1_2 - y0_2)
        size_intersection = (overlap_x1 - overlap_x0) * (overlap_y1 - overlap_y0)
        size_union = size_1 + size_2 - size_intersection
        iou = size_intersection / size_union
        # return size_intersection / size_union
        iou_list[i] = iou

        # return iou
    return iou_list


def get_items(jsonl_file, start=0, end=1000):
    items = []
    # count = 0
    start_line = start
    count = start
    end_line = end
    with open(jsonl_file, 'r', encoding="utf8") as fr:
        if end == 'inf':
            for line in jsonlines.Reader(fr):
                items.append(line)
        else:
            for line in jsonlines.Reader(fr):
                if start_line <= count < end_line:
                    count += 1
                    items.append(line)
                else:
                    break
    return items


if __name__ == '__main__':
    pass

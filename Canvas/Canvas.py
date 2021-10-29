#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
"""
@AUTHOR:
@FILE:Canvas.py
@NAME:Table_renderer
@TIME:2021/07/17
@IDE: PyCharm
@Ref:
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw, features
from TextString.TextString import TextString


class CanvasImage(object):
    """
    画布类
    """

    def __init__(self, size=(1280, 720), color='white'):
        """
        :param size_w:
        :param size_h:
        :param color: PIL.ImageColor.colormap
        """
        self.size_w = size[0]
        self.size_h = size[1]
        self.bg_color = color
        self.pil_img = self.create_canvas()
        self.draw = self.create_draw()

    def create_canvas(self):
        canvas = Image.new('RGB', (self.size_w, self.size_h), self.bg_color)
        self.pil_img = canvas
        # img_arr = np.array(canvas)
        # pil_img = Image.fromarray(img_arr)
        # draw = ImageDraw.Draw(canvas)
        return canvas

    def create_draw(self):
        draw = ImageDraw.Draw(self.pil_img)
        return draw

    def open(self, file_path=None):
        pil_image = Image.open(file_path)
        self.pil_img = pil_image
        return self

    @staticmethod
    def set_coordxy(text_string, xy):
        assert len(xy) == 2
        if text_string.direction == 'ltr' or text_string.direction is None:
            text_string.coord_xy = xy
        elif text_string.direction == 'rtl':
            text_string.coord_xy = (xy[0] - text_string.char_w, xy[1])
        elif text_string.direction == 'ttb':
            text_string.coord_xy = xy
        elif text_string.direction == 'btt':
            text_string.coord_xy = (xy[0], xy[1] - text_string.char_h)
        return 0

    @staticmethod
    def set_direction(text_string, direction):
        if not text_string.direction and not direction:
            text_string.direction = None
        elif not text_string.direction and direction:
            text_string.direction = direction
        elif text_string and not direction:
            text_string.direction = text_string.direction
        elif text_string and direction:
            print("The string's direction is not same")
            text_string.direction = direction

    def spilt_text_string(self, text_string):

        pass

    def draw_str(self, text_string):

        coord_xy = text_string.coord_xy
        cnt_char = 0
        cnt_enter = 0
        min_bboxes = []
        vaild_text = ''
        valid_text_bbox = []
        # todo 这里可以改成如果画布写不下就只写一部分
        if text_string.char_space <= 2:
            # if text_string.direction == 'ltr':
            lt_x = coord_xy[0]
            lt_y = coord_xy[1]
            # todo 在linux上没有libraqm,不支持文字方向
            width, height = text_string.getsize()

            if 0 < lt_x < self.size_w and 0 < lt_y < self.size_h \
                    and 0 < lt_x + width < self.size_w and 0 < lt_y + height < self.size_h:
                self.draw.text((lt_x, lt_y), text=text_string.text, fill=text_string.color, font=text_string.font,
                               )
                min_bbox = (lt_x, lt_y, lt_x + width, lt_y + height)
                vaild_text = text_string.text
                min_bboxes.append(min_bbox)
                valid_text_bbox.append((vaild_text, min_bbox))
            # elif text_string.direction=='ttb':
            # todo  没有学垂直方向的
            #     pass

            else:
                print('line 107:坐标超出画布,', text_string.text, (lt_x, lt_y, lt_x + width, lt_y + height), end='')

        elif text_string.char_space > 2:
            # 文本类，一个一个写
            if text_string.direction == 'ltr' or text_string.direction is None:
                # 从左到右
                lt_x = coord_xy[0]
                lt_y = coord_xy[1]
                # 如果整行文本写不下，只能写部分
                for i, char in enumerate(text_string.text):

                    # 判断单个字能否写在画布内
                    if lt_x <= 0 or lt_x + text_string.char_w > self.size_w or \
                            lt_y <= 0 or lt_y + text_string.char_h > self.size_h:
                        print('the char %s out of border' % char)
                        print("Warning: The text maybe out of the canvas's border")
                        # todo 这里重复加了几次，需要改进，后面返回时去重了
                        # 这里应该跳进下一行
                        min_bbox_w = cnt_char * (text_string.char_w + text_string.char_space)
                        min_bbox_h = text_string.char_h
                        min_bbox = (lt_x - min_bbox_w, lt_y, lt_x - text_string.char_space, lt_y + min_bbox_h)
                        if min_bbox in min_bboxes:
                            continue
                        else:
                            min_bboxes.append(min_bbox)
                            valid_text_bbox.append((vaild_text, min_bbox))

                    else:
                        self.draw.text((lt_x, lt_y), char, text_string.color, font=text_string.font)
                        # 记下写了几个字
                        vaild_text += char
                        cnt_char += 1
                        lt_x = lt_x + text_string.char_space + text_string.char_w
                # min_bboxes为空，说明这行文本能完全写完，那么直接调用得到
                if not min_bboxes:
                    tmp_bboxs = text_string.get_bbox()
                    for tmp in tmp_bboxs:
                        min_bboxes.append(tmp)
                        valid_text_bbox.append((vaild_text, tmp))

            elif text_string.direction == 'ttb':
                # 从上到下
                # todo 去掉不在画布的文字
                # print('VerticalTextString is top to bottom')
                lt_x = coord_xy[0]
                lt_y = coord_xy[1]
                for i, char in enumerate(text_string.text):
                    if lt_x <= 0 or lt_x + text_string.char_w > self.size_w or \
                            lt_y <= 0 or lt_y + text_string.char_h > self.size_h:
                        # print('the char %s out of border' % char,end='')
                        print("Warning: The text maybe out of the canvas's border", (lt_x, lt_y), )

                        # todo 这里重复加了几次，需要改进
                        min_bbox_h = cnt_char * (text_string.char_h + text_string.char_space)
                        min_bbox_w = text_string.char_w
                        min_bbox = (lt_x, lt_y - min_bbox_h, lt_x + min_bbox_w, lt_y - text_string.char_space)
                        if min_bbox in min_bboxes:
                            continue
                        else:
                            min_bboxes.append(min_bbox)
                            valid_text_bbox.append((vaild_text, min_bbox))
                    else:
                        self.draw.text((lt_x, lt_y), char, text_string.color, font=text_string.font)
                        vaild_text += char
                        cnt_char += 1
                        lt_y = lt_y + text_string.char_h + text_string.char_space
                # min_bboxes为空，说明这行文本能完全写完，那么直接调用得到
                if not min_bboxes:
                    # 这里得到的是多行的bboxes[(),()()]
                    tmp_bboxs = text_string.get_bbox()
                    for tmp in tmp_bboxs:
                        min_bboxes.append(tmp)
                        valid_text_bbox.append((vaild_text, tmp))

        text_string.bbox = min_bboxes
        text_string.vaild_text_bbox = valid_text_bbox
        # print('line 185:', min_bboxes)
        # print('不重复的框', tmp_bboxes)
        self.pil_img = self.pil_img
        return min_bboxes, valid_text_bbox

    def draw_text_string(self, text_string, coord_xy=None, direction=None, fp=None):
        """
        返回写上文字的PIL.Image.Image对象
        :param text_string:
        :param coord_xy:
        :param direction；
        :param fp:
        :return:
        """
        res_bboxes = []
        min_bboxes = []
        text_string.coord_xy = coord_xy
        if len(coord_xy) != 2:
            raise ValueError('coord_xy must be a 2-tuple or array')

        if not self.pil_img:
            self.create_canvas()
            # self.draw = ImageDraw.Draw(self.pil_img)
            self.create_draw()
        text_string_list = text_string.split_string()

        # 如果是文本类，一行一行切开
        for sub_str in text_string_list:
            sub_text_string = TextString(text_string=sub_str, font=text_string.font_file, color=text_string.color,
                                         char_size=text_string.char_w, direction=text_string.direction,
                                         line_space=text_string.line_space, char_space=text_string.char_space)
            # 设置文本书写方向
            assert len(coord_xy) == 2
            # text_string.direction = direction
            self.set_direction(sub_text_string, direction)
            # 设置文本的对齐坐标--左上角（ltr,ttb)右上角（rtl)左下角(btt)
            # text_string.coord_xy = coord_xy
            self.set_coordxy(sub_text_string, coord_xy)

            # text_string.coord_xy = coord_xy
            coord_xy = sub_text_string.coord_xy

            min_bbox, valid_text_bbox = self.draw_str(sub_text_string)

            res_bboxes += valid_text_bbox
            min_bboxes += min_bbox
            # 写下行
            if text_string.direction == 'ltr' or text_string.direction is None:
                coord_xy = (coord_xy[0], coord_xy[1] + sub_text_string.char_h + text_string.line_space)
            elif text_string.direction == 'ttb':
                coord_xy = (coord_xy[0] + sub_text_string.char_w + text_string.line_space, coord_xy[1])

        text_string.bbox = min_bboxes
        text_string.vaild_text_bbox = res_bboxes
        # print('line 238:', text_string.bbox)
        return res_bboxes

    # @staticmethod
    def get_bbox(self, text_string, fp=None):

        # 这里其实可以调用TextString.get_bbox
        # todo 不一样,要重写,应该调用Canvas.draw_text_string
        # 如果之前没有调用Canvas.draw_text_string,则需要设置默认坐标
        if not text_string.coord_xy:
            self.set_coordxy(text_string, (1, 1))
        coord_xy = text_string.coord_xy
        # if coord_xy[0] < 0 or coord_xy[0] > self.size_w or coord_xy[1] < 0 or coord_xy[1] > self.size_h:
        #     return []
        assert len(coord_xy) == 2
        bboxes = []
        valid_text_bbox = []
        if 'ltr' == text_string.direction or text_string.direction is None:
            if text_string.char_space < 1.5 * text_string.char_w:
                if not text_string.bbox:
                    # 没有调用draw_text_string,
                    # todo 如果没有先写字，就想画文本框,如何处理
                    # print('line 262 : Maybe first call Canvas.draw_text_string', coord_xy, end='')
                    # bboxes = text_string.get_bbox()
                    pass
                else:
                    bboxes = text_string.bbox
                    valid_text_bbox = text_string.vaild_text_bbox

            elif text_string.char_space >= 1.5 * text_string.char_w:
                lt_x = text_string.coord_xy[0]
                lt_y = text_string.coord_xy[1]
                for i, char in enumerate(text_string.text):

                    if char != '\n':
                        # 判断单个字能否写在画布内
                        if lt_x <= 0 or lt_x + text_string.char_w > self.size_w or \
                                lt_y <= 0 or lt_y + text_string.char_h > self.size_h:
                            print('the char %s out of border' % char)
                            print("Warning: The text maybe out of the canvas's border")
                            continue
                        else:
                            # self.draw.text((lt_x, lt_y), char, text_string.color, font=text_string.font)
                            bbox = (lt_x, lt_y, lt_x + text_string.char_w, lt_y + text_string.char_h)
                            bboxes.append(bbox)
                            valid_text_bbox.append((char, bbox))
                            lt_x = lt_x + text_string.char_space + text_string.char_w

                    elif char == '\n':
                        lt_y = lt_y + text_string.char_h + text_string.line_space
                        lt_x = coord_xy[0]

        elif text_string.direction == 'ttb':
            # todo 有问题
            if text_string.char_space < 1.5 * text_string.char_w:
                if not text_string.bbox:
                    # todo 如果没有先写字，就想画文本框,如何处理
                    print('line 262 : Maybe first call Canvas.draw_text_string')
                else:
                    bboxes = text_string.bbox
                    valid_text_bbox = text_string.vaild_text_bbox

            elif text_string.char_space >= 1.5 * text_string.char_w:
                lt_x = text_string.coord_xy[0]
                lt_y = text_string.coord_xy[1]
                for i, char in enumerate(text_string.text):

                    if char != '\n':
                        if lt_x <= 0 or lt_x + text_string.char_w > self.size_w or \
                                lt_y <= 0 or lt_y + text_string.char_h > self.size_h:
                            print('the char %s out of border' % char)
                            print("Warning: The text maybe out of the canvas's border")
                            continue
                        else:
                            bbox = (lt_x, lt_y, lt_x + text_string.char_w, lt_y + text_string.char_h)
                            bboxes.append(bbox)
                            valid_text_bbox.append((char, bbox))
                            lt_y = lt_y + text_string.char_h + text_string.char_space
                    elif char == '\n':
                        lt_x = lt_x + text_string.char_w + text_string.line_space
                        lt_y = coord_xy[1]

        # 更新写在画布内的有效字体
        text_string.bbox = bboxes
        text_string.vaild_text_bbox = valid_text_bbox

        return bboxes, valid_text_bbox

    def draw_bbox(self, text_string, offset=0, width=1, color='black', **kwargs):
        """
        画出单行最小文本框
        :param offset:
        :param color:
        :param text_string:
        :param width:
        :return:
        """
        res_bboxes = []
        bboxes, valid_text_bbox = self.get_bbox(text_string, **kwargs)
        if len(bboxes) == 0:
            # 如果起始点坐标就没有在画布内，就会有空bbox,或者起始点(左上角）不够写
            # print('line 342:', text_string.text)
            print('line 345: No bounding box')

        elif len(bboxes):
            for bbox in bboxes:
                # print('line 349', bbox)
                bbox = (bbox[0] - offset, bbox[1] - offset, bbox[2] + offset, bbox[3] + offset)
                self.draw.rectangle(bbox, fill=None, outline=color, width=width)
                res_bboxes.append(bbox)
        self.pil_img = self.pil_img
        return res_bboxes, valid_text_bbox

    def draw_line(self, xy, color, width=1, kind=None):
        if not self.pil_img:
            self.create_canvas()
            self.create_draw()

        self.draw.line(xy, fill=color, width=width)

        # plt.plot(x, y, color='r', marker='o', linestyle='dashed')

    def draw_multilines(self, xy, color, multi=2, offset=2, width=1, kind=None):
        """
        画多线
        :param xy:[(x,y),(x,y)],(x,y,x,y)
        :param color:
        :param multi:
        :param offset:
        :param width:
        :return:
        """
        x_1, y_1, x_2, y_2 = 0, 0, 0, 0
        assert multi >= 1
        if len(xy) == 2:
            x_1, y_1 = xy[0][0], xy[0][1]
            x_2, y_2 = xy[1][0], xy[1][0]
        elif len(xy) == 4:
            x_1, y_1, x_2, y_2 = xy[0], xy[1], xy[2], xy[3]

        for i in range(multi):
            x1, y1, x2, y2 = x_1, y_1, x_2, y_2
            self.draw_line((x1, y1, x2, y2), color, width=width)
            # self.draw.line((x1, y1, x2, y2), fill=color, width=width)
            y_1, y_2 = y_1 + offset, y_2 + offset

    def draw_dash(self):
        """
        # todo 画虚线，先画直线，在crop出来，旋转，在原图上将画了直线的地方进行恢复，最后paste进去，
        :return:
        """
        pass

    def draw_rectangle(self, bbox, fill=None, outline=None, width=1):
        if not self.pil_img:
            self.create_canvas()
            self.create_draw()

        self.draw.rectangle(bbox, fill=fill, outline=outline, width=width)

    def crop(self, bbox, fp=None):
        assert len(bbox) == 4

        res_pil_img = self.pil_img.crop(bbox)
        if fp:
            res_pil_img.save(fp)
        return res_pil_img

    def paste_img(self, pil_image, xy=(0, 0)):

        if isinstance(pil_image, Image.Image):
            self.pil_img.paste(pil_image, box=xy)

        elif len(pil_image) == 2:
            img, size = pil_image
            rb = (xy[0] + size[0], xy[1] + size[1])

        # print('line 448:saved ./result.jpg')
        # self.pil_img.save('./result.jpg')

        # return self

    def save(self, file_path=None):
        self.pil_img.save(file_path)


if __name__ == '__main__':
    print(0)

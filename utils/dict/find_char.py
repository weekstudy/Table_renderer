#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
"""
@AUTHOR:
@FILE:find_char.py
@NAME:Table_renderer
@TIME:2021/07/20
@IDE: PyCharm
@Ref:
"""


def find():
    char_dict1 = './cht_std_dict.txt'
    char_dict2 = './cht_std_fanti_dict.txt'
    char1 = []
    i = 0
    with open(char_dict1, 'r') as fr:
        lines = fr.readlines()

    for line in lines:
        cont = line.strip().split(' ')
        # print(cont)
        char1.append(cont)
    char2 = []
    i = 0
    with open(char_dict2, 'r') as fr:
        lines = fr.readlines()
    for line in lines:
        cont = line.strip().split(' ')

        # print(cont)
        char2.append(cont)
    # print(char1)
    # print(char2)
    for i in range(len(char1)):
        # print(len(char2[i]))
        # print()
        if len(char2[i]) != len(char1[i]):
            print(char1[i])
            print(char2[i])


if __name__ == '__main__':
    find()

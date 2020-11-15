#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2020 WShuai, Inc.
# All Rights Reserved.

# @File: jinzhi.py
# @Author: WShuai, WShuai, Inc.
# @Time: 2020/11/14 16:27

class Jinzhi(object):
    def __init__(self):
        return

    def str2bin(self, str):
        return ''.join(['{:08d}'.format(int(bin(ord(char)).replace('0b', ''))) for char in str])

    def bin2str(self, bin):
        if bin[:2] == '0b' or bin[:2] == '0B':
            bin = bin[2:]
        if len(bin) % 8 != 0:
            bin = '0' * (8 - len(bin) % 8) + bin
        return ''.join([chr(int(bin[index * 8 : (index + 1) * 8], 2)) for index in range(len(bin) // 8)])

    def str2hex(self, str):
        return ''.join(['{:02x}'.format(ord(char)) for char in str])

    def hex2str(self, hex):
        if hex[:2] == '0x' or hex[:2] == '0X':
            hex = hex[2:]
        if len(hex) % 2 != 0:
            hex = '0' * (2 - len(hex) % 2) + hex
        return ''.join([chr(int(hex[index * 2 : (index + 1) * 2], 16)) for index in range(len(hex) // 2)])

    def hex2bin(self, hex):
        if hex[:2] == '0x' or hex[:2] == '0X':
            hex = hex[2:]
        if len(hex) % 2 != 0:
            hex = '0' * (2 - len(hex) % 2) + hex
        return ''.join(['{:04d}'.format(int(bin(int(char, 16)).replace('0b', ''))) for char in hex])

    def bin2hex(self, bin):
        if bin[:2] == '0b' or bin[:2] == '0B':
            bin = bin[2:]
        return ''.join([hex(int(bin[index * 4 : (index + 1) * 4], 2)).replace('0x', '') for index in range(len(bin) // 4)])

import sys
if __name__ == '__main__':
    base = Jinzhi()

    result = base.str2hex('wshuai')
    result = base.hex2str('777368756169')

    result = base.str2bin('wshuai')
    result = base.bin2str('0b011101110111001101101000011101010110000101101001')

    result = base.hex2bin('777368756169')
    result = base.bin2hex('0b011101110111001101101000011101010110000101101001')

    result = base.hex2bin('0123456789ABCDEF')
    result = base.bin2hex('1000010111101000000100110101010000001111000010101011010000000101')

    result = base.bin2hex('0b011101110111001101101000011101010110000101101001')
    print(result)
    sys.exit(0)

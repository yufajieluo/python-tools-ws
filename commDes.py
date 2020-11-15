#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2020 WShuai, Inc.
# All Rights Reserved.

# @File: commDes.py
# @Author: WShuai, WShuai, Inc.
# @Time: 2020/11/14 11:08

import inspect
from jinzhi import Jinzhi

class DesComm(object):
    def __init__(self, key_len):
        self.key_len = key_len
        self.jinzhi = Jinzhi()
        self.shift_bit = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
        self.bitmap_key_init = [
            57, 49, 41, 33, 25, 17, 9,
            1, 58, 50, 42, 34, 26, 18,
            10, 2, 59, 51, 43, 35, 27,
            19, 11, 3, 60, 52, 44, 36,
            63, 55, 47, 39, 31, 23, 15,
            7, 62, 54, 46, 38, 30, 22,
            14, 6, 61, 53, 45, 37, 29,
            21, 13, 5, 28, 20, 12, 4,
        ]
        self.bitmap_key_proc = [
            14, 17, 11, 24, 1, 5,
            3, 28, 15, 6, 21, 10,
            23, 19, 12, 4, 26, 8,
            16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55,
            30, 40, 51, 45, 33, 48,
            44, 49, 39, 56, 34, 53,
            46, 42, 50, 36, 29, 32,
        ]
        self.bitmap_plaintext = [
            58, 50, 42, 34, 26, 18, 10, 2,
            60, 52, 44, 36, 28, 20, 12, 4,
            62, 54, 46, 38, 30, 22, 14, 6,
            64, 56, 48, 40, 32, 24, 16, 8,
            57, 49, 41, 33, 25, 17, 9, 1,
            59, 51, 43, 35, 27, 19, 11, 3,
            61, 53, 45, 37, 29, 21, 13, 5,
            63, 55, 47, 39, 31, 23, 15, 7,
        ]
        self.bitmap_right_proc = [
            32, 1, 2, 3, 4, 5,
            4, 5, 6, 7, 8, 9,
            8, 9, 10, 11, 12, 13,
            12, 13, 14, 15, 16, 17,
            16, 17, 18, 19, 20, 21,
            20, 21, 22, 23, 24, 25,
            24, 25, 26, 27, 28, 29,
            28, 29, 30, 31, 32, 1,
        ]
        self.bitmap_zip_proc = [
            16, 7, 20, 21, 29, 12, 28, 17,
            1, 15, 23, 26, 5, 18, 31, 10,
            2, 8, 24, 14, 32, 27, 3, 9,
            19, 13, 30, 6, 22, 11, 4, 25,
        ]
        self.bitmap_final = [
            40, 8, 48, 16, 56, 24, 64, 32,
            39, 7, 47, 15, 55, 23, 63, 31,
            38, 6, 46, 14, 54, 22, 62, 30,
            37, 5, 45, 13, 53, 21, 61, 29,
            36, 4, 44, 12, 52, 20, 60, 28,
            35, 3, 43, 11, 51, 19, 59, 27,
            34, 2, 42, 10, 50, 18, 58, 26,
            33, 1, 41, 9, 49, 17, 57, 25,
        ]
        self.bitmap_zip = [
            [
                [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
                [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
                [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
                [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
            ],
            [
                [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
                [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
                [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
                [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
            ],
            [
                [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
                [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
                [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
                [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
            ],
            [
                [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
                [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
                [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
                [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
            ],
            [
                [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
                [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
                [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
                [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
            ],
            [
                [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
                [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
                [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
                [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
            ],
            [
                [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
                [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
                [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
                [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
            ],
            [
                [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
                [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
                [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
                [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
            ],
        ]
        return

    def bitmap(self, source, bitmap):
        return ''.join([source[index - 1] for index in bitmap])

    def PKCS5Padding(self, source):
        num = 8 - len(source) % 8
        result = '{}{}'.format(source, chr(num) * num)
        return result

    def complement_key(self, key):
        if len(key) >= self.key_len:
            result = key[:self.key_len]
        else:
            result = '{}{}'.format(key, chr(self.key_len - len(key)) * (self.key_len - len(key)))
        return result

    def PKCS5UnPadding(self, source):
        return source[: 0 - ord(source[-1])]

    def xor(self, source1, source2):
        result = '{0:0{1}d}'.format(
            int(bin(int('0b{}'.format(source1), 2) ^ int('0b{}'.format(source2), 2)).replace('0b', '')),
            len(source1)
        )
        return result

    def get_index_key(self, init_key_bin, index):
        init_key_left = init_key_bin[ : len(init_key_bin) // 2]
        init_key_right = init_key_bin[len(init_key_bin) // 2 : ]

        bits = sum(self.shift_bit[ : index + 1])

        current_key_left = init_key_left[bits:] + init_key_left[:bits]
        current_key_right = init_key_right[bits:] + init_key_right[:bits]
        current_key = self.bitmap(current_key_left + current_key_right, self.bitmap_key_proc)
        return current_key

    def transposer(self, plaintext_right, index_key):
        plaintext_right_bitmap = self.bitmap(plaintext_right, self.bitmap_right_proc)

        plaintext_right_xor = self.xor(plaintext_right_bitmap, index_key)

        plaintext_right_zip = ''
        for index in range(len(plaintext_right_xor) // 6):
            #print(plaintext_right_xor[index * 6: (index + 1) * 6])
            row = int('0b{}{}'.format(plaintext_right_xor[index * 6: (index + 1) * 6][0], plaintext_right_xor[index * 6: (index + 1) * 6][-1]), 2)
            col = int('0b{}'.format(int(plaintext_right_xor[index * 6: (index + 1) * 6][1:-1])), 2)
            plaintext_right_zip += '{:04d}'.format(int(bin(self.bitmap_zip[index][row][col]).replace('0b', '')))

        plaintext_right_pro = self.bitmap(plaintext_right_zip, self.bitmap_zip_proc)
        return plaintext_right_pro

    def iterator(self, source_hex, key_init_bin, type):
        result = ''
        for group in range(len(source_hex) // 16):
            source_group = source_hex[group * 16 : (group + 1) * 16]
            source_bin = self.jinzhi.hex2bin(source_group)
            source_init = self.bitmap(source_bin, self.bitmap_plaintext)
            current_source_left = source_init[ : len(source_init) // 2]
            current_source_right = source_init[len(source_init) // 2 : ]

            for index in range(16):
                if type == 'encrypt':
                    index_key = self.get_index_key(key_init_bin, index)
                else:
                    index_key = self.get_index_key(key_init_bin, 16 - index - 1)
                #print('index {} key is {}'.format(index, index_key))
                ciphetext_left = current_source_right
                ciphetext_right = self.xor(current_source_left, self.transposer(current_source_right, index_key))

                current_source_left = ciphetext_left
                current_source_right = ciphetext_right

            group_plaintext = '{}{}'.format(current_source_right, current_source_left)
            group_target_bin = self.bitmap(group_plaintext, self.bitmap_final)
            group_target_hex = self.jinzhi.bin2hex(group_target_bin)
            result += group_target_hex
        return result

    def encrypt(self, plaintext_hex, key):
        key_cop = self.complement_key(key)
        key_bin = self.jinzhi.str2bin(key_cop)
        key_init_bin = self.bitmap(key_bin, self.bitmap_key_init)

        ciphetext = self.iterator(plaintext_hex, key_init_bin, inspect.stack()[0][3])
        return ciphetext

    def decrypt(self, ciphetext, key):
        key_cop = self.complement_key(key)
        key_bin = self.jinzhi.str2bin(key_cop)
        key_init_bin = self.bitmap(key_bin, self.bitmap_key_init)

        plaintext_hex = self.iterator(ciphetext, key_init_bin, inspect.stack()[0][3])
        return plaintext_hex

class Des(DesComm):
    '''
    目前只支持 ECB 模式，填充方式为 pkcs5padding
    '''
    def __init__(self):
        super(eval(self.__class__.__name__), self).__init__(8)
        return

    def encrypt(self, plaintext, key):
        plaintext_cop = self.PKCS5Padding(plaintext)
        plaintext_hex = self.jinzhi.str2hex(plaintext_cop)
        ciphetext = super(eval(self.__class__.__name__), self).encrypt(plaintext_hex, key)
        return ciphetext

    def decrypt(self, ciphetext, key):
        plaintext_hex = super(eval(self.__class__.__name__), self).decrypt(ciphetext, key)
        plaintext_str = self.jinzhi.hex2str(plaintext_hex)
        plaintext = self.PKCS5UnPadding(plaintext_str)
        return plaintext

class Des3(DesComm):
    def __init__(self):
        super(eval(self.__class__.__name__), self).__init__(8 * 3)
        return

    def encrypt(self, plaintext, key):
        key_cop = self.complement_key(key)

        plaintext_cop = self.PKCS5Padding(plaintext)
        plaintext_hex = self.jinzhi.str2hex(plaintext_cop)

        tmp_ciphetext = super(eval(self.__class__.__name__), self).encrypt(plaintext_hex, key_cop[:8])
        tmp_plaintext_hex = super(eval(self.__class__.__name__), self).decrypt(tmp_ciphetext, key_cop[8:16])
        ciphetext = super(eval(self.__class__.__name__), self).encrypt(tmp_plaintext_hex, key_cop[16:])

        return ciphetext

    def decrypt(self, ciphetext, key):
        key_cop = self.complement_key(key)

        tmp_plaintext_hex = super(eval(self.__class__.__name__), self).decrypt(ciphetext, key_cop[16:])
        tmp_ciphetext = super(eval(self.__class__.__name__), self).encrypt(tmp_plaintext_hex, key_cop[8:16])
        plaintext_hex = super(eval(self.__class__.__name__), self).decrypt(tmp_ciphetext, key_cop[:8])

        plaintext_str = self.jinzhi.hex2str(plaintext_hex)
        plaintext = self.PKCS5UnPadding(plaintext_str)
        return plaintext

import sys
if __name__ == '__main__':
    plaintext = 'wshuaigj'
    key = '12345678'

    des = Des()
    ciphetext = des.encrypt(plaintext, key)
    print('Des ciphetext is [{}]'.format(ciphetext))

    plaintext = des.decrypt(ciphetext, key)
    print('Des plaintext1 is [{}]'.format(plaintext))

    print('==========')

    plaintext_des3 = 'wshuaigj'
    key_des3 = '123456781111111122222222'

    des3 = Des3()
    ciphetext_des3 = des3.encrypt(plaintext_des3, key_des3)
    print('3Des ciphetext is {}'.format(ciphetext_des3))

    plaintext_des3 = des3.decrypt(ciphetext_des3, key_des3)
    print('3Des plaintext is {}'.format(plaintext_des3))
    sys.exit(0)

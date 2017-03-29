#!/usr/bin/python
# -*- coding:utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2016 WShuai, Inc.
# All Rights Reserved.

# @author: WShuai, WShuai, Inc.

import base64
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

'''
Personal Encrypt
pip install pycrypto
'''
class CryptHandler(object):
    def __init__(self):
        self.key = "asdfghjkl;'shuai" # must by 16 length
        self.mode = AES.MODE_CBC

    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        length = 16
        count = len(text)
        add = length - (count % length)
        text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        return base64.b64encode(b2a_hex(self.ciphertext))

    def decrypt(self, text):
        try:
            cryptor = AES.new(self.key, self.mode, self.key)
            plain_text = cryptor.decrypt(a2b_hex(base64.b64decode(text)))
            return plain_text.rstrip('\0')
        except:
            return '213'

import sys
import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", help="type",type=str, choices=['encode', 'decode'], required=True)
    parser.add_argument("--text", help="text",type=str, required=True)
    args = parser.parse_args()

    encrypt = Crypt()
    if args.type == 'encode':
        print encrypt.encrypt(args.text)
    elif args.type == 'decode':
        print encrypt.decrypt(args.text)
    sys.exit(0)

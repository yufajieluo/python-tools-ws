#!/usr/bin/python
# -*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2017 Sengled, Inc.
# All Rights Reserved.

# @author: WShuai, Sengled, Inc.

import os
import xml.dom.minidom

'''
XML Handler
'''

class XMLHandler(object):
    '''
    file_name - str: XML文件名
    '''
    def __init__(self, type, string_buffer = None, file_name = None):
        self.type = type
        self.string_buffer = string_buffer
        self.file_name = file_name
        self.dom = None
        self.root = None
        return

    def load_xml(self):
        if self.type == 'file':
            try:
                self.dom = xml.dom.minidom.parse(self.file_name)
                self.root = self.dom.documentElement
            except Exception as e:
                print 'load xml file [{0}] except: [{1}]'.format(self.file_name, e)
        else:
            try:
                self.dom = xml.dom.minidom.parseString(self.string_buffer)
                self.root = self.dom.documentElement
            except Exception as e:
                print 'load xml buffer except: [{0}]'.format(e)
        return

    def get_node_value(self, node_path):
        '''
        node_path - str: XML节点全路径, 如: /project/builders/hudson.tasks.Shell/command
        '''
        paths = node_path.split('/')[1:]
        current_node = self.root
        value = None
        try:
            for path in paths:
                if path == self.root.nodeName:
                    continue
                current_node = current_node.getElementsByTagName(path)[0]
            value = current_node.childNodes[0].nodeValue
        except Exception as e:
            print 'get template node [{0}] value except: [{1}]'.format(node_path, e)
        return value

    def set_node_value(self, node_path, node_value):
        '''
        node_path - str: XML节点全路径, 如: /project/builders/hudson.tasks.Shell/command
        node_value - str: XML节点的值
        '''
        paths = node_path.split('/')[1:]
        parent_node = None
        current_node = self.root
        try:
            for path in paths:
                if path == self.root.nodeName:
                    continue
                parent_node = current_node
                current_node = current_node.getElementsByTagName(path)[0]
            if node_value:
                current_node.childNodes[0].nodeValue = node_value
            else:
                parent_node.removeChild(current_node)
                parent_node.appendChild(self.dom.createElement(os.path.basename(node_path)))
        except Exception as e:
            print 'set template node [{0}] value except: [{1}]'.format(node_path, e)
        return

    def save_file(self, save_file):
        with open(save_file, 'w') as file_handler:
            self.dom.writexml(file_handler, encoding='utf-8')
        return

    def save_string(self):
        return self.dom.toxml(encoding='utf-8')


import sys
if __name__ == '__main__':
    string = '<?xml version="1.0" encoding="utf-8"?><xml><ToUserName><![CDATA[gh_6b3a97017b9c]]></ToUserName><FromUserName><![CDATA[oEGzbv1b60ofn4UrB4Ziac_pCmPQ]]></FromUserName><CreateTime>1492081678</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[三十四]]></Content><MsgId>6408442010415810800</MsgId></xml>'
    xml_handler = XMLHandler('string', string)
    xml_handler.load_xml()
    req_msg = xml_handler.get_node_value('/xml/Content')
    print isinstance(req_msg, str)
    print isinstance(req_msg, unicode)
    print req_msg.encode('utf-8')
    rsp_msg = '{0}, biubiubiu'.format(req_msg.encode('utf-8'))
    print rsp_msg
    print isinstance(rsp_msg, str)
    print isinstance(rsp_msg, unicode)
    print rsp_msg.decode('utf-8')
    xml_handler.set_node_value('/xml/Content', rsp_msg.decode('utf-8'))
    print xml_handler.save_string()
    sys.exit(0)

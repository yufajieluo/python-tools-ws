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
    def __init__(self, file_name):
        self.file_name = file_name
        self.dom = None
        self.root = None
        return

    def load_xml(self):
        try:
            self.dom = xml.dom.minidom.parse(self.file_name)
            self.root = self.dom.documentElement
        except Exception as e:
            print 'load xml file [{0}] except: [{1}]'.format(self.file_name, e)
        return

    def get_node_value(self, node_path):
        '''
        node_path - str: XML节点全路径, 如: /project/builders/hudson.tasks.Shell/command
        '''
        paths = node_path.split('/')[1:]
        current_node = self.root
        try:
            for path in paths:
                if path == self.root.nodeName:
                    continue
                current_node = current_node.getElementsByTagName(path)[0]
            value = current_node.childNodes[0].nodeValue
            print 'get template node [{0}] value is [{1}]'.format(node_path, value)
        except Exception as e:
            print 'get template node [{0}] value except: [{1}]'.format(node_path, e)
        return

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
            print 'set template node [{0}] value is [{1}]'.format(node_path, node_value)
        except Exception as e:
            print 'set template node [{0}] value except: [{1}]'.format(node_path, e)
        return

    def save_xml(self, save_file):
        with open(save_file, 'w') as file_handler:
            self.dom.writexml(file_handler, encoding='utf-8')
        return

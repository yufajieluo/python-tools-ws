#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2017 Sengled, Inc.
# All Rights Reserved.

# @author: WShuai, Sengled, Inc.

import ConfigParser

class  ConfigHandler(object):
    def __init__(self, config_file):
        self.config_file = config_file
        self.configger = ConfigParser.ConfigParser()
        self.defaults = []
        self.sections = []
        self.configs = {}
        return
 
    def get_sections(self):
        try:
            self.configger.read(self.config_file)
            self.defaults = self.configger.defaults()
            self.sections = self.configger.sections()
        except Exception as e:
            print('get sections failed: [$1]'.format(e))
        return
    
    def get_configs(self):
        self.get_sections()
        for section in self.sections:
            section_items = dict(self.configger.items(section))
            if self.defaults:
                for default_key in dict(self.defaults):
                    if section_items[default_key] == self.defaults[default_key]:
                        del section_items[default_key]
            self.configs[section] = section_items
        self.configs['DEFAULT'] = dict(self.defaults)
        return self.configs

import sys
if __name__ == '__main__':
    config_file = './sengled.conf'
    config_handler = ConfigHandler(config_file)
    print config_handler.get_configs()
    sys.exit(0)

#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2015 Sengled, Inc.
# All Rights Reserved.

# @author: WShuai, Sengled, Inc.

'''
获取配置文件中的配置项，可以兼容两个配置文件的情况，因为一般情况下，每台机器有一个配置文件，服务本身还有自己的配置文件
'''

import ConfigParser

comm_config_format = {
    'DEFAULT':{
        'PRIVATE_IPV4': {
            'format': 'string',
            'default':''
        },
    }
}

self_config_format = {
    'default':{
        'listen_port':{
           'format':'int',
           'default':0
        },
    }
}

class OverrideConfigParser(ConfigParser.ConfigParser):
    def __init__(self):
        ConfigParser.ConfigParser.__init__(self)
        return
    def optionxform(self, optionstr):
        return optionstr

class CommonCfg(object):
    def __init__(self, config_file, config_format):
        self.config_file = config_file
        self.config_format = config_format
        self.configger = OverrideConfigParser()
        self.configger.read(self.config_file)
        return

    def optionxform(self, optionstr):
        return optionstr

    def get_config(self):
        dict_config = {}
        for section in self.config_format.keys():
            dict_section = {}
            for option in self.config_format[section].keys():
                try:
                    value = self.configger.get(section, option)
                except:
                    value = ''
                if self.config_format[section][option]['format'] == 'string':
                    dict_section[option] = value
                elif self.config_format[section][option]['format'] == 'int':
                    try:
                        dict_section[option] = int(value)
                    except:
                        dict_section[option] = 0
                elif self.config_format[section][option]['format'] == 'boolean':
                    if  value.upper() == 'FALSE' or value == '0':
                        dict_section[option] = False
                    elif value.upper() == 'TRUE':
                        dict_section[option] = True
                    else:
                        dict_section[option] = False
            dict_config[section] = dict_section
        return dict_config

def get_configger(config_file, config_format):
    common_cfg = CommonCfg(config_file, config_format)
    return common_cfg

    
'''
例子
'''
import sys
if __name__ == '__main__':
    config_file_comm = '/etc/nginx.conf'
    comm_cfg = get_configger(config_file_comm, comm_config_format)
    comm_service_config = comm_cfg.get_config()
    
    config_file_self = 'self.conf'
    self_cfg = get_configger(config_file_self, self_config_format)
    self_service_config = self_cfg.get_config()
    
    service_config = dict(self_service_config['default'].items() + comm_service_config['DEFAULT'].items())
    print service_config
    sys.exit(0)

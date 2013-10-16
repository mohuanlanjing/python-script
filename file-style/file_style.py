#coding: utf-8

"""
此脚本用来持续读取文件并且检测是否有新的切割文件，若有，则读取新切割文件
author: mohuanlanhjing
date: 20131016
"""
import os
import time
import re
from collections import namedtuple

from settings import Sleep_interval, Path

class FileStyle:

    def __init__(self):
        self.suffix = 'py'
        self.prefix = ''
        self.num = 0
        self.file_list = []
        self.Log = namedtuple('Log', ['time', 'host', 'path', 'status', \
                        'response_time'])
        # [2013-10-16 11:27:19,704] 127.0.0.1 /analytics/new-geo-admin/ 200 0.0168969631195
        self.log_pattern = re.compile(r'''
            (?x)            # 启用verbose模式
            \[(?P<time>.*?)\]\s
            (?P<host>[\d\.+])\s
            (?P<path>.*?)\s
            (?P<status>\d+)\s
            (?P<response_time>.*?)$
        '''
        ) 

    def get_filelist(self):
        # 获取相同后缀名(前缀名)的文件列表
        file_list = []
        for filename in os.listdir(Path):
            if filename.endswith(self.suffix):
                file_list.append(filename)
        return file_list.sort()

    def check_new_file(self):
        # 检测是否有新的文件产生
        file_list = self.get_filelist()
        if len(file_list) > len(self.file_list):
            self.num = len(file_list) - len(self.file_list)
            self.file_list = file_list
            return True 
        else:
            return False

    def prepare_analytics(self):
        # first run
        
        if self.file_list:
            return

        self.file_list = self.get_filelist()
        for filename in self.file_list[:-1]:
            file_path = os.path.join(Path, filename)
            with file(file_path) as f:
                lines = f.readlines()
                for line in lines:
                    match = self.log_pattern.match(line)
                    group = self.Log(**match.groupdict())
                    # mysql.insert(group)

    def analytics(self):
        
            
                        

    def run(self):
        self.prepare_analytics()
                    
                    
                
                
            
if __name__ == "__main__":
    pass


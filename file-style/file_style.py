#coding: utf-8

"""
此脚本用来持续读取文件并且检测是否有新的切割文件，若有，则读取新切割文件
author: mohuanlanhjing
date: 20131016
"""
import os
import time
import re
import logging
from traceback import format_exc
from collections import namedtuple

from settings import Sleep_interval, Log_Path, Pos_Path, Access_Path

class FileStyle:

    def __init__(self):
        self.prefix = 'cdn'
        self.loglist_len = 0
        self.Access = namedtuple('Access', ['time', 'host', 'path', 'status', \
                        'response_time'])
        # [2013-10-16 11:27:19,704] 127.0.0.1 /analytics/new-geo-admin/ 200 0.0168969631195
        self.log_pattern = re.compile(r'''
            (?x)            # 启用verbose模式
            \[(?P<time>.*?)\]\s
            (?P<host>[\d\.]+)\s
            (?P<path>.*?)\s
            (?P<status>\d+)\s
            (?P<response_time>.*?)$
        '''
        ) 
        logging.basicConfig(filename=Log_Path, level=logging.DEBUG, format =\
                        '%(asctime)s %(message)s')

    def get_loglist_length(self):
        # 获取相同后缀名(前缀名)的文件列表长度
        file_list = []
        for filename in os.listdir(os.path.dirname(Access_Path)):
            if filename.startswith(self.prefix):
                file_list.append(filename)
        return len(file_list)

    def read_pos(self):
        # 查询上一次文件读取位置
        with file(Pos_Path) as f:
            try:
                pos = f.readlines()[0]
            except:
                logging.warning(format_exc())
            return pos

    def write_pos(self, pos):
        # 将当前文件位置写入pos文件
        with file(Pos_Path, 'w') as f:
            f.write(pos)
            
    def has_new_file(self):
        # 检测是否有新的文件产生
        loglist_len = self.get_loglist_length()
        if loglist_len > self.loglist_len:
            self.loglist_len = loglist_len
            return True 
        return False

    def is_unexcepted_down(self):
        if os.path.isfile(Pos_Path):
            return True
        self.write_pos('0')
        return False

    def prepare(self):
        self.loglist_len = self.get_loglist_length()

    def _do_when_not_line(self, pos):
        if not self.has_new_file():
            self.write_pos(pos)
            time.sleep(2)
            return 
        self.write_pos('0')
        self.analytics('0')

    def analytics(self, pos):
        f = file(Access_Path)
        f.seek(int(pos))
        while True:
            line = f.readline()
            if not line:
                self._do_when_not_line(str(f.tell()))
                continue
            try:
                match = self.log_pattern.match(line)
                group = self.Access(**match.groupdict())
                print group
            except:
                logging.warning(format_exc())
            # mysql insert group.xxx
        f.close()

    def run(self):
        self.prepare()
        pos = '0'
        if self.is_unexcepted_down():
            pos = self.read_pos()
        self.analytics(pos)
            
if __name__ == "__main__":
    style = FileStyle()
    style.run()
    


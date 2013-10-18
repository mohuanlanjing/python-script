#coding: utf-8
import re
log_pattern = re.compile(r'''
            (?x)            # 启用verbose模式
            \[(?P<time>.*?)\]\s
            (?P<host>[\d\.]+)\s
            (?P<path>.*?)\s
            (?P<status>\d+)\s
            (?P<response_time>.*?)$
        '''
        ) 

line = '[2013-10-16 11:27:19,704] 127.0.0.1 /analytics/new-geo-admin/ 200 0.0168969631195'
print log_pattern.match(line).groupdict()



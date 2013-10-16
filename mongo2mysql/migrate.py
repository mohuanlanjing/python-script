#coding: utf-8

#此脚本用来迁移离线分析的geo的mongodb数据到实时分析的mysql数据

from pymongo import MongoClient
import GeoHandler

def mongo_conn():
    port = 27017
    host = 'localhost'
    client = MongoClient(host, port)
    return client


class Mongo2MysqlHandler:
    
    def __init__(self, db_name):
        self.client = mongo_conn()
        self.db = self.client[db_name]
        self.flag = True
        if 'co' in db_name: 
            self.coll = self.db['url_geo_co_info']
        else:
            self.coll = self.db['url_geo_po_info']
            self.flag = False

    def get_mongo_datas(self):
        return self.coll.find()

    def mongo2mysql(self):
        geo = GeoHandler()
        datas = self.get_mongo_datas()
        for data in datas:
            spec = {
                'updated': data['dt'],
                'city': '-',
                'country': data['co'],
                'domain': data['dm'],
                'hit': data['req_count'],
                'uv': 0,
                'miss': 0,
                'traffic': 0,
                'isp': 'TEL',
            }
            if self.flag:
                spec['province'] = '-'
            else: 
                spec['province'] = data['po']
            geo.insert(**spec)
            
           
if __name__ == "__main__":

    port = 27017
    host = 'localhost'

    client = MongoClient(host, port)
    db_names = client.database_names()

    for db in db_names:
        if db.startswith('url_geo_analytics_province')  or \
            db.startswith('url_geo_analytics_country'):
            m2m = Mongo2MysqlHandler(db)
            m2m.mongo2mysql()
        


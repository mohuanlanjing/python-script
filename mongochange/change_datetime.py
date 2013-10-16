#coding: utf-8
from pymongo import MongoClient

port = 27017
host = 'localhost'
dbname = 'code_info_201309'
collection = 'code_info_daily'

client = MongoClient(host, port)
db = client[dbname]
coll = db[collection]
docs = coll.find({'date_time': 20130912})
doc_list = []
for doc in docs:
    del doc['_id']
    doc_list.append(doc)

for i in range(20130901, 20130930):
    for doc in doc_list:
        doc['date_time'] = i 
        coll.insert(doc)
        del doc['_id']
for i in range(20131001, 20131030):
    for doc in doc_list:
        doc['date_time'] = i 
        coll.insert(doc)
        del doc['_id']


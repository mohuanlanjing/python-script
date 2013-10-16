#coding: utf-8
from pymongo import MongoClient

port = 27017
host = 'localhost'

client = MongoClient(host, port)
dbnames = client.database_names()
for db in dbnames:
    client.drop_database(db)

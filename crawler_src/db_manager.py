from pymongo import MongoClient
import json


class DBManger:
    """
        manager the mongodb
    """
    host = None
    port = None
    client = None
    db = None

    def __init__(self, host: str, port: int, db: str):
        self.host = host
        self.port = port
        self.client = MongoClient(host=host, port=port)
        self.db = self.client[db]

    def insert(self, col_name: str, doc):
        return self.db[col_name].insert(doc)

    def remove(self):
        pass

    def find_all(self, col_name: str):
        return self.db[col_name].find()

    def find_by_condition(self, col_name: str, condition):
        return self.db[col_name].find(condition)

    def update(self, col_name, query, update, upsert=False, multi=False):
        self.db[col_name].update(query, update, upsert, multi)

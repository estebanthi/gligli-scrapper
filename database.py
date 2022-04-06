from pymongo import MongoClient
from yaml import safe_load


class Database:

    def __init__(self):
        with open('config.yml', 'r') as file:
            mongo_url = safe_load(file)['mongo_url']
        client = MongoClient(mongo_url)
        db = client.aerodb
        self.collection = db['QCMs']

    def insert_qcm(self, qcm):
        self.collection.insert_one(qcm)

    def insert_many_qcms(self, qcms):
        self.collection.insert_many(qcms)

    def clear(self):
        self.collection.delete_many({})


if __name__ == '__main__':
    db = Database()
    db.clear()
from pymongo import MongoClient
from yaml import safe_load
from selenium import webdriver
from scrapper import Scrapper

with open('config.yml', 'r') as file:
    mongo_url = safe_load(file)['mongo_url']
client = MongoClient(mongo_url)
db = client.aerodb


def get_ids(collection):
    items = list(collection.find({}, {'_id': True}))
    return [str(item['_id']) for item in items]


categories = ['6260676fc6e31f792088a962', '626067d9c6e31f792088a963']

for category in categories:
    find = {'category': category}

    total = db['QCMs'].count_documents({'category': category})
    free = total // 10

    if free < 10:
        free = total

    to_update = list(db['QCMs'].find(find, {'_id'}).limit(free))

    if to_update:
        to_update = [qcm['_id'] for qcm in to_update]

        for _id in to_update:
            db['QCMs'].update_one({"_id": _id}, {"$set": {'free': True}})

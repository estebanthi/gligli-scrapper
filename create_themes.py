from pymongo import MongoClient
from yaml import safe_load
from selenium import webdriver
from scrapper import Scrapper


with open('config.yml', 'r') as file:
    mongo_url = safe_load(file)['mongo_url']
client = MongoClient(mongo_url)
db = client.aerodb
driver = webdriver.Chrome()

scrapper = Scrapper(driver)
print(scrapper.get_themes_mappers())


"""def get_ids(collection):
    items = list(collection.find({}, {'_id': True}))
    return [str(item['_id']) for item in items]


categories = get_ids(db['Categories'])
themes = get_ids(db['Themes'])

for category in categories:
    for theme in themes:
        find = {'category': category, 'theme': theme}

        total = db['QCMs'].count_documents({'theme': theme})
        free = total // 10

        print(themes)
"""
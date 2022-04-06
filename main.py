from selenium import webdriver

from scrapper import Scrapper


driver = webdriver.Chrome()

scrapper = Scrapper(driver)
print(scrapper.get_themes_mappers())

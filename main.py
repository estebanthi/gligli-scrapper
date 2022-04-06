from selenium import webdriver

from scrapper import Scrapper



driver = webdriver.Chrome()

scrapper = Scrapper(driver)
scrapper.run()

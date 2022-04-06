import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from bs4 import BeautifulSoup


def format_text(text):
    text = text.replace('Ã©', 'é').replace('Ã¨', 'è').replace('Ã ', 'à').replace('Ã¯', 'ï').replace('Ã®', 'î') \
        .replace('Ãª', 'ê').replace('Ã§', 'ç')
    return text


driver = webdriver.Chrome()

gligli_home_url = "https://www.chezgligli.net/"
driver.get(gligli_home_url)

email_input = driver.find_element(by=By.NAME, value='compte_login')
email_input.send_keys(email)

password_input = driver.find_element(by=By.NAME, value='compte_mdp')
password_input.send_keys(password)

login_button = driver.find_element(By.XPATH,
                                   value='/html/body/table[1]/tbody/tr[2]/td[2]/form/table/tbody/tr/td/table/tbody/tr[1]/td/span/input[3]')
login_button.click()

try:
    path = '/html/body/table[2]/tbody/tr[2]/td/table/tbody/tr/td[2]/aside/ul/li[2]/ul/li[1]/a'
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, path))
    )
finally:
    pass

qcm_button = driver.find_element(By.XPATH, value='//*[@id="appleNav"]/li[1]/a')
qcm_button.click()

ppl_qcms_button = driver.find_element(By.XPATH,
                                      value='/html/body/table[2]/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[1]/form/table/tbody/tr[2]/td[3]/input')
ppl_qcms_button.click()

reglementation_theme = driver.find_element(By.XPATH,
                                           value='/html/body/table[2]/tbody/tr[2]/td/table/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[1]/td[1]/input')
aeronef_knowledge_theme = driver.find_element(By.XPATH,
                                              value='/html/body/table[2]/tbody/tr[2]/td/table/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/input')

aeronef_knowledge_theme.click()

qcms_nb_input = driver.find_element(By.NAME, value='limite1')
qcms_nb_input.send_keys('9999')

qcms_button = driver.find_element(By.XPATH,
                                  value='/html/body/table[2]/tbody/tr[2]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/form/table/tbody/tr[1]/td[2]/input')
qcms_button.click()

correction_button = driver.find_element(By.XPATH,
                                        value='/html/body/table[2]/tbody/tr[2]/td/table/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td/input')
correction_button.click()

"""
questions = driver.find_elements(By.CLASS_NAME, value='qcm_examen_question')
questions = questions[4::2]

responses = driver.find_elements(By.CLASS_NAME, value='qcm_examen_reponses')
good_responses = driver.find_elements(By.CLASS_NAME, value='qcm_examen_reponses_bonne')

Questions = []

for i in range(len(good_responses)):
    question = {}
    question['question'] = questions[i].text
    question['responses'] = [res.text for res in responses[i*3: i*3+3]]
    question['good_response'] = good_responses[i].text
    Questions.append(question)

print(Questions)
"""

page_source = driver.page_source

soup = BeautifulSoup(page_source, 'lxml')

tables = soup.find_all('table', class_='texte cadre')

elems = {}
for table in tables:
    question = table.find('td', class_='qcm_examen_question')
    link = table.find('a', class_='liens')
    linked_image = None
    if link:
        linked_image = 'https://www.chezgligli.net/' + link.find('img')['src']

    responses = table.find_all('td', class_='qcm_examen_reponses')
    good_response = table.find('td', class_='qcm_examen_reponses_bonne')

    correction = table.find('div', class_='commentaires-list commentaire_cadre2')
    correction_image = correction.find('img')
    if correction_image:
        correction_image = correction_image['src']

    elem = {}
    elem['question'] = format_text(question.get_text())
    elem['linked_image'] = linked_image
    elem['responses'] = [format_text(response.get_text()) for response in responses] + \
                        [format_text(good_response.get_text())]
    elem['good_response'] = format_text(good_response.get_text())
    elem['correction'] = format_text(correction.get_text())
    elem['correction_image'] = correction_image
    print(elem)

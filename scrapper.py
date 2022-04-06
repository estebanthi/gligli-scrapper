from yaml import safe_load
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from qcm import QCM


class Scrapper:

    def __init__(self, driver):
        self.driver = driver
        self.email, self.password = self._load_config()

    def _load_config(self):
        with open('config.yml', 'r') as config_file:
            data = safe_load(config_file)
            return data['gligli_email'], data['gligli_password']

    def run(self):
        self._login()
        self._wait_login_completed()
        self._click_on_qcm_button()
        categories = self._get_categories()
        for i in range(len(categories)):
            self._run_for_category(i)
            print(f"i : {i}")

    def _run_for_category(self, index):
        category = self._get_categories()[index]
        category.click()
        if index not in [1, 7]:
            themes = self._get_themes()
            for i in range(len(themes)):
                qcms = self._run_for_theme(index, i)
                category = self._get_categories()[index]
                category.click()
                print(f"j : {i}")

        else:
            qcms = self._run_for_non_theme(index)

        qcm_button = self.driver.find_element(By.XPATH, value='//*[@id="appleNav"]/li[1]/a')
        qcm_button.click()

    def _wait_category_available(self):
        try:
            path = '/html/body/table[2]/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[1]/form/table/tbody/tr[2]/td[2]/input'
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, path))
            )
        finally:
            pass

    def _run_for_theme(self, category_index, theme_index):
        theme = self._get_themes()[theme_index]
        theme.click()
        self._enter_qcm()
        self._correct()
        qcms = self._get_qcms(category_index, theme_index)
        qcm_button = self.driver.find_element(By.XPATH, value='//*[@id="appleNav"]/li[1]/a')
        qcm_button.click()
        return qcms

    def _run_for_non_theme(self, index):
        self._enter_qcm()
        self._correct()
        qcms = self._get_qcms(index)
        qcm_button = self.driver.find_element(By.XPATH, value='//*[@id="appleNav"]/li[1]/a')
        qcm_button.click()
        return qcms

    def _login(self):
        self.driver.get("https://www.chezgligli.net/")

        email_input = self.driver.find_element(by=By.NAME, value='compte_login')
        email_input.send_keys(self.email)

        password_input = self.driver.find_element(by=By.NAME, value='compte_mdp')
        password_input.send_keys(self.password)

        login_button = self.driver.find_element(By.XPATH,
                                           value='/html/body/table[1]/tbody/tr[2]/td[2]/form/table/tbody/tr/td/table/tbody/tr[1]/td/span/input[3]')
        login_button.click()

    def _wait_login_completed(self):
        try:
            path = '/html/body/table[2]/tbody/tr[2]/td/table/tbody/tr/td[2]/aside/ul/li[2]/ul/li[1]/a'
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, path))
            )
        finally:
            pass

    def _click_on_qcm_button(self):
        qcm_button = self.driver.find_element(By.XPATH, value='//*[@id="appleNav"]/li[1]/a')
        qcm_button.click()

    def _get_categories(self):
        categories = self.driver.find_elements(By.XPATH, value='//form[not(@name)]//table//tbody//tr//td//input')
        return categories

    def _get_themes(self):
        themes = self.driver.find_elements(By.XPATH, value='//form//table//tbody//tr//td//input')
        return themes

    def _click_on_category(self, xpath):
        category_button = self.driver.find_element(By.XPATH, value=xpath)
        category_button.click()

    def _click_on_theme(self, xpath):
        theme_button = self.driver.find_element(By.XPATH, value=xpath)
        theme_button.click()

    def _enter_qcm(self):
        qcms_nb_input = self.driver.find_element(By.NAME, value='limite1')
        qcms_nb_input.send_keys('9999')

        qcms_button = self.driver.find_element(By.XPATH,
                                          value='/html/body/table[2]/tbody/tr[2]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/form/table/tbody/tr[1]/td[2]/input')
        qcms_button.click()

    def _correct(self):
        correction_button = self.driver.find_element(By.XPATH,
                                                value='/html/body/table[2]/tbody/tr[2]/td/table/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td/input')
        correction_button.click()

    def _get_qcms(self, category, theme=None):
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        tables = soup.find_all('table', class_='texte cadre')
        qcms = []
        for table in tables:
            raw_qcm = self._get_raw_qcm(table)
            qcm = QCM(raw_qcm, category, theme)
            qcms.append(qcm)
        return qcms

    def _get_raw_qcm(self, table):
        question = self._get_question(table)
        linked_image = self._get_linked_image(table)
        responses = self._get_responses(table)
        good_response = self._get_good_response(table)
        correction = self._get_correction(table)
        correction_image = self._get_correction_image(correction)

        return {'question': question, 'linked_image': linked_image, 'responses': responses,
                'good_response': good_response, 'correction': correction, 'correction_image': correction_image}

    @staticmethod
    def _get_question(table):
        return table.find('td', class_='qcm_examen_question')

    @staticmethod
    def _get_linked_image(table):
        link = table.find('a', class_='liens')
        linked_image = None
        if link:
            linked_image = 'https://www.chezgligli.net/' + link.find('img')['src']
        return linked_image

    @staticmethod
    def _get_responses(table):
        return table.find_all('td', class_='qcm_examen_reponses')

    @staticmethod
    def _get_good_response(table):
        return table.find('td', class_='qcm_examen_reponses_bonne')

    @staticmethod
    def _get_correction(table):
        return table.find('div', class_='commentaires-list commentaire_cadre2')

    @staticmethod
    def _get_correction_image(correction):
        correction_image = correction.find('img')
        if correction_image:
            correction_image = correction_image['src']
        return correction_image

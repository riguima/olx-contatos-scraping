import re

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class Browser:
    def __init__(self, headless=True):
        options = Options()
        options.add_argument('--user-data-dir=default_user_data')
        if headless:
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
        self.driver = Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

    def get_contacts_infos(self, ad_type, state, category, page):
        if ad_type == 'Profissional':
            self.driver.get(
                f'https://www.olx.com.br/autos-e-pecas/{category}/estado-{state}?f=c&o={page}'
            )
        elif ad_type == 'Particular':
            self.driver.get(
                f'https://www.olx.com.br/autos-e-pecas/{category}/estado-{state}?f=p&o={page}'
            )
        try:
            self.find_element('.olx-text--title-large', wait=5)
            return []
        except TimeoutException:
            pass
        result = {
            'Nome': [],
            'Telefone': [],
        }
        urls = []
        for ad in self.find_elements('.sc-74d68375-2 .olx-ad-card__link-wrapper'):
            urls.append(ad.get_attribute('href'))
        for url in urls:
            self.driver.get(url)
            try:
                self.find_element(
                    'button[data-testid="button-wrapper"]', wait=5
                ).click()
                result['Telefone'].append(self.find_element('.sc-hknOHE').text)
                result['Nome'].append(self.find_element('.sc-iMWBiJ').text)
            except TimeoutException:
                continue
        return result

    def find_element(self, selector, element=None, wait=10):
        return WebDriverWait(element or self.driver, wait).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )

    def find_elements(self, selector, element=None, wait=10):
        return WebDriverWait(element or self.driver, wait).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
        )

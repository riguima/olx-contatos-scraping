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

    def get_contacts_infos(self, ad_type, state, category):
        if ad_type == 'Profissional':
            self.driver.get(
                f'https://www.olx.com.br/autos-e-pecas/{category}/estado-{state}?f=c&o=1'
            )
        elif ad_type == 'Particular':
            self.driver.get(
                f'https://www.olx.com.br/autos-e-pecas/{category}/estado-{state}?f=p&o=1'
            )
        result = {
            'Nome': [],
            'Telefone': [],
        }
        urls = self.get_all_urls()
        for url in urls:
            self.driver.get(url)
            try:
                self.find_element(
                    'button[data-testid="button-wrapper"]'
                ).click()
                result['Telefone'].append(self.find_element('.sc-hknOHE').text)
                result['Nome'].append(self.find_element('.sc-iMWBiJ').text)
            except TimeoutException:
                continue
        return result

    def get_all_urls(self):
        urls = []
        while True:
            for ad in self.find_elements('.olx-ad-card__link-wrapper'):
                urls.append(ad.get_attribute('href'))
            base_url, current_page = re.findall(
                r'(.+?)(\d+)$', self.driver.current_url, re.DOTALL
            )[0]
            self.driver.get(f'{base_url}{int(current_page) + 1}')
            if (
                base_url not in self.driver.current_url
                or self.driver.find_elements(
                    By.CSS_SELECTOR, '.olx-text--title-large'
                )
            ):
                break
        return urls

    def find_element(self, selector, element=None, wait=10):
        return WebDriverWait(element or self.driver, wait).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )

    def find_elements(self, selector, element=None, wait=10):
        return WebDriverWait(element or self.driver, wait).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
        )

import time

from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from seleniumwire import webdriver
from selenium.webdriver.common.action_chains import ActionChains


class BotClickerV1:

    def __init__(self, proxy, query, mode=True, domain=None, headless=True):
        """

        :param proxy: proxy dict
        :param query: google like query example: "agence+web+lille"
        """
        self.proxy = proxy
        self.query = query
        self.driver = self.init_webdriver(headless)
        self.mode = mode
        self.domain = domain

    def init_webdriver(self, headless):
        options = {
            'proxy': {
                'http': f'http://{self.proxy["user"]}:{self.proxy["pass"]}@{self.proxy["host"]}:{self.proxy["port"]}',
                'https': f'https://{self.proxy["user"]}:{self.proxy["pass"]}@{self.proxy["host"]}:{self.proxy["port"]}',
                'no_proxy': 'localhost,127.0.0.1'
            }
        }
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X)'
                                    ' AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e '
                                    'Safari/602.1')
        if headless:
            chrome_options.add_argument('--headless')

        chrome_options.add_experimental_option('prefs', {
            'geolocation': True
        })

        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options,
                                  seleniumwire_options=options)
        return driver

    def find_res_natural(self):
        result = self.driver.find_element(By.ID, "rso")
        for res in result.find_elements(By.CSS_SELECTOR, ".uUPGi"):
            print(res.text)
            actions = ActionChains(self.driver)
            actions.move_to_element(res).perform()
            presentation = res.find_element(By.CSS_SELECTOR, "[role=presentation]")
            if self.domain in presentation.get_attribute("href"):
                presentation.click()
                return True
            time.sleep(0.2)
        return False

    def find_res_ads(self):
        annonces = self.driver.find_elements(By.CSS_SELECTOR, "[aria-label=Annonces] .uEierd")
        if len(annonces) > 0:
            for annonce in annonces:
                actions = ActionChains(self.driver)
                actions.move_to_element(annonce).perform()
                time.sleep(0.5)
                annonce.find_element(By.CSS_SELECTOR, "[role=heading]").click()
                self.website_action()
                time.sleep(1.2)
                self.driver.back()
                time.sleep(2)

    def website_action(self):
        """

        :return:
        """
        delay_sleep = 1 if self.mode else 2
        for offset in range(0, 910, 70):
            self.driver.execute_script(f"window.scrollTo({offset}, {offset + 70})")
            time.sleep(delay_sleep)

    def execute(self):
        self.driver.get(f'https://www.google.com/search?q={self.query}')
        time.sleep(1.5)
        if self.mode:
            self.find_res_ads()
        else:
            found = self.find_res_natural()
            self.website_action()
            if not found:
                print("Website not in 1st page")
                exit()
        self.driver.close()
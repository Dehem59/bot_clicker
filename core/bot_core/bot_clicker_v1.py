import os
import random
import time

from bo.models.siteweb import SiteWeb
from bo.models.requete import Requete
from bo.models.aclicker import Aclicker

from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from seleniumwire import webdriver
from selenium.webdriver.common.action_chains import ActionChains


# GOOGLE_CHROME_BIN = os.getenv("GOOGLE_CHROME_BIN")
# CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")
RANDOM_VARIABLE = {"scroll": [37, 58, 76, 117, 221], "delay": [1.05, 1.6, 1.2, 2.11, 3.07, 3.34]}

class BotClickerV1:

    def __init__(self, proxy, query, domain=None, online=True):
        """

        :param proxy: proxy dict
        :param query: google like query example: "agence+web+lille"
        """
        self.proxy = proxy
        self.query = query
        self.domain = domain
        self.online = online
        self.driver = self.init_webdriver()


    def init_webdriver(self):

        options = {
            'proxy': {
                'http': f'http://{self.proxy["user"]}:{self.proxy["pass"]}@{self.proxy["host"]}:{self.proxy["port"]}',
                'https': f'https://{self.proxy["user"]}:{self.proxy["pass"]}@{self.proxy["host"]}:{self.proxy["port"]}',
                'no_proxy': 'localhost,127.0.0.1'
            }
        }
        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X)'
                                    ' AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e '
                                    'Safari/602.1')
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities["device"] = "iPhone 12 Pro"
        capabilities["real_mobile"] = True

        if self.online:
            chrome_options.add_argument("--headless")
            chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            driver = webdriver.Chrome(executable_path=os.getenv("CHROMEDRIVER_PATH"), chrome_options=chrome_options,
                                  seleniumwire_options=options)
        else:
            driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=capabilities,
                                  chrome_options=chrome_options, seleniumwire_options=options)
            driver.set_window_position(50, 0)
            driver.set_window_size(390, 844)
        return driver


    def find_res_natural(self):
        result = self.driver.find_element(By.ID, "rso")
        for res in result.find_elements(By.CSS_SELECTOR, ".uUPGi"):
            actions = ActionChains(self.driver)
            actions.move_to_element(res).perform()
            presentation = res.find_element(By.CSS_SELECTOR, "a[role=presentation]")
            if self.domain in presentation.get_attribute("href"):
                presentation.click()
                time.sleep(0.5)
                return True
            time.sleep(0.2)
        return False

    def website_action(self):
        """

        :return:
        """
        last_offset = 0
        for nb_scroll in range(21):
            offset = random.choice(RANDOM_VARIABLE["scroll"])
            delay = random.choice(RANDOM_VARIABLE["delay"])
            self.driver.execute_script(f"window.scrollTo({last_offset}, {last_offset + offset})")
            time.sleep(delay)
            last_offset += offset

    def database_maj(self,found,delay,pos):
        r=Requete.objects.create(libelle= self.query)
        s=SiteWeb.objects.get_or_create(url=self.driver.current_url)
        s.requetes.add(r, through_defaults={'resultat': found,'proxy': self.proxy["host"], 'timescrolling':delay, 'positition_page':pos})


    def execute(self):
        i = 0
        while i <= 50:
            self.driver.get(f'https://www.google.com/search?q={self.query}&start={i}')
            i += 10
            time.sleep(1)
            if self.find_res_natural():
                time_before = time.time()
                self.website_action()
                time_after = time.time()
                delay = time_before-time_after
                self.database_maj("Found",delay, i)
            else:
                self.database_maj("NotFound",0, i)
                print("Website not in 1st page")
                self.driver.close()

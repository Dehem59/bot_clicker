import os
import random
import time

from django.db import transaction

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
RANDOM_VARIABLE = {"scroll": [37, 58, 76, 117, 221], "delay_debug": [0.05, 0.2, 0.2, 0.11, 0.07, 0.34],
                   "delay": [0.75, 1.21, 1.77, 2.03, 2.64, 3.11]}

MAX_TRY_GOOGLE = 2


class BotClickerV1:

    def __init__(self, proxy, query, domain, user_agent, online=True):
        """
        init the bot clicker, user_agent is the description of an specific user agent
        """
        self.proxy = proxy
        self.query = query
        self.domain = domain
        self.online = online
        self.driver = self.init_webdriver(user_agent)


    def init_webdriver(self, user_agent):

        options = {
            'proxy': {
                'http': f'http://{self.proxy["user"]}:{self.proxy["pass"]}@{self.proxy["host"]}:{self.proxy["port"]}',
                'https': f'https://{self.proxy["user"]}:{self.proxy["pass"]}@{self.proxy["host"]}:{self.proxy["port"]}',
                'no_proxy': 'localhost,127.0.0.1'
            }
        }
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument(f'--user-agent={user_agent}')
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
        p = self.driver.find_elements(By.TAG_NAME, "p")
        if len(p) > 2:
            for par in p:
                loc = par.location
                delay = random.choice(RANDOM_VARIABLE["delay"])
                self.driver.execute_script(f"window.scrollTo({last_offset}, {loc['y']})")
                last_offset = loc["y"]
                time.sleep(delay)
        else:
            for nb_scroll in range(21):
                offset = random.choice(RANDOM_VARIABLE["scroll"])
                delay = random.choice(RANDOM_VARIABLE["delay_debug"])
                self.driver.execute_script(f"window.scrollTo({last_offset}, {last_offset + offset})")
                time.sleep(delay)
                last_offset += offset

    def database_maj(self,found,delay,pos):
        with transaction.atomic():
            r=Requete.objects.create(libelle= self.query)
            s,status=SiteWeb.objects.get_or_create(url=self.driver.current_url)
            s.requetes.add(r, through_defaults={'resultat': found,'proxy': self.proxy["host"], 'timescrolling':delay,
                                                'positition_page':pos})


    def accept_google_condition(self, nb_try=0):
        nb_try += 1
        if nb_try < MAX_TRY_GOOGLE:
            try:
                for i in range(10):
                    try:
                        p = self.driver.find_elements(By.ID, "jYfXMb")
                        last_offset = 0
                        for i in p:
                            loc = i.location
                            self.driver.execute_script(f"window.scrollTo({last_offset}, {loc['y']})")
                            last_offset = loc["y"]
                        # read more to make accept button visible
                        read_more = self.driver.find_element(By.ID, "KByQx")
                        read_more.click()
                        time.sleep(0.1)
                    except:
                        pass
                time.sleep(1)
                # Accept google condition
                accept = self.driver.find_element(By.CSS_SELECTOR, "button#L2AGLb")
                print(accept.text)
                accept.click()
                return True
            except:
                time.sleep(0.2)
                return self.accept_google_condition(nb_try=nb_try)
        else:
            return False

    def execute(self):
        i = 0
        found = False
        while i < 50 and not found:
            self.driver.get(f'https://www.google.com/search?q={self.query}&start={i}')
            i += 10
            time.sleep(1.5)
            status_google = self.accept_google_condition()
            if not status_google:
                print("Google condition was not accepted or not present ...")
            if self.find_res_natural():
                time_before = time.time()
                self.website_action()
                time_after = time.time()
                delay = time_after-time_before
                self.database_maj("Found",delay, i//10)
                found = True
        if not found:
            self.database_maj("NotFound", 0, i)
            self.driver.close()
        return found

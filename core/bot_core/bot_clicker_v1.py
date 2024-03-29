import os
import random
import time


from django.db import transaction

from bo.models.siteweb import SiteWeb
from bo.models.requete import Requete

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

    def __init__(self, proxy, query, domain, user_agent, google_ads=False, online=True, coordinate=None):
        """
        init the bot clicker, user_agent is the description of an specific user agent
        """
        self.proxy = proxy
        self.query = query
        self.domain = domain
        self.online = online
        self.google_ads = google_ads
        if coordinate is None:
            coordinate = {"latitude": 41.8781, "longitude": -87.6298, "accuracy": 100}
        self.driver = self.init_webdriver(user_agent, coordinate)

    def init_webdriver(self, user_agent, coordinate):

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
            driver.execute_cdp_cmd("Emulation.setGeolocationOverride", coordinate)
        return driver


    def find_res_natural(self):
        result = self.driver.find_element(By.ID, "rso")
        last_offset = 0
        for res in result.find_elements(By.CSS_SELECTOR, ".uUPGi"):
            try:
                actions = ActionChains(self.driver)
                actions.move_to_element(res).perform()
            except:
                self.driver.execute_script(f"window.scrollTo({last_offset}, {res.location['y']})")
            time.sleep(0.21)
            last_offset = res.location["y"]
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
        if len(p) > 7:
            for par in p:
                loc = par.location
                delay = random.choice(RANDOM_VARIABLE["delay"])
                self.driver.execute_script(f"window.scrollTo({last_offset}, {loc['y']})")
                last_offset = loc["y"]
                time.sleep(delay)
        else:
            for nb_scroll in range(21):
                offset = random.choice(RANDOM_VARIABLE["scroll"])
                delay = random.choice(RANDOM_VARIABLE["delay"])
                self.driver.execute_script(f"window.scrollTo({last_offset}, {last_offset + offset})")
                time.sleep(delay)
                last_offset += offset

    def database_maj(self,found,delay,pos):
        with transaction.atomic():
            r=Requete.objects.create(libelle=self.query)
            s,status=SiteWeb.objects.get_or_create(url=self.driver.current_url)
            s.requetes.add(r, through_defaults={'resultat': found,'proxy': self.proxy["host"], 'timescrolling':delay,
                                                'positition_page':pos})

    def login_google_account(self,login,password):

        # msg = MIMEMultipart()
        # msg['From'] = 'bertrandgaudreau8@gmail.com'
        # msg['To'] = 'zakaria.hairane@gmail.com'
        # msg['Subject'] = 'new mail'
        # message =  "Brand news !! je te confirme ton accès"
        # msg.attach(MIMEText(message))
        # mailserver = smtplib.SMTP('smtp.gmail.com', 587)
        # mailserver.ehlo()
        # mailserver.starttls()
        # mailserver.ehlo()
        # mailserver.login('bertrandgaudreau8@gmail.com', 'Bertrand2911')
        # mailserver.sendmail('bertrandgaudreau8@gmail.com', 'zakaria.hairane@gmail.com', msg.as_string())
        #mailserver.quit()
        self.driver.get("https://stackoverflow.com/users/login?ssrc=head&returnurl=https%3a%2f%2fstackoverflow.com%2f")
        time.sleep(5000)
        self.driver.find_element(By.CLASS_NAME, ".s-btn__google").click()
        time.sleep(3)
        self.driver.find_element(By.ID, "susi-modal-google-button").click()
        self.driver.find_element(By.ID, "identifierNext").click()
        time.sleep(3000)
        self.driver.find_element(By.CSS_SELECTOR, "input[name=password]").send_keys(password)
        time.sleep(3)
        self.driver.find_element(By.ID, "passwordNext").click()
        time.sleep(3)

    def find_res_ads(self):
        last_offset = 0
        clicked_ads = []
        cpt = 0
        all_ads = self.driver.find_elements(By.CSS_SELECTOR, "div[aria-label=Annonces] .uEierd")
        while cpt < len(all_ads):
            # get ads at each loop to avoid stale element error (less efficient but don't fail)
            all_ads = self.driver.find_elements(By.CSS_SELECTOR, "div[aria-label=Annonces] .uEierd")
            annonce = all_ads[cpt]
            clicked_ads.append(annonce.text)
            cpt += 1
            try:
                actions = ActionChains(self.driver)
                actions.move_to_element(annonce).perform()
                time.sleep(0.5)
            except:
                loc = annonce.location
                self.driver.execute_script(f"window.scrollTo({last_offset}, {loc['y']})")
                last_offset = loc["y"]
                time.sleep(0.37)
            try:
                domain = annonce.find_element(By.CSS_SELECTOR, "span[role=text]")
                link = annonce.find_element(By.CSS_SELECTOR, "[role=presentation]")
                if self.domain not in domain.text:
                    link.click()
                    time.sleep(0.3)
                    self.website_action()
                    time.sleep(1.2)
                    self.driver.execute_script("window.history.go(-1)")
                    time.sleep(1.2)
            except:
                print(f"\n\n----- Dont find link for {annonce.text}-------------\n")
                try:
                    website = annonce.find_element(By.CSS_SELECTOR, "div.Qc4Zr")
                    print("[INFO_ADS] Call ads ==> found website to click")
                    if "Accéder au site Web" in website.text:
                        print("\t ===> click on website subads")
                        website.click()
                        time.sleep(0.5)
                        self.website_action()
                        time.sleep(0.2)
                        self.driver.execute_script("window.history.go(-1)")
                        time.sleep(1.1)
                except:
                    print("[ERROR] Definitively not found link \n")
        return True, clicked_ads

    def accept_google_condition(self, nb_try=0):
        nb_try += 1
        if nb_try < MAX_TRY_GOOGLE:
            try:
                for i in range(10):
                    try:
                        p = self.driver.find_elements(By.CSS_SELECTOR, "#jYfXMb p")
                        last_offset = 0
                        for i in p:
                            loc = i.location
                            self.driver.execute_script(f"window.scrollTo({last_offset}, {loc['y']})")
                            last_offset = loc["y"]
                        # read more to make accept button visible
                        read_more = self.driver.find_element(By.ID, "KByQx")
                        read_more.click()
                        time.sleep(0.15)
                    except:
                        pass
                time.sleep(1)
                # Accept google condition
                accept = self.driver.find_element(By.CSS_SELECTOR, "button#L2AGLb")
                accept.click()
                return True
            except:
                time.sleep(0.2)
                return self.accept_google_condition(nb_try=nb_try)
        else:
            return False

    def execute(self):
        if self.google_ads:
            self.driver.get(f'https://www.google.com/search?q={self.query}')
            time.sleep(1.4)
            self.accept_google_condition()
            time.sleep(1)
            try:
                # locate me (activate the google location)
                locate = self.driver.find_element(By.TAG_NAME, "update-location")
                if "position" in locate.find_element(By.CSS_SELECTOR, "div").text:
                    locate.click()
                    time.sleep(4)
            except:
                print("No Location was provided")
            status, proof = self.find_res_ads()
            return status, proof
        else:
            i = 0
            found = False
            while i < 50 and not found:
                # self.login_google_account('bertrandgaudreau8@gmail.com','Bertrand2911')
                # time.sleep(3000)
                self.driver.get(f'https://www.google.com/search?q={self.query}&start={i}')
                i += 10
                time.sleep(1.5)
                status_google = self.accept_google_condition()
                time.sleep(1.2)

                try:
                    # locate me (activate the google location)
                    locate = self.driver.find_element(By.TAG_NAME, "update-location")
                    if "position" in locate.find_element(By.CSS_SELECTOR, "div").text:
                        locate.click()
                        time.sleep(4)
                except:
                    pass

                if not status_google:
                    print("Google condition was not accepted or not present ...")
                if self.find_res_natural():
                    time_before = time.time()
                    self.website_action()
                    proof = [p.text for p in self.driver.find_elements(By.TAG_NAME, "p")]
                    time_after = time.time()
                    delay = time_after-time_before
                    self.database_maj("Found",delay, i//10)
                    found = True
            if not found:
                self.database_maj("NotFound", 0, i)
                proof = ["site pas trouvé ==> no proof of work"]
                self.driver.close()
            return found, proof

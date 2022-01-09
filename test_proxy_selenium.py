import time

from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from seleniumwire import webdriver


PROXY_HOST = "88.151.10.50"
PROXY_PORT = "12323"
PROXY_USER = "7a30a18635d4"
PROXY_PASS = "25091b96f6"

options = {
    'proxy': {
        'http': f'http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}',
        'https': f'https://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}',
        'no_proxy': 'localhost,127.0.0.1'
    }
}

driver = webdriver.Chrome(ChromeDriverManager().install(), seleniumwire_options=options)

driver.get('https://google.com')


time.sleep(1000)

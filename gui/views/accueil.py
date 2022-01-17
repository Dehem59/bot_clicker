import time

from django.views import View
from django.shortcuts import render
from selenium.webdriver import DesiredCapabilities
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from bo.models import Proxy, UserAgent


class IndexView(View):

    def get(self, request):
        return render(request, 'gui/index.html', {})


class ManualLaunchView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "gui/manual_launch.html", {"proxies": Proxy.objects.all(),
                                                          "user_agents": UserAgent.objects.all()})

    def post(self, request, *args, **kwargs):
        proxy = Proxy.objects.get(pk=request.POST["proxy"])
        user = UserAgent.objects.get(pk=request.POST["user_agent"])
        driver = self.launch_driver(user, proxy)
        driver.get("https://www.google.com/")
        duree = int(request.POST["duree"])
        time.sleep(duree)
        return self.get(request, "gui/manual_launch.html", {"proxies": Proxy.objects.all(),
                                                          "user_agents": UserAgent.objects.all()})

    def launch_driver(self, user, proxy):
        options = {
            'proxy': {
                'http': f'http://{proxy.user}:{proxy.password}@{proxy.host}:{proxy.port}',
                'https': f'https://{proxy.user}:{proxy.password}@{proxy.host}:{proxy.port}',
                'no_proxy': 'localhost,127.0.0.1'
            }
        }
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument(f'--user-agent={user.definition}')
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities["real_mobile"] = True
        driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=capabilities,
                                  chrome_options=chrome_options, seleniumwire_options=options)
        driver.set_window_position(50, 0)
        driver.set_window_size(390, 844)
        return driver
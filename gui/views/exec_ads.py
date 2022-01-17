from django.http import JsonResponse
from django.views import View
from django.shortcuts import render

from bo.models import UserAgent, Keyword, Proxy
from core.bot_core.bot_clicker_v1 import BotClickerV1
import time
from gui.views.common import CommonExecView


class ExecutionAdsView(CommonExecView):

    http_method_names = ["get", "post", "patch"]

    def get(self, request, *args, **kwargs):
        return self.get_process(request, "gui/exec_ads.html", *args, **kwargs)


    def post(self, request, *args, **kwargs):
        return self.post_process(request, True, *args, **kwargs)




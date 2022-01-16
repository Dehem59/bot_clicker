from django.http import JsonResponse
from django.views import View
from django.shortcuts import render

from bo.models import UserAgent, Aclicker
from core.bot_core.bot_clicker_v1 import BotClickerV1
from core.bot_core.variable import PROXY
from bot_clicker.tasks import launch_bot


class StatistiqueView(View):

    http_method_names = ["get", "post", "patch"]

    def get(self, request, *args, **kwargs):
        AclickerObjects = Aclicker.objects.all().order_by("-date_heure")
        return render(request, "gui/admin_temp.html", { "aclicker_list": AclickerObjects})







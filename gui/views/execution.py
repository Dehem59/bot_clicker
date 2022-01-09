from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from core.bot_core.bot_clicker_v1 import BotClickerV1
from core.bot_core.variable import PROXY


class ExecutionView(View):

    http_method_names = ["get", "post", "patch"]

    def get(self, request, *args, **kwargs):
        return render(request, "gui/execution.html", {})

    def post(self, request, *args, **kwargs):

        cpt = 0
        nb_proxy = int(request.POST["proxy"])
        query = request.POST["query"]
        headless = request.POST["headless"].lower() == "true"
        for name, proxy in PROXY.items():
            try:
                tmp_bot = BotClickerV1(proxy=proxy, query=query, headless=headless)
                res = tmp_bot.execute()
                cpt += 1
                if cpt == nb_proxy:
                    return JsonResponse({"detail": True, "result": res}, status=200)
            except Exception as exc:
                print(exc)
                return JsonResponse({"detail": exc.args}, status=400)



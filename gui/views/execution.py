from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from core.bot_core.bot_clicker_v1 import BotClickerV1
from core.bot_core.variable import PROXY
from bot_clicker.tasks import test_task


class ExecutionView(View):

    http_method_names = ["get", "post", "patch"]

    def get(self, request, *args, **kwargs):
        return render(request, "gui/execution.html", {"nb_proxy": len(PROXY)})

    def post(self, request, *args, **kwargs):
        cpt = 0
        nb_proxy = int(request.POST["proxy"])
        query = request.POST["query"]
        domaine = request.POST["domaine"]
        online = request.POST["headless"].lower() == "true"
        test_task.delay()

        for name, proxy in PROXY.items():
            try:
                tmp_bot = BotClickerV1(proxy=proxy, query=query, domain=domaine, online=online)
                res = tmp_bot.execute()
                if not res:
                    return JsonResponse({"detail": False, "result": "you're not in results pages"}, status=200)
                cpt += 1
                if cpt == nb_proxy:
                    return JsonResponse({"detail": True, "result": res}, status=200)
            except Exception as exc:
                print(exc)
                return JsonResponse({"detail": exc.args}, status=400)



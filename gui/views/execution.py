from django.http import JsonResponse
from django.views import View
from django.shortcuts import render

from bo.models import UserAgent
from core.bot_core.bot_clicker_v1 import BotClickerV1
from core.bot_core.variable import PROXY
from bot_clicker.tasks import launch_bot


class ExecutionView(View):

    http_method_names = ["get", "post", "patch"]

    def get(self, request, *args, **kwargs):
        user_agents = UserAgent.objects.all()
        return render(request, "gui/execution.html", {"nb_proxy": len(PROXY), "user_agents": user_agents, "nb_user_agent": user_agents.count()})


    def post(self, request, *args, **kwargs):
        nb_proxy = int(request.POST["proxy"])
        query = request.POST["query"]
        domaine = request.POST["domaine"]
        online = request.POST["headless"].lower() == "true"
        user_agent = UserAgent.objects.get(nom=request.POST["user_agent"])
        params = {"query": query, "domaine": domaine, "online": online, "nb_proxy": nb_proxy,
                  "user_agent": user_agent.pk}
        # ref = launch_bot.delay(params)
        cpt = 0
        for name, proxy in PROXY.items():
            try:
                tmp_bot = BotClickerV1(proxy=proxy, query=params["query"], domain=params["domaine"],
                                       user_agent=user_agent.definition, online=params["online"])
                res = tmp_bot.execute()
                if not res:
                    return JsonResponse({"detail": False, "result": "you're not in results pages"}, status=400)
                cpt += 1
                if cpt == params["nb_proxy"]:
                    return JsonResponse({"detail": True, "result": res})
            except Exception as exc:
                print(exc)
                return JsonResponse({"detail": False, "result": str(exc)}, status=400)




from django.http import JsonResponse
from django.views import View
from django.shortcuts import render

from bo.models import UserAgent, Keyword, Proxy
from core.bot_core.bot_clicker_v1 import BotClickerV1
from core.bot_core.variable import PROXY
from bot_clicker.tasks import launch_bot


class CommonView(View):

    http_method_names = ["get", "post", "patch"]

    def get_process(self, request, template_name, *args, **kwargs):
        user_agents = UserAgent.objects.all()
        return render(request, template_name, {"nb_proxy": len(Proxy.objects.all()), "user_agents": user_agents})


    def post_process(self, request, ads_mode, *args, **kwargs):
        nb_proxy = int(request.POST["proxy"])
        query = request.POST["query"]
        query_obj, _ = Keyword.objects.get_or_create(nom=query)
        domaine = request.POST["domaine"]
        online = False
        ads_mode = ads_mode
        user_agent = UserAgent.objects.get(nom=request.POST["user_agent"])
        params = {"query": query_obj.google_correspondance, "domaine": domaine, "online": online, "nb_proxy": nb_proxy,
                  "user_agent": user_agent.pk}
        # ref = launch_bot.delay(params)
        cpt = 0
        for proxy_obj in Proxy.objects.filter(est_actif=True):
            proxy = {"host": proxy_obj.host, "port": proxy_obj.port, "user": proxy_obj.user, "pass": proxy_obj.password}
            try:
                tmp_bot = BotClickerV1(proxy=proxy, query=params["query"], domain=params["domaine"], google_ads=ads_mode,
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




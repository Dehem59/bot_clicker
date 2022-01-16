import random

from django.http import JsonResponse
from django.views import View
from django.shortcuts import render

from bo.models import UserAgent, Keyword, Proxy
from core.bot_core.bot_clicker_v1 import BotClickerV1


class ExecutionAutoView(View):

    http_method_names = ["get", "post", "patch"]

    def get(self, request, *args, **kwargs):
        user_agents = UserAgent.objects.all()
        keywords = Keyword.objects.all()
        return render(
            request, "gui/planification.html", {"nb_proxy": Proxy.objects.all().count(), "user_agents": user_agents,
                                                "keywords": keywords}
        )

    def post(self, request, *args, **kwargs):
        nb_proxy = int(request.POST["proxy"])
        queries = request.POST.getlist("queries[]")
        domaine = request.POST["domaine"]
        online = False
        user_agent = UserAgent.objects.get(nom=request.POST["user_agent"])
        keywords = Keyword.objects.filter(pk__in=queries)
        # ref = launch_bot.delay(params)
        cpt = 0
        proxies = list(Proxy.objects.all())
        seen = set()
        results = {"detail": False, "results": []}
        while cpt < nb_proxy:
            cpt += 1
            current_proxy = random.choice(proxies)
            while current_proxy.host in seen:
                current_proxy = random.choice(proxies)
            seen.add(current_proxy.host)
            for keyword in keywords:
                try:
                    dict_proxy = {
                        "host": current_proxy.host, "port": current_proxy.port, "user": current_proxy.user,
                        "pass": current_proxy.password
                    }
                    tmp_bot = BotClickerV1(proxy=dict_proxy, query=keyword.google_correspondance,
                                           domain=domaine, user_agent=user_agent.definition, online=False)
                    res = tmp_bot.execute()
                    results["results"].append(res)
                except Exception as exc:
                    if "errors" not in results:
                        results["errors"] = [str(exc)]
                    else:
                        results["errors"].append(str(exc))

        return JsonResponse(results, status=200)




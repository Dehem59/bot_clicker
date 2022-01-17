import random
import time

from django.http import JsonResponse
from django.views import View
from django.shortcuts import render

from bo.models import UserAgent, Keyword, Proxy
from core.bot_core.bot_clicker_v1 import BotClickerV1


class CommonExecView(View):

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
                status, proof = tmp_bot.execute()
                if not status:
                    return JsonResponse({"detail": False, "result": "you're not in results pages"}, status=400)
                cpt += 1
                if cpt == params["nb_proxy"]:
                    return JsonResponse({"result": {"execution": status, "proof_of_work": proof}})
            except Exception as exc:
                print(exc)
                return JsonResponse({"detail": False, "result": str(exc)}, status=400)



class CommonAutoView(View):

    http_method_names = ["get", "post", "patch"]

    def get_process(self, request, template_name="gui/planification.html", *args, **kwargs):
        user_agents = UserAgent.objects.all()
        keywords = Keyword.objects.all()
        return render(
            request, template_name, {"nb_proxy": Proxy.objects.all().count(), "user_agents": user_agents,
                                                "keywords": keywords}
        )

    def post_process(self, request, google_ads=False, *args, **kwargs):
        nb_proxy = int(request.POST["proxy"])
        queries = request.POST.getlist("queries[]")
        domaine = request.POST["domaine"]
        online = False
        user_agent = UserAgent.objects.get(nom=request.POST["user_agent"])
        keywords = Keyword.objects.filter(pk__in=queries)
        delay = int(request.POST["delay"])
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
                                           domain=domaine, user_agent=user_agent.definition, google_ads=google_ads,
                                           online=False)
                    res = tmp_bot.execute()
                    results["results"].append(res)
                    time.sleep(delay)
                except Exception as exc:
                    if "errors" not in results:
                        results["errors"] = [str(exc)]
                    else:
                        results["errors"].append(str(exc))

        return JsonResponse(results, status=200)


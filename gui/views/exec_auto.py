from django.http import JsonResponse
from django.views import View
from django.shortcuts import render

from bo.models import UserAgent, Keyword, Proxy



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
        pass




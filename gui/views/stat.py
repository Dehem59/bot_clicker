from django.http import JsonResponse
from django.views import View
from django.shortcuts import render

from bo.models import UserAgent, Aclicker


class StatistiqueView(View):

    http_method_names = ["get", "post", "patch"]

    def get(self, request, *args, **kwargs):
        AclickerObjects = Aclicker.objects.all().order_by("-date_heure")
        return render(request, "gui/admin_temp.html", { "aclicker_list": AclickerObjects})







from django.http import JsonResponse
from django.views import View
from django.shortcuts import render


class ExecutionView(View):

    http_method_names = ["get", "post", "patch"]

    def get(self, request, *args, **kwargs):
        return render(request, "gui/execution.html", {})

    def post(self, request, *args, **kwargs):
        return JsonResponse({"detail": "post request called", "data_received": request.POST}, status=200)

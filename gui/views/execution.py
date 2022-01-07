from django.views import View
from django.shortcuts import render


class ExecutionView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "gui/execution.html", {})


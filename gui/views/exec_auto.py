from gui.views.common import CommonAutoView


class ExecutionAutoView(CommonAutoView):

    http_method_names = ["get", "post", "patch"]

    def get(self, request, *args, **kwargs):
        return self.get_process(request, "gui/planification.html", *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.post_process(request, False, *args, **kwargs)


class ExecutionAdsAutoView(CommonAutoView):

    http_method_names = ["get", "post", "patch"]

    def get(self, request, *args, **kwargs):
        return self.get_process(request, "gui/planification_ads.html", *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.post_process(request, True, *args, **kwargs)



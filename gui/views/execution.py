from gui.views.common import CommonExecView


class ExecutionView(CommonExecView):

    http_method_names = ["get", "post", "patch"]

    def get(self, request, *args, **kwargs):
        return self.get_process(request, "gui/execution.html", *args, **kwargs)


    def post(self, request, *args, **kwargs):
        return self.post_process(request, False, *args, **kwargs)




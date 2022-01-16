from django.contrib.auth.decorators import login_required
from django.urls import path
from gui.views import ExecutionView, IndexView, ExecutionAutoView

urlpatterns = [
    path("execution/", login_required(ExecutionView.as_view()), name="execution"),
    path("execution-auto/", login_required(ExecutionAutoView.as_view()), name="auto-exec"),
    path("", IndexView.as_view(), name="index")
]
from django.contrib.auth.decorators import login_required
from django.urls import path
from gui.views import ExecutionView, IndexView, StatistiqueView, ExecutionAutoView

urlpatterns = [
    path("execution/", ExecutionView.as_view(), name="execution"),
    path("stat/", login_required(StatistiqueView.as_view()), name="stat"),
    path("execution-auto/", login_required(ExecutionAutoView.as_view()), name="auto-exec"),
    path("", IndexView.as_view(), name="index")
]
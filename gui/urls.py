from django.contrib.auth.decorators import login_required
from django.urls import path
from gui.views import ExecutionView, IndexView, StatistiqueView, ExecutionAutoView, ExecutionAdsView, \
    ExecutionAdsAutoView, ManualLaunchView

urlpatterns = [
    path("execution/", login_required(ExecutionView.as_view()), name="execution"),
    path("execution-ads/", login_required(ExecutionAdsView.as_view()), name="execution-ads"),
    path("stat/", login_required(StatistiqueView.as_view()), name="stat"),
    path("manual/", login_required(ManualLaunchView.as_view()), name="manual"),
    path("execution-auto/", login_required(ExecutionAutoView.as_view()), name="auto-exec"),
    path("execution-auto-ads/", login_required(ExecutionAdsAutoView.as_view()), name="auto-exec-ads"),
    path("", login_required(IndexView.as_view()), name="index")
]
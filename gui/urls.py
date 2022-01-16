from django.contrib.auth.decorators import login_required
from django.urls import path
from gui.views import ExecutionView, IndexView, StatistiqueView

urlpatterns = [
    path("execution", ExecutionView.as_view(), name="execution"),
    path("stat", login_required(StatistiqueView.as_view()), name="stat"),
    path("", IndexView.as_view(), name="index")

]

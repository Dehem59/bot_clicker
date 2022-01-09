from django.urls import path
from gui.views import ExecutionView, IndexView

urlpatterns = [
    path("execution", ExecutionView.as_view(), name="execution"),
    path("", IndexView.as_view(), name="index")
]
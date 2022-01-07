from django.urls import path, re_path
from gui.views import ExecutionView

urlpatterns = [
    path("execution", ExecutionView.as_view(), name="execution"),
]
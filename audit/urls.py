from django.urls import path

from CVProject.constants import LOGS_BASE_URL

from . import views

urlpatterns = [
    path(LOGS_BASE_URL, views.recent_logs, name="recent_logs"),
]

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from CVProject.constants import AUDIT_BASE_URL

from .models import RequestLog


@login_required
def recent_logs(request):
    logs = RequestLog.objects.order_by("-timestamp")[:10]
    context = {
        "title": "Recent Request Logs",
        "logs": logs,
        "home_btn_title": "< Home",
        "column_one_title": "Timestamp",
        "column_two_title": "Method",
        "column_three_title": "Path",
    }
    return render(request, f"{AUDIT_BASE_URL}recent_logs.html", context)

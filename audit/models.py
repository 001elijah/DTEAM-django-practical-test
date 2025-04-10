from django.db import models


class RequestLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=200)
    query_string = models.TextField(blank=True, null=True)
    remote_ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    user = models.ForeignKey(
        "auth.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="request_logs",
    )

    def __str__(self):
        return f"{self.method} {self.path} ({self.timestamp})"

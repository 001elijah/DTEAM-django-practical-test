from .models import RequestLog


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        self.log_request(request)

        return response

    def log_request(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        RequestLog.objects.create(
            method=request.method,
            path=request.path,
            query_string=request.META.get("QUERY_STRING", ""),
            remote_ip=ip,
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
            user=request.user if request.user.is_authenticated else None,
        )

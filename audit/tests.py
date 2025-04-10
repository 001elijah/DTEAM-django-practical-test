from django.urls import reverse

from main.tests import BaseTest

from .models import RequestLog


class RequestLoggingTestCase(BaseTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_logging_middleware_creates_log(self):
        url = reverse("cv_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Check that a log entry was created
        log = RequestLog.objects.first()
        self.assertIsNotNone(log)
        self.assertEqual(log.method, "GET")
        self.assertEqual(log.path, url)
        self.assertEqual(log.user, self.user)

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from api.models import User


class ZipTestCase(TestCase):

    def setUp(self):
        super().setUp()

        self.user = User.objects.create_user(username="username", email="test@example.com", password='password')
        self.user.save()

        # We can't use this because our view is not a classic DRF view.
        # We need a token inside our request.
        # self.client = APIClient()
        # self.client.force_authenticate(user=self.user)

        self.client = APIClient()
        response = self.client.post(
            reverse("rest_login"),
            {
                "email": "test@example.com",
                "password": "password"
            },
            format="json"
        )
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])

    def test_generate_excel_report_view(self):
        url = reverse('generate_zip')

        with self.assertNumQueries(1):
            resp = self.client.get(url, stream=True)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(list(resp)), 53)  # 53 chunks sent

        # An anonymous user should not get the zip.
        self.anonymous_client = APIClient()

        with self.assertNumQueries(0):
            resp = self.anonymous_client.get(url, stream=True)

        self.assertEqual(resp.status_code, 404)

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient


class StaffPermissionTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.staff = User.objects.create_user(
            username="staffer",
            email="staff@example.com",
            password="Test12345!",
            is_staff=True,
        )
        self.user = User.objects.create_user(
            username="regular",
            email="regular@example.com",
            password="Test12345!",
            is_staff=False,
        )
        self.client = APIClient()

    def test_regular_user_cannot_create_program(self):
        self.client.login(username="regular", password="Test12345!")
        resp = self.client.post(
            "/api/programs/",
            {
                "title": "Blocked",
                "language_primary": "en",
                "languages_available": ["en"],
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 403)

    def test_staff_user_can_create_program(self):
        self.client.login(username="staffer", password="Test12345!")
        resp = self.client.post(
            "/api/programs/",
            {
                "title": "Allowed",
                "language_primary": "en",
                "languages_available": ["en"],
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 201)


class OpenApiDocsTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_schema_endpoint_available(self):
        resp = self.client.get("/api/schema/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("openapi", resp.data)

    def test_swagger_ui_served(self):
        resp = self.client.get("/api/docs/")
        self.assertEqual(resp.status_code, 200)
        content = resp.rendered_content.decode().lower()
        self.assertIn("swagger-ui", content)

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


class AuthPermissionTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="apitester",
            email="api@example.com",
            password="Test12345!",
            is_staff=True,
        )
        self.client = APIClient()

    def test_anonymous_can_read_but_cannot_write(self):
        get_status = self.client.get("/api/programs/").status_code
        post_status = self.client.post(
            "/api/programs/",
            {"title": "T", "language_primary": "en", "languages_available": ["en"]},
            format="json",
        ).status_code

        self.assertEqual(get_status, 200)
        self.assertIn(post_status, (401, 403))

    def test_authenticated_session_can_write(self):
        self.client.login(username="apitester", password="Test12345!")
        post_status = self.client.post(
            "/api/programs/",
            {"title": "AuthT", "language_primary": "en", "languages_available": ["en"]},
            format="json",
        ).status_code
        self.assertEqual(post_status, 201)

    def test_authenticated_jwt_can_write(self):
        token_resp = self.client.post(
            "/api/token/",
            {"username": "apitester", "password": "Test12345!"},
            format="json",
        )
        self.assertEqual(token_resp.status_code, 200)
        access = token_resp.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        post_status = self.client.post(
            "/api/programs/",
            {"title": "JwtT", "language_primary": "en", "languages_available": ["en"]},
            format="json",
        ).status_code

        self.assertEqual(post_status, 201)

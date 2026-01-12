from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from core.models import Program, Term


class ValidationTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="validator",
            email="validator@example.com",
            password="Test12345!",
            is_staff=True,
        )
        self.client = APIClient()
        self.client.login(username="validator", password="Test12345!")

        self.program = Program.objects.create(
            title="Python 101",
            language_primary="en",
            languages_available=["en", "fr"],
            status="draft",
        )
        self.term = Term.objects.create(
            program=self.program,
            term_number=1,
            title="Basics",
        )

    def _lesson_payload(self):
        return {
            "term_id": self.term.id,
            "lesson_number": 1,
            "title": "Intro",
            "content_type": "video",
            "content_language_primary": "en",
            "content_languages_available": ["en", "fr"],
            "content_urls_by_language": {
                "en": "https://cdn.example.com/en.mp4",
                "fr": "https://cdn.example.com/fr.mp4",
            },
            "status": "draft",
        }

    def test_program_requires_primary_language_in_languages_available(self):
        resp = self.client.post(
            "/api/programs/",
            {
                "title": "Bad Program",
                "language_primary": "en",
                "languages_available": ["fr", "es"],
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("languages_available", resp.data)

    def test_scheduled_lesson_requires_future_publish_at(self):
        payload = self._lesson_payload()
        payload["status"] = "scheduled"

        # Missing publish_at
        resp_missing = self.client.post("/api/lessons/", payload, format="json")
        self.assertEqual(resp_missing.status_code, 400)
        self.assertIn("publish_at", resp_missing.data)

        # Publish in the past
        payload["publish_at"] = (timezone.now() - timedelta(minutes=5)).isoformat()
        resp_past = self.client.post("/api/lessons/", payload, format="json")
        self.assertEqual(resp_past.status_code, 400)
        self.assertIn("publish_at", resp_past.data)

    def test_published_lesson_requires_valid_published_at(self):
        payload = self._lesson_payload()
        payload["status"] = "published"

        # Missing published_at
        resp_missing = self.client.post("/api/lessons/", payload, format="json")
        self.assertEqual(resp_missing.status_code, 400)
        self.assertIn("published_at", resp_missing.data)

        # Published_at cannot be in the future
        payload["published_at"] = (timezone.now() + timedelta(minutes=10)).isoformat()
        resp_future = self.client.post("/api/lessons/", payload, format="json")
        self.assertEqual(resp_future.status_code, 400)
        self.assertIn("published_at", resp_future.data)

    def test_primary_language_url_is_required(self):
        payload = self._lesson_payload()
        payload["content_urls_by_language"] = {
            "fr": "https://cdn.example.com/fr.mp4",
        }
        resp = self.client.post("/api/lessons/", payload, format="json")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("content_urls_by_language", resp.data)

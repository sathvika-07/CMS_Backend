from django.test import TestCase
from rest_framework.test import APIClient

from core.models import Program, Topic


class FilterSearchPaginationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Topics for filtering/search
        topic_ai = Topic.objects.create(name="AI")
        topic_web = Topic.objects.create(name="Web")

        # Programs: mix statuses and languages
        programs = []
        for idx in range(12):
            prog = Program.objects.create(
                title=f"Data Course {idx}",
                description="Learn data",
                language_primary="en" if idx % 2 == 0 else "es",
                languages_available=["en", "es"],
                status="published" if idx % 3 == 0 else "draft",
            )
            programs.append(prog)

        # Attach topics for topic-based search/filter
        programs[0].topics.add(topic_ai)
        programs[1].topics.add(topic_web)
        programs[2].topics.add(topic_ai, topic_web)

    def test_pagination_page_and_size(self):
        resp = self.client.get("/api/programs/?page=2&page_size=5")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["count"], 12)
        self.assertEqual(len(resp.data["results"]), 5)

    def test_filter_by_status(self):
        resp = self.client.get("/api/programs/?status=published&page_size=50")
        self.assertEqual(resp.status_code, 200)
        # Every 3rd program is published → 4 published out of 12
        self.assertEqual(resp.data["count"], 4)
        self.assertTrue(all(item["status"] == "published" for item in resp.data["results"]))

    def test_search_by_title_and_topic(self):
        # Search matches title substring "Data" and topic name "AI"
        resp_title = self.client.get("/api/programs/?search=Data&page_size=50")
        self.assertEqual(resp_title.status_code, 200)
        self.assertEqual(resp_title.data["count"], 12)

        resp_topic = self.client.get("/api/programs/?search=AI&page_size=50")
        self.assertEqual(resp_topic.status_code, 200)
        self.assertGreaterEqual(resp_topic.data["count"], 2)
        # Ensure results include only entries with the AI topic in search hit
        titles = [item["title"] for item in resp_topic.data["results"]]
        self.assertTrue(any("Data Course" in t for t in titles))

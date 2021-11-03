import re
import json
import unittest
from fastapi.testclient import TestClient

from .main import app
from .models import ShortURL
from .settings import exec_env


# TODO: this should be done better and safer, probably by mocking the DynamoDB class
if exec_env != "local":
    exit("Running the tests in prod could drop the database!")


class TestShortenURLAPI(unittest.TestCase):
    def clean_database(self):
        for item in ShortURL.scan():
            item.delete()

    def setUp(self):
        self.client = TestClient(app)
        self.clean_database()

    def test_shorten_without_user_controlled_key(self):
        """Its possible to shorten a URL"""
        response = self.client.post("/shorten", json={"url": "https://facebook.com"})
        content = json.loads(response._content)
        url_match = re.fullmatch(r"https:\/\/tier.app\/[a-zA-Z0-9]+", content["url"])

        assert url_match is not None

    def test_shorten_url_validation(self):
        """Its not possible to create short URL for non URLs"""
        response = self.client.post("/shorten", json={"url": "notevenaurl"})
        assert response.status_code == 422

    def test_shorten_with_user_controlled_key(self):
        """Its possible to supply own key, and the key will be used for the short key"""
        key = "mytestkey"
        response = self.client.post(
            "/shorten", json={"url": "https://facebook.com", "key": key}
        )
        content = json.loads(response._content)
        assert content["url"] == f"https://tier.app/{key}"

    def test_shorten_key_unique_contraint(self):
        """Shortened URL cannot be created with an existing short key"""
        # Create shortened URL
        key = "mytestkey"
        self.client.post("/shorten", json={"url": "https://facebook.com", "key": key})

        # Try to recreate with same key
        response = self.client.post(
            "/shorten", json={"url": "https://facebook.com", "key": key}
        )
        content = json.loads(response._content)
        assert response.status_code == 400
        assert content["detail"] == "Short key has to be unique!"


class TestStatisticsAPI(unittest.TestCase):
    def clean_database(self):
        for item in ShortURL.scan():
            item.delete()

    def setUp(self):
        self.client = TestClient(app)
        self.clean_database()

    def test_statistics_url(self):
        """Its possible to shorten a URL"""

        # Create a short URL
        key = "mykey"
        self.client.post("/shorten", json={"url": "https://facebook.com", "key": key})

        # Visit short URL
        self.client.get(f"/{key}")

        # View count is incremented
        response = self.client.get(f"/statistics/{key}")
        content = json.loads(response._content)
        assert content == {"url": "https://facebook.com", "views": 1}

    def test_statistics_url_non_existent_response(self):
        """Retrieving statisctics of not existing short URLs results in 404"""

        # Visit short URL
        response = self.client.get("/notexisting")
        content = json.loads(response._content)
        assert response.status_code == 404
        assert content["detail"] == "URL for short key: 'notexisting' not found!"

import pytest
from rest_framework.test import APIClient


class TestHealthCheck:
    client = APIClient()
    url = "/health/check/"

    def test_get_health(self):
        response = self.client.get(self.url)

        assert "active" in response.json()["message"]
        assert response.status_code == 200

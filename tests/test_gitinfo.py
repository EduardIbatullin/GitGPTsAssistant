# tests/test_gitinfo.py

import pytest
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from app.api.dependencies import get_github_client
from app.domain.services.gitinfo_service import GitInfoService

client = TestClient(app)


class MockGitInfoService:
    async def list_branches(self, repo: str):
        return [{"name": "main"}, {"name": "dev"}]

    async def list_commits(self, repo: str, path: str = None):
        return [
            {
                "sha": "abc123",
                "commit": {
                    "author": {"name": "Alice", "date": "2024-05-01T12:00:00Z"},
                    "message": "Initial commit",
                }
            },
            {
                "sha": "def456",
                "commit": {
                    "author": {"name": "Bob", "date": "2024-05-02T15:30:00Z"},
                    "message": "Update readme",
                }
            }
        ]


@pytest.fixture(autouse=True)
def override_dependency():
    app.dependency_overrides[get_github_client] = lambda: MockGitInfoService()
    yield
    app.dependency_overrides = {}


def test_list_commits_repo():
    response = client.get("/repos/test-repo/commits")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["sha"] == "abc123"
    assert "message" in data[0]["commit"]


def test_list_commits_with_path():
    response = client.get("/repos/test-repo/commits?path=README.md")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[1]["commit"]["author"]["name"] == "Bob"

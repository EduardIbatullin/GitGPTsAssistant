# tests/test_github_client.py

import pytest
import pytest_asyncio
from unittest.mock import patch
from app.infrastructure.github_client import GitHubClient

@pytest_asyncio.fixture
async def client():
    return GitHubClient()

@patch("httpx.AsyncClient.get")
@pytest.mark.asyncio
async def test_list_repo_tree(mock_get, client):
    class MockResponse:
        def __init__(self, payload):
            self.payload = payload
            self.status_code = 200

        async def json(self):
            return self.payload

        def raise_for_status(self):
            pass

    def side_effect(url, headers):
        if "repos/" in url and "/git/trees/" not in url:
            return MockResponse({"default_branch": "main"})
        if "/git/trees/" in url:
            return MockResponse({
                "tree": [
                    {"path": "README.md", "type": "blob"},
                    {"path": "src", "type": "tree"},
                    {"path": "src/main.py", "type": "blob"},
                ]
            })

    mock_get.side_effect = side_effect

    tree = await client.list_repo_tree("test-repo")
    assert isinstance(tree, list)
    assert {"path": "README.md", "type": "blob"} in tree
    assert {"path": "src", "type": "tree"} in tree
    assert {"path": "src/main.py", "type": "blob"} in tree

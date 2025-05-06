# tests/test_github_client.py

import pytest
import pytest_asyncio
from unittest.mock import patch
from app.infrastructure.github_client import GitHubClient

@pytest_asyncio.fixture
async def client():
    return GitHubClient()

class MockResponse:
    def __init__(self, data: dict):
        self._data = data
        self.status_code = 200

    async def json(self):
        return self._data

    def raise_for_status(self):
        pass

@patch("httpx.AsyncClient.get")
@pytest.mark.asyncio
async def test_list_repo_tree(mock_get, client):
    mock_get.side_effect = [
        MockResponse({"default_branch": "main"}),
        MockResponse({
            "tree": [
                {"path": "README.md", "type": "blob"},
                {"path": "src", "type": "tree"},
                {"path": "src/main.py", "type": "blob"},
            ]
        }),
    ]

    tree = await client.list_repo_tree("test-repo")
    assert isinstance(tree, list)
    assert {"path": "README.md", "type": "blob"} in tree
    assert {"path": "src", "type": "tree"} in tree
    assert {"path": "src/main.py", "type": "blob"} in tree

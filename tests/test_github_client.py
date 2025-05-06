# tests/test_github_client.py

import pytest
import pytest_asyncio
from unittest.mock import patch, AsyncMock
from app.infrastructure.github_client import GitHubClient

@pytest_asyncio.fixture
async def client():
    return GitHubClient()

def make_async_response(data: dict) -> AsyncMock:
    mock = AsyncMock()
    mock.status_code = 200
    mock.json.return_value = data
    mock.raise_for_status.return_value = None
    return mock

@patch("httpx.AsyncClient.get")
@pytest.mark.asyncio
async def test_list_repo_tree(mock_get, client):
    mock_get.side_effect = [
        make_async_response({"default_branch": "main"}),
        make_async_response({
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

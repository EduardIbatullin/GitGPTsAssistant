# tests/test_github_client.py

import pytest
import pytest_asyncio
from unittest.mock import patch, AsyncMock
from app.infrastructure.github_client import GitHubClient

@pytest_asyncio.fixture
async def client():
    return GitHubClient()

@patch("httpx.AsyncClient.get", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_list_repo_tree(mock_get, client):
    mock_get.side_effect = [
        AsyncMock(status_code=200, json=AsyncMock(return_value={"default_branch": "main"})),
        AsyncMock(status_code=200, json=AsyncMock(return_value={
            "tree": [
                {"path": "README.md", "type": "blob"},
                {"path": "src", "type": "tree"},
                {"path": "src/main.py", "type": "blob"},
            ]
        }))
    ]

    tree = await client.list_repo_tree("test-repo")
    assert isinstance(tree, list)
    assert {"path": "README.md", "type": "blob"} in tree
    assert {"path": "src", "type": "tree"} in tree
    assert {"path": "src/main.py", "type": "blob"} in tree

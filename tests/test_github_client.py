# tests/test_github_client.py

import pytest
import pytest_asyncio
from unittest.mock import patch, AsyncMock
from app.infrastructure.github_client import GitHubClient

@pytest_asyncio.fixture
async def client():
    return GitHubClient()

@patch("httpx.AsyncClient.get")
@pytest.mark.asyncio
async def test_list_repo_tree(mock_get, client):
    repo_info = {"default_branch": "main"}
    tree_data = {
        "tree": [
            {"path": "README.md", "type": "blob"},
            {"path": "src", "type": "tree"},
            {"path": "src/main.py", "type": "blob"},
        ]
    }

    async def side_effect(url, headers):
        if url.endswith("/repos/your-github-username/test-repo"):
            mock = AsyncMock()
            mock.status_code = 200
            mock.json.return_value = repo_info
            return mock
        if url.endswith("/git/trees/main?recursive=1"):
            mock = AsyncMock()
            mock.status_code = 200
            mock.json.return_value = tree_data
            return mock

    mock_get.side_effect = side_effect

    tree = await client.list_repo_tree("test-repo")
    assert isinstance(tree, list)
    assert {"path": "README.md", "type": "blob"} in tree
    assert {"path": "src", "type": "tree"} in tree
    assert {"path": "src/main.py", "type": "blob"} in tree

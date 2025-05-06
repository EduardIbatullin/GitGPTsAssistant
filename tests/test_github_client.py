# tests/test_github_client.py

import pytest
import pytest_asyncio
from unittest.mock import patch, AsyncMock
from app.infrastructure.github_client import GitHubClient

@pytest_asyncio.fixture
async def client():
    return GitHubClient()

def make_mock_response(data: dict) -> AsyncMock:
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json = AsyncMock(return_value=data)
    return mock_response

@patch("httpx.AsyncClient.get", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_list_repo_tree(mock_get, client):
    mock_get.side_effect = [
        make_mock_response({"default_branch": "main"}),
        make_mock_response({
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

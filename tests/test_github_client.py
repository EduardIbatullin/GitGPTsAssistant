# tests/test_github_client.py

import pytest
import pytest_asyncio
from unittest.mock import patch, Mock
from app.infrastructure.github_client import GitHubClient

@pytest_asyncio.fixture
async def client():
    return GitHubClient()

@patch("httpx.AsyncClient.get")
@pytest.mark.asyncio
async def test_list_repo_tree(mock_get, client):
    mock_repo_info = Mock()
    mock_repo_info.status_code = 200
    mock_repo_info.json = lambda: {"default_branch": "main"}
    mock_repo_info.raise_for_status.return_value = None

    mock_tree_info = Mock()
    mock_tree_info.status_code = 200
    mock_tree_info.json = lambda: {
        "tree": [
            {"path": "README.md", "type": "blob"},
            {"path": "src", "type": "tree"},
            {"path": "src/main.py", "type": "blob"},
        ]
    }
    mock_tree_info.raise_for_status.return_value = None

    mock_get.side_effect = [mock_repo_info, mock_tree_info]

    tree = await client.list_repo_tree("test-repo")

    assert isinstance(tree, list)
    assert {"path": "README.md", "type": "blob"} in tree
    assert {"path": "src", "type": "tree"} in tree
    assert {"path": "src/main.py", "type": "blob"} in tree

@patch("httpx.AsyncClient.get")
@pytest.mark.asyncio
async def test_list_branches(mock_get, client):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json = lambda: [
        {"name": "main", "commit": {"sha": "abc123"}},
        {"name": "dev", "commit": {"sha": "def456"}}
    ]
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    branches = await client.list_branches("test-repo")

    assert isinstance(branches, list)
    assert any(b["name"] == "main" for b in branches)
    assert any(b["name"] == "dev" for b in branches)
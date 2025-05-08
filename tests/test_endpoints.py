# tests/test_endpoints.py

import pytest
from fastapi.testclient import TestClient
from fastapi import status

from app.api.main import app
from app.api.dependencies import get_file_service, get_github_client
from app.domain.models import FileContentResponse, RepoStructureResponse
from app.core.exceptions import ResourceNotFoundError, InvalidRepositoryError

# --- Сервис-заглушка для успешных сценариев ---
class DummyFileService:
    async def get_repo_structure(self, repo: str) -> list:
        return [
            {"path": "", "type": "dir"},
            {"path": "README.md", "type": "file"},
            {"path": "subdir", "type": "dir"},
            {"path": "subdir/nested.txt", "type": "file"},
        ]

    async def get_file_content(self, repo: str, path: str) -> FileContentResponse:
        text = f"Content of {path}"
        return FileContentResponse(path=path, content=text, encoding="utf-8")

    async def create_file(
        self, repo: str, path: str, filename: str, content: str, message: str
    ) -> FileContentResponse:
        full_path = f"{path}/{filename}" if path else filename
        return FileContentResponse(path=full_path, content=content, encoding="utf-8")

    async def update_file(
        self, repo: str, path: str, filename: str, content: str, message: str
    ) -> FileContentResponse:
        full_path = f"{path}/{filename}" if path else filename
        return FileContentResponse(path=full_path, content=content, encoding="utf-8")

    async def delete_file(
        self, repo: str, path: str, filename: str, message: str
    ) -> FileContentResponse:
        full_path = f"{path}/{filename}" if path else filename
        return FileContentResponse(path=full_path, content="", encoding="utf-8")


class DummyGitInfoService:
    async def list_branches(self, repo: str) -> list:
        return [
            {"name": "main", "commit": {"sha": "abc123"}},
            {"name": "dev", "commit": {"sha": "def456"}}
        ]


# --- Сервис-заглушка для ошибок ---
class ErrorFileService:
    def __init__(self, exc):
        self.exc = exc

    async def get_repo_structure(self, repo: str):
        raise self.exc

    async def get_file_content(self, repo: str, path: str):
        raise self.exc

    async def create_file(self, repo: str, path: str, filename: str, content: str, message: str):
        raise self.exc

    async def update_file(self, repo: str, path: str, filename: str, content: str, message: str):
        raise self.exc

    async def delete_file(self, repo: str, path: str, filename: str, message: str):
        raise self.exc


# Инициализируем клиент
client = TestClient(app)

# Переназначение зависимостей
app.dependency_overrides[get_file_service] = lambda: DummyFileService()
app.dependency_overrides[get_github_client] = lambda: DummyGitInfoService()


def test_get_repo_structure():
    response = client.get("/repos/test-repo/structure")
    assert response.status_code == 200
    assert response.json() == {
        "repo": "test-repo",
        "tree": [
            {"path": "", "type": "dir"},
            {"path": "README.md", "type": "file"},
            {"path": "subdir", "type": "dir"},
            {"path": "subdir/nested.txt", "type": "file"},
        ],
    }


def test_get_branches():
    response = client.get("/repos/test-repo/branches")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(branch["name"] == "main" for branch in data)
    assert any(branch["name"] == "dev" for branch in data)

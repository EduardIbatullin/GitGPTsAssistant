# app/domain/services/file_service.py

import base64
import httpx

from app.infrastructure.github_client import GitHubClient
from app.domain.models import FileContentResponse, RepoStructureResponse
from app.core.exceptions import ResourceNotFoundError, GitHubAPIError, InvalidRepositoryError

class FileService:
    """
    Сервис для работы с GitHub API: структура и файлы.
    """
    def __init__(self, github_client: GitHubClient):
        self.github_client = github_client

    async def get_repo_structure(self, repo: str) -> RepoStructureResponse:
        try:
            tree = await self.github_client.list_repo_tree(repo)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise InvalidRepositoryError(f"Репозиторий '{repo}' не найден")
            raise GitHubAPIError(f"GitHub API error: {e.response.text}", status_code=e.response.status_code)

        return RepoStructureResponse(repo=repo, tree=tree)

    async def get_file_content(self, repo: str, path: str) -> FileContentResponse:
        try:
            api_data = await self.github_client.get_file_content(repo, path)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ResourceNotFoundError(f"Репозиторий '{repo}' или файл '{path}' не найден")
            raise GitHubAPIError(f"GitHub API error: {e.response.text}", status_code=e.response.status_code)

        raw_b64 = api_data.get("content", "")
        decoded = base64.b64decode(raw_b64).decode("utf-8")
        return FileContentResponse(path=path, content=decoded, encoding="utf-8")

    async def create_file(self, repo: str, path: str, filename: str, content: str, message: str) -> FileContentResponse:
        try:
            result = await self.github_client.create_file(repo, path, filename, content, message)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ResourceNotFoundError(f"Репозиторий '{repo}' или путь '{path}' не найден")
            raise GitHubAPIError(f"GitHub API error: {e.response.text}", status_code=e.response.status_code)

        file_info = result["content"]
        return FileContentResponse(path=file_info["path"], content=content, encoding="utf-8")

    async def update_file(self, repo: str, path: str, filename: str, content: str, message: str) -> FileContentResponse:
        try:
            result = await self.github_client.update_file(repo, path, filename, content, message)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ResourceNotFoundError(f"Файл '{path.rstrip('/')}/{filename}' не найден в репозитории '{repo}'")
            raise GitHubAPIError(f"GitHub API error: {e.response.text}", status_code=e.response.status_code)

        file_info = result["content"]
        return FileContentResponse(path=file_info["path"], content=content, encoding="utf-8")

    async def delete_file(self, repo: str, path: str, filename: str, message: str) -> FileContentResponse:
        url_path = f"{path.rstrip('/')}/{filename}" if path else filename

        try:
            await self.github_client.delete_file(repo, path, filename, message)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ResourceNotFoundError(f"Файл '{url_path}' не найден в репозитории '{repo}'")
            raise GitHubAPIError(f"GitHub API error: {e.response.text}", status_code=e.response.status_code)

        return FileContentResponse(path=url_path, content="", encoding="utf-8")

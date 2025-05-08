# app/infrastructure/github_client.py

import base64
import httpx
from app.core.config import MY_GITHUB_TOKEN, MY_GITHUB_USERNAME

class GitHubClient:
    """
    Клиент для работы с GitHub API.

    Предоставляет методы для CRUD-файлов и получения структуры репозитория.
    """
    def __init__(self):
        """
        Инициализация GitHub клиента с базовым URL и заголовками.
        """
        self.base_url = "https://api.github.com"
        self.headers = {"Authorization": f"Bearer {MY_GITHUB_TOKEN}"}

    async def get_repo_info(self, repo: str) -> dict:
        """
        Получение мета-информации о репозитории (включая default_branch).

        Args:
            repo (str): Имя репозитория.

        Returns:
            dict: Полная информация о репозитории.
        """
        url = f"{self.base_url}/repos/{MY_GITHUB_USERNAME}/{repo}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    async def list_branches(self, repo: str) -> list:
        """
        Получение списка веток репозитория.

        Args:
            repo (str): Имя репозитория GitHub.

        Returns:
            list: Список веток (имя, SHA и т.д.).
        """
        url = f"{self.base_url}/repos/{MY_GITHUB_USERNAME}/{repo}/branches"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    async def list_repo_tree(self, repo: str) -> list:
        """
        Получение полного дерева файлов и папок репозитория рекурсивно.

        Args:
            repo (str): Имя репозитория.

        Returns:
            list: Список узлов дерева (type="blob" для файлов, "tree" для папок).
        """
        repo_info = await self.get_repo_info(repo)
        branch = repo_info.get("default_branch", "main")

        url = (
            f"{self.base_url}/repos/"
            f"{MY_GITHUB_USERNAME}/{repo}/git/trees/{branch}"
            "?recursive=1"
        )
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        return data.get("tree", [])

    async def get_file_content(self, repo: str, path: str) -> dict:
        ...

    async def create_file(self, repo: str, path: str, filename: str, content: str, message: str) -> dict:
        ...

    async def update_file(self, repo: str, path: str, filename: str, content: str, message: str) -> dict:
        ...

    async def delete_file(self, repo: str, path: str, filename: str, message: str) -> dict:
        ...

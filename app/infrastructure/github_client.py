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
        url = f"{self.base_url}/repos/{MY_GITHUB_USERNAME}/{repo}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    async def list_branches(self, repo: str) -> list:
        url = f"{self.base_url}/repos/{MY_GITHUB_USERNAME}/{repo}/branches"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    async def list_commits(self, repo: str, path: str = None) -> list:
        url = f"{self.base_url}/repos/{MY_GITHUB_USERNAME}/{repo}/commits"
        if path:
            url += f"?path={path}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    async def list_pull_requests(self, repo: str) -> list:
        url = f"{self.base_url}/repos/{MY_GITHUB_USERNAME}/{repo}/pulls"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    async def list_issues(self, repo: str) -> list:
        url = f"{self.base_url}/repos/{MY_GITHUB_USERNAME}/{repo}/issues"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    async def list_repo_tree(self, repo: str) -> list:
        repo_info = await self.get_repo_info(repo)
        branch = repo_info.get("default_branch", "main")
        url = f"{self.base_url}/repos/{MY_GITHUB_USERNAME}/{repo}/git/trees/{branch}?recursive=1"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        return data.get("tree", [])

    async def get_file_content(self, repo: str, path: str) -> dict:
        url = f"{self.base_url}/repos/{MY_GITHUB_USERNAME}/{repo}/contents/{path}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    async def create_file(self, repo: str, path: str, filename: str, content: str, message: str) -> dict:
        encoded_content = base64.b64encode(content.encode("utf-8")).decode("ascii")
        url_path = f"{path.rstrip('/')}/{filename}" if path else filename
        url = f"{self.base_url}/repos/{MY_GITHUB_USERNAME}/{repo}/contents/{url_path}"
        data = {"message": message, "content": encoded_content}
        async with httpx.AsyncClient() as client:
            response = await client.put(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()

    async def update_file(self, repo: str, path: str, filename: str, content: str, message: str) -> dict:
        url_path = f"{path.rstrip('/')}/{filename}" if path else filename
        existing = await self.get_file_content(repo, url_path)
        sha = existing["sha"]
        encoded = base64.b64encode(content.encode("utf-8")).decode("ascii")
        url = f"{self.base_url}/repos/{MY_GITHUB_USERNAME}/{repo}/contents/{url_path}"
        data = {"message": message, "content": encoded, "sha": sha}
        async with httpx.AsyncClient() as client:
            response = await client.put(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()

    async def delete_file(self, repo: str, path: str, filename: str, message: str) -> dict:
        url_path = f"{path.rstrip('/')}/{filename}" if path else filename
        existing = await self.get_file_content(repo, url_path)
        sha = existing["sha"]
        url = f"{self.base_url}/repos/{MY_GITHUB_USERNAME}/{repo}/contents/{url_path}"
        payload = {"message": message, "sha": sha}
        async with httpx.AsyncClient() as client:
            response = await client.request("DELETE", url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()
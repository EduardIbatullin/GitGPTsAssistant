from app.infrastructure.github_client import GitHubClient
from app.core.exceptions import GitHubAPIError

class GitInfoService:
    def __init__(self, github_client: GitHubClient):
        self.github_client = github_client

    async def list_branches(self, repo: str) -> list:
        """
        Получает список веток указанного репозитория через GitHub API.

        Args:
            repo (str): Название репозитория GitHub.

        Returns:
            list: Список словарей с информацией о ветках.
        """
        try:
            return await self.github_client.list_branches(repo)
        except Exception as e:
            raise GitHubAPIError(str(e), status_code=500)

    async def list_commits(self, repo: str, path: str = None) -> list:
        """
        Получает список коммитов по репозиторию или конкретному пути.

        Args:
            repo (str): Название репозитория.
            path (str, optional): Путь к файлу или директории.

        Returns:
            list: Список словарей с информацией о коммитах.
        """
        try:
            return await self.github_client.list_commits(repo, path)
        except Exception as e:
            raise GitHubAPIError(str(e), status_code=500)

    async def list_pull_requests(self, repo: str) -> list:
        """
        Получает список pull requests из указанного репозитория.

        Args:
            repo (str): Название репозитория.

        Returns:
            list: Список pull requests.
        """
        try:
            return await self.github_client.list_pull_requests(repo)
        except Exception as e:
            raise GitHubAPIError(str(e), status_code=500)

    async def list_issues(self, repo: str) -> list:
        """
        Получает список issues из указанного репозитория.

        Args:
            repo (str): Название репозитория.

        Returns:
            list: Список issues.
        """
        try:
            return await self.github_client.list_issues(repo)
        except Exception as e:
            raise GitHubAPIError(str(e), status_code=500)
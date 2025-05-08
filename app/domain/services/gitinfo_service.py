from app.infrastructure.github_client import GitHubClient

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
        return await self.github_client.list_branches(repo)
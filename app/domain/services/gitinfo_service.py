from app.infrastructure.github_client import GitHubClient

class GitInfoService:
    def __init__(self, github_client: GitHubClient):
        self.github_client = github_client

    async def list_branches(self, repo: str) -> list:
        return await self.github_client.list_branches(repo)
# app/api/dependencies.py

from fastapi import Depends
from app.infrastructure.github_client import GitHubClient
from app.domain.services.file_service import FileService

def get_github_client() -> GitHubClient:
    """
    Функция для инъекции зависимости GitHub клиента.
    
    Возвращает экземпляр GitHubClient, который используется для взаимодействия
    с API GitHub.

    Returns:
        GitHubClient: Экземпляр клиента для работы с GitHub API.
    """
    return GitHubClient()

def get_file_service(
    client: GitHubClient = Depends(get_github_client),
) -> FileService:
    """
    Функция для инъекции зависимости GitHub сервиса (FileService).

    Returns:
        FileService: Экземпляр сервиса для работы с GitHub API.
    """
    return FileService(client)

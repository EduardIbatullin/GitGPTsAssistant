# app/domain/models.py

from pydantic import BaseModel, Field
from typing import List, Optional

class RepoStructureResponse(BaseModel):
    """
    Ответ с информацией о структуре репозитория.

    Attributes:
        repo (str): Имя репозитория.
        tree (list): Список файлов и папок в репозитории.
    """
    repo: str
    tree: list

class FileContentResponse(BaseModel):
    """
    Ответ с содержимым файла в репозитории.

    Attributes:
        path (str): Путь к файлу.
        content (str): Содержимое файла.
        encoding (str): Кодировка файла.
    """
    path: str
    content: str
    encoding: str

class CreateFileRequest(BaseModel):
    """
    Запрос для создания нового файла в репозитории.

    Attributes:
        path (str): Путь к папке в репозитории.
        filename (str): Имя файла.
        content (str): Содержимое файла.
        message (str): Сообщение коммита.
    """
    path: str
    filename: str
    content: str
    message: str

class UpdateFileRequest(BaseModel):
    """
    Запрос для обновления существующего файла в репозитории.

    Attributes:
        path (str): Путь к папке в репозитории.
        filename (str): Имя файла.
        content (str): Новое содержимое файла.
        message (str): Сообщение коммита.
    """
    path: str
    filename: str
    content: str
    message: str

class DeleteFileRequest(BaseModel):
    """
    Запрос для удаления файла из репозитория.

    Attributes:
        path (str): Путь к папке в репозитории.
        filename (str): Имя файла.
        message (str): Сообщение коммита.
    """
    path: str
    filename: str
    message: str

# ===== Git Metadata Models =====

class BranchResponse(BaseModel):
    """
    Модель ответа для ветки репозитория.

    Attributes:
        name (str): Название ветки.
        commit_sha (str): SHA последнего коммита.
    """
    name: str
    commit_sha: str = Field(..., alias="commit.sha")

class CommitAuthor(BaseModel):
    """
    Модель автора коммита.

    Attributes:
        name (str): Имя автора.
        email (str): Email автора.
        date (str): Дата коммита.
    """
    name: str
    email: str
    date: str

class CommitInfo(BaseModel):
    """
    Информация о коммите.

    Attributes:
        message (str): Сообщение коммита.
        author (CommitAuthor): Автор коммита.
    """
    message: str
    author: CommitAuthor

class CommitResponse(BaseModel):
    """
    Модель ответа для коммита.

    Attributes:
        sha (str): SHA хеша коммита.
        commit (CommitInfo): Информация о коммите.
    """
    sha: str
    commit: CommitInfo

class PullRequestResponse(BaseModel):
    """
    Модель ответа для Pull Request.

    Attributes:
        id (int): Идентификатор Pull Request.
        title (str): Заголовок PR.
        state (str): Статус (open/closed).
        html_url (str): Ссылка на PR.
    """
    id: int
    title: str
    state: str
    html_url: str

class IssueResponse(BaseModel):
    """
    Модель ответа для Issue.

    Attributes:
        id (int): Идентификатор Issue.
        title (str): Заголовок Issue.
        state (str): Статус (open/closed).
        html_url (str): Ссылка на Issue.
    """
    id: int
    title: str
    state: str
    html_url: str

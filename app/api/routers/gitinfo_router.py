from fastapi import APIRouter, Depends, Query
from typing import List, Annotated

from app.api.dependencies import get_github_client
from app.domain.services.gitinfo_service import GitInfoService
from app.domain.models import (
    BranchResponse,
    CommitResponse,
    PullRequestResponse,
    IssueResponse
)

router = APIRouter()

@router.get("/repos/{repo}/branches", response_model=List[BranchResponse])
async def get_branches(
    repo: str,
    service: GitInfoService = Depends(get_github_client)
) -> List[BranchResponse]:
    return await service.list_branches(repo)

@router.get("/repos/{repo}/commits", response_model=List[CommitResponse])
async def get_commits(
    repo: str,
    path: Annotated[str | None, Query()] = None,
    service: GitInfoService = Depends(get_github_client)
) -> List[CommitResponse]:
    return await service.list_commits(repo, path)

@router.get("/repos/{repo}/pulls", response_model=List[PullRequestResponse])
async def get_pull_requests(
    repo: str,
    service: GitInfoService = Depends(get_github_client)
) -> List[PullRequestResponse]:
    return await service.list_pull_requests(repo)

@router.get("/repos/{repo}/issues", response_model=List[IssueResponse])
async def get_issues(
    repo: str,
    service: GitInfoService = Depends(get_github_client)
) -> List[IssueResponse]:
    return await service.list_issues(repo)
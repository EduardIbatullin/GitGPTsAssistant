from fastapi import APIRouter, Depends, HTTPException, Query
from app.domain.services.gitinfo_service import GitInfoService
from app.api.dependencies import get_github_client

router = APIRouter()

@router.get("/repos/{repo}/branches", tags=["Git Metadata"])
async def get_branches(repo: str, service: GitInfoService = Depends(get_github_client)):
    try:
        return await service.list_branches(repo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/repos/{repo}/commits", tags=["Git Metadata"])
async def get_commits(repo: str, path: str = Query(None), service: GitInfoService = Depends(get_github_client)):
    try:
        return await service.list_commits(repo, path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/repos/{repo}/pulls", tags=["Git Metadata"])
async def get_pull_requests(repo: str, service: GitInfoService = Depends(get_github_client)):
    try:
        return await service.list_pull_requests(repo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/repos/{repo}/issues", tags=["Git Metadata"])
async def get_issues(repo: str, service: GitInfoService = Depends(get_github_client)):
    try:
        return await service.list_issues(repo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
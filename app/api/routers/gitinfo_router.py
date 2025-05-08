from fastapi import APIRouter, Depends, HTTPException
from app.domain.services.gitinfo_service import GitInfoService
from app.api.dependencies import get_github_client

router = APIRouter()

@router.get("/repos/{repo}/branches", tags=["Git Metadata"])
async def get_branches(repo: str, service: GitInfoService = Depends(get_github_client)):
    try:
        return await service.list_branches(repo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
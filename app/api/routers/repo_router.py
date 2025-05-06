# app/api/routers/repo_router.py

from fastapi import APIRouter, Depends
from app.domain.services.file_service import FileService
from app.domain.models import (
    RepoStructureResponse,
    FileContentResponse,
    CreateFileRequest,
    UpdateFileRequest,
    DeleteFileRequest,
)
from app.api.dependencies import get_file_service

router = APIRouter()

@router.get("/repos/{repo}/structure", response_model=RepoStructureResponse)
async def get_repo_structure(
    repo: str, 
    file_service: FileService = Depends(get_file_service)
) -> RepoStructureResponse:
    structure = await file_service.get_repo_structure(repo)
    return RepoStructureResponse(repo=repo, tree=structure)

@router.get("/repos/{repo}/file", response_model=FileContentResponse)
async def get_file_content(
    repo: str, 
    path: str, 
    file_service: FileService = Depends(get_file_service)
) -> FileContentResponse:
    return await file_service.get_file_content(repo, path)

@router.post("/repos/{repo}/file", response_model=FileContentResponse)
async def create_new_file(
    repo: str, 
    file_data: CreateFileRequest, 
    file_service: FileService = Depends(get_file_service)
) -> FileContentResponse:
    return await file_service.create_file(
        repo,
        file_data.path,
        file_data.filename,
        file_data.content,
        file_data.message,
    )

@router.put("/repos/{repo}/file", response_model=FileContentResponse)
async def update_file(
    repo: str,
    file_data: UpdateFileRequest,
    file_service: FileService = Depends(get_file_service)
) -> FileContentResponse:
    return await file_service.update_file(
        repo,
        file_data.path,
        file_data.filename,
        file_data.content,
        file_data.message,
    )

@router.delete("/repos/{repo}/file", response_model=FileContentResponse)
async def delete_file(
    repo: str,
    file_data: DeleteFileRequest,
    file_service: FileService = Depends(get_file_service)
) -> FileContentResponse:
    return await file_service.delete_file(
        repo,
        file_data.path,
        file_data.filename,
        file_data.message,
    )

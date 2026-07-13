from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.core.database import get_database
from app.repositories.source_repository import SourceRepository
from app.services.source_service import SourceService
from app.models.sources import SourceCreate, SourceUpdate, SourceResponse

router = APIRouter(prefix="/sources", tags=["Sources"])


def get_source_service(db=Depends(get_database)) -> SourceService:
    return SourceService(SourceRepository(db))


@router.post("/", response_model=SourceResponse, status_code=201)
async def create_source(
    payload: SourceCreate,
    service: SourceService = Depends(get_source_service),
):
    """Create a new source (chapter/episode citation)."""
    return await service.create_source(payload)


@router.get("/", response_model=List[SourceResponse])
async def list_sources(service: SourceService = Depends(get_source_service)):
    """List all sources."""
    return await service.list_sources()


@router.get("/{source_id}", response_model=SourceResponse)
async def get_source(
    source_id: str,
    service: SourceService = Depends(get_source_service),
):
    """Get a single source by id."""
    source = await service.get_source(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@router.patch("/{source_id}", response_model=SourceResponse)
async def update_source(
    source_id: str,
    payload: SourceUpdate,
    service: SourceService = Depends(get_source_service),
):
    """Update an existing source. Only send fields you want to change."""
    source = await service.update_source(source_id, payload)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@router.delete("/{source_id}", status_code=204)
async def delete_source(
    source_id: str,
    service: SourceService = Depends(get_source_service),
):
    """Delete a source."""
    deleted = await service.delete_source(source_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Source not found")
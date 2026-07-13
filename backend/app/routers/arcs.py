from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.core.database import get_database
from app.repositories.arc_repository import ArcRepository
from app.services.arc_service import ArcService
from app.models.arcs import ArcCreate, ArcUpdate, ArcResponse

router = APIRouter(prefix="/arcs", tags=["Arcs"])


def get_arc_service(db=Depends(get_database)) -> ArcService:
    return ArcService(ArcRepository(db))


@router.post("/", response_model=ArcResponse, status_code=201)
async def create_arc(
    payload: ArcCreate,
    service: ArcService = Depends(get_arc_service),
):
    """Create a new story arc."""
    return await service.create_arc(payload)


@router.get("/", response_model=List[ArcResponse])
async def list_arcs(service: ArcService = Depends(get_arc_service)):
    """List all arcs, ordered by their timeline sequence."""
    return await service.list_arcs()


@router.get("/{arc_id}", response_model=ArcResponse)
async def get_arc(
    arc_id: str,
    service: ArcService = Depends(get_arc_service),
):
    """Get a single arc by id."""
    arc = await service.get_arc(arc_id)
    if not arc:
        raise HTTPException(status_code=404, detail="Arc not found")
    return arc


@router.patch("/{arc_id}", response_model=ArcResponse)
async def update_arc(
    arc_id: str,
    payload: ArcUpdate,
    service: ArcService = Depends(get_arc_service),
):
    """Update an existing arc. Only send fields you want to change."""
    arc = await service.update_arc(arc_id, payload)
    if not arc:
        raise HTTPException(status_code=404, detail="Arc not found")
    return arc


@router.delete("/{arc_id}", status_code=204)
async def delete_arc(
    arc_id: str,
    service: ArcService = Depends(get_arc_service),
):
    """Delete an arc."""
    deleted = await service.delete_arc(arc_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Arc not found")
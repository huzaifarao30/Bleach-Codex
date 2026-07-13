from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from app.core.database import get_database
from app.repositories.lore_event_repository import LoreEventRepository
from app.repositories.source_repository import SourceRepository
from app.services.lore_event_service import LoreEventService
from app.models.lore_events import LoreEventCreate, LoreEventUpdate, LoreEventResponse, LoreEventStatus

router = APIRouter(prefix="/lore-events", tags=["Lore Events"])


def get_lore_event_service(db=Depends(get_database)) -> LoreEventService:
    return LoreEventService(LoreEventRepository(db), SourceRepository(db))


@router.post("/", response_model=LoreEventResponse, status_code=201)
async def create_lore_event(
    payload: LoreEventCreate,
    service: LoreEventService = Depends(get_lore_event_service),
):
    """Create a new lore event (foreshadowing hint, payoff, or contradiction)."""
    return await service.create_lore_event(payload)


@router.get("/", response_model=List[LoreEventResponse])
async def list_lore_events(
    status: Optional[LoreEventStatus] = Query(default=None, description="Filter by review status."),
    service: LoreEventService = Depends(get_lore_event_service),
):
    """List all lore events, optionally filtered by review status (for the Plot Hole Tracker)."""
    if status:
        return await service.list_lore_events_by_status(status)
    return await service.list_lore_events()


@router.get("/{event_id}", response_model=LoreEventResponse)
async def get_lore_event(
    event_id: str,
    service: LoreEventService = Depends(get_lore_event_service),
):
    """Get a single lore event by id, with sources resolved."""
    event = await service.get_lore_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Lore event not found")
    return event


@router.patch("/{event_id}", response_model=LoreEventResponse)
async def update_lore_event(
    event_id: str,
    payload: LoreEventUpdate,
    service: LoreEventService = Depends(get_lore_event_service),
):
    """Update an existing lore event. Only send fields you want to change."""
    event = await service.update_lore_event(event_id, payload)
    if not event:
        raise HTTPException(status_code=404, detail="Lore event not found")
    return event


@router.delete("/{event_id}", status_code=204)
async def delete_lore_event(
    event_id: str,
    service: LoreEventService = Depends(get_lore_event_service),
):
    """Delete a lore event."""
    deleted = await service.delete_lore_event(event_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Lore event not found")
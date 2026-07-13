from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.core.database import get_database
from app.repositories.power_repository import PowerRepository
from app.services.power_service import PowerService
from app.models.powers import PowerCreate, PowerUpdate, PowerResponse

router = APIRouter(prefix="/powers", tags=["Powers"])


def get_power_service(db=Depends(get_database)) -> PowerService:
    return PowerService(PowerRepository(db))


@router.post("/", response_model=PowerResponse, status_code=201)
async def create_power(
    payload: PowerCreate,
    service: PowerService = Depends(get_power_service),
):
    """Create a new power for a character."""
    return await service.create_power(payload)


@router.get("/", response_model=List[PowerResponse])
async def list_powers(service: PowerService = Depends(get_power_service)):
    """List all powers."""
    return await service.list_powers()


@router.get("/character/{character_id}", response_model=List[PowerResponse])
async def list_powers_for_character(
    character_id: str,
    service: PowerService = Depends(get_power_service),
):
    """List all powers belonging to a specific character."""
    return await service.list_powers_for_character(character_id)


@router.get("/{power_id}", response_model=PowerResponse)
async def get_power(
    power_id: str,
    service: PowerService = Depends(get_power_service),
):
    """Get a single power by id."""
    power = await service.get_power(power_id)
    if not power:
        raise HTTPException(status_code=404, detail="Power not found")
    return power


@router.patch("/{power_id}", response_model=PowerResponse)
async def update_power(
    power_id: str,
    payload: PowerUpdate,
    service: PowerService = Depends(get_power_service),
):
    """Update an existing power. Only send fields you want to change."""
    power = await service.update_power(power_id, payload)
    if not power:
        raise HTTPException(status_code=404, detail="Power not found")
    return power


@router.delete("/{power_id}", status_code=204)
async def delete_power(
    power_id: str,
    service: PowerService = Depends(get_power_service),
):
    """Delete a power."""
    deleted = await service.delete_power(power_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Power not found")
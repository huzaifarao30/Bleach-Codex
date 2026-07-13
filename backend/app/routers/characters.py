from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.core.database import get_database
from app.repositories.character_repository import CharacterRepository
from app.repositories.power_repository import PowerRepository
from app.repositories.relationship_repository import RelationshipRepository
from app.repositories.arc_repository import ArcRepository
from app.services.character_service import CharacterService
from app.services.character_profile_service import CharacterProfileService
from app.models.character import CharacterCreate, CharacterUpdate, CharacterResponse

router = APIRouter(prefix="/characters", tags=["Characters"])


def get_character_service(db=Depends(get_database)) -> CharacterService:
    return CharacterService(CharacterRepository(db))


def get_character_profile_service(db=Depends(get_database)) -> CharacterProfileService:
    return CharacterProfileService(
        CharacterRepository(db),
        PowerRepository(db),
        RelationshipRepository(db),
        ArcRepository(db),
    )


@router.post("/", response_model=CharacterResponse, status_code=201)
async def create_character(
    payload: CharacterCreate,
    service: CharacterService = Depends(get_character_service),
):
    """Create a new character."""
    return await service.create_character(payload)


@router.get("/", response_model=List[CharacterResponse])
async def list_characters(service: CharacterService = Depends(get_character_service)):
    """List all characters."""
    return await service.list_characters()


@router.get("/{character_id}/full")
async def get_character_full_profile(
    character_id: str,
    service: CharacterProfileService = Depends(get_character_profile_service),
):
    """
    Full character page in one call: bio + powers + relationships (with
    connected character names resolved) + arcs. Built for the frontend
    character detail page — avoids needing 3+ separate requests.
    """
    profile = await service.get_full_profile(character_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Character not found")
    return profile


@router.get("/{character_id}", response_model=CharacterResponse)
async def get_character(
    character_id: str,
    service: CharacterService = Depends(get_character_service),
):
    """Get a single character by id."""
    character = await service.get_character(character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character


@router.patch("/{character_id}", response_model=CharacterResponse)
async def update_character(
    character_id: str,
    payload: CharacterUpdate,
    service: CharacterService = Depends(get_character_service),
):
    """Update an existing character. Only send fields you want to change."""
    character = await service.update_character(character_id, payload)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character


@router.post("/{character_id}/arcs/{arc_id}", response_model=CharacterResponse)
async def link_arc_to_character(
    character_id: str,
    arc_id: str,
    service: CharacterService = Depends(get_character_service),
):
    """
    Links an arc to a character (adds arc_id to the character's arc_ids).
    This is the missing piece that makes a character's 'Arc Appearances'
    section actually populate — without calling this, arc_ids stays empty
    even after the arc itself exists.
    """
    character = await service.add_arc(character_id, arc_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character


@router.delete("/{character_id}", status_code=204)
async def delete_character(
    character_id: str,
    service: CharacterService = Depends(get_character_service),
):
    """Delete a character."""
    deleted = await service.delete_character(character_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Character not found")
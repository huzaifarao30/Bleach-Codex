from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.core.database import get_database
from app.repositories.relationship_repository import RelationshipRepository
from app.services.relationship_service import RelationshipService
from app.models.relationships import RelationshipCreate, RelationshipUpdate, RelationshipResponse

router = APIRouter(prefix="/relationships", tags=["Relationships"])


def get_relationship_service(db=Depends(get_database)) -> RelationshipService:
    return RelationshipService(RelationshipRepository(db))


@router.post("/", response_model=RelationshipResponse, status_code=201)
async def create_relationship(
    payload: RelationshipCreate,
    service: RelationshipService = Depends(get_relationship_service),
):
    """Create a new relationship edge between two characters."""
    return await service.create_relationship(payload)


@router.get("/", response_model=List[RelationshipResponse])
async def list_relationships(service: RelationshipService = Depends(get_relationship_service)):
    """List all relationship edges."""
    return await service.list_relationships()


@router.get("/character/{character_id}", response_model=List[RelationshipResponse])
async def list_relationships_for_character(
    character_id: str,
    service: RelationshipService = Depends(get_relationship_service),
):
    """List all relationships involving a specific character (either side of the edge)."""
    return await service.list_relationships_for_character(character_id)


@router.get("/{relationship_id}", response_model=RelationshipResponse)
async def get_relationship(
    relationship_id: str,
    service: RelationshipService = Depends(get_relationship_service),
):
    """Get a single relationship by id."""
    relationship = await service.get_relationship(relationship_id)
    if not relationship:
        raise HTTPException(status_code=404, detail="Relationship not found")
    return relationship


@router.patch("/{relationship_id}", response_model=RelationshipResponse)
async def update_relationship(
    relationship_id: str,
    payload: RelationshipUpdate,
    service: RelationshipService = Depends(get_relationship_service),
):
    """Update an existing relationship. Only send fields you want to change."""
    relationship = await service.update_relationship(relationship_id, payload)
    if not relationship:
        raise HTTPException(status_code=404, detail="Relationship not found")
    return relationship


@router.delete("/{relationship_id}", status_code=204)
async def delete_relationship(
    relationship_id: str,
    service: RelationshipService = Depends(get_relationship_service),
):
    """Delete a relationship."""
    deleted = await service.delete_relationship(relationship_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Relationship not found")
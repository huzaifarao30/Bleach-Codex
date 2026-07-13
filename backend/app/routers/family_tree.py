from fastapi import APIRouter, Depends, Query
from app.core.database import get_database
from app.repositories.character_repository import CharacterRepository
from app.repositories.relationship_repository import RelationshipRepository
from app.services.family_tree_service import FamilyTreeService

router = APIRouter(prefix="/family-tree", tags=["Family Tree"])


def get_family_tree_service(db=Depends(get_database)) -> FamilyTreeService:
    return FamilyTreeService(CharacterRepository(db), RelationshipRepository(db))


@router.get("/{character_id}")
async def get_family_tree(
    character_id: str,
    depth: int = Query(default=2, ge=1, le=5, description="How many relationship hops out from the root character to include."),
    service: FamilyTreeService = Depends(get_family_tree_service),
):
    """
    Build a graph (nodes + edges) centered on the given character, walking outward
    through relationships up to `depth` hops. Powers the interactive family tree UI.
    """
    return await service.get_family_tree(character_id, max_depth=depth)
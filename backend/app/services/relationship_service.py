from typing import Optional, List
from app.repositories.relationship_repository import RelationshipRepository
from app.models.relationships import RelationshipCreate, RelationshipUpdate, RelationshipResponse


class RelationshipService:
    """
    Business logic for relationships (family-tree edges).
    Routers call this — never the repository directly.
    """

    def __init__(self, repository: RelationshipRepository):
        self.repository = repository

    async def create_relationship(self, payload: RelationshipCreate) -> RelationshipResponse:
        doc = payload.model_dump()
        created = await self.repository.create(doc)
        return RelationshipResponse(**created)

    async def get_relationship(self, relationship_id: str) -> Optional[RelationshipResponse]:
        doc = await self.repository.get_by_id(relationship_id)
        return RelationshipResponse(**doc) if doc else None

    async def list_relationships(self) -> List[RelationshipResponse]:
        docs = await self.repository.list_all()
        return [RelationshipResponse(**doc) for doc in docs]

    async def list_relationships_for_character(self, character_id: str) -> List[RelationshipResponse]:
        docs = await self.repository.list_for_character(character_id)
        return [RelationshipResponse(**doc) for doc in docs]

    async def update_relationship(self, relationship_id: str, payload: RelationshipUpdate) -> Optional[RelationshipResponse]:
        update_data = payload.model_dump(exclude_none=True)
        if not update_data:
            return await self.get_relationship(relationship_id)
        doc = await self.repository.update(relationship_id, update_data)
        return RelationshipResponse(**doc) if doc else None

    async def delete_relationship(self, relationship_id: str) -> bool:
        return await self.repository.delete(relationship_id)
from typing import Optional, List
from app.repositories.character_repository import CharacterRepository
from app.models.character import CharacterCreate, CharacterUpdate, CharacterResponse


class CharacterService:
    """
    Business logic for characters. Routers call this — never the repository directly.
    This is where validation-beyond-schema, orchestration, or future business rules live
    (e.g. 'don't allow deleting a character who still has linked powers' would go here).
    """

    def __init__(self, repository: CharacterRepository):
        self.repository = repository

    async def create_character(self, payload: CharacterCreate) -> CharacterResponse:
        doc = payload.model_dump()
        doc["arc_ids"] = []
        doc["source_ids"] = []
        created = await self.repository.create(doc)
        return CharacterResponse(**created)

    async def get_character(self, character_id: str) -> Optional[CharacterResponse]:
        doc = await self.repository.get_by_id(character_id)
        return CharacterResponse(**doc) if doc else None

    async def list_characters(self) -> List[CharacterResponse]:
        docs = await self.repository.list_all()
        return [CharacterResponse(**doc) for doc in docs]

    async def update_character(self, character_id: str, payload: CharacterUpdate) -> Optional[CharacterResponse]:
        update_data = payload.model_dump(exclude_none=True)
        if not update_data:
            return await self.get_character(character_id)
        doc = await self.repository.update(character_id, update_data)
        return CharacterResponse(**doc) if doc else None

    async def delete_character(self, character_id: str) -> bool:
        return await self.repository.delete(character_id)

    async def add_arc(self, character_id: str, arc_id: str) -> Optional[CharacterResponse]:
        """Links an arc to a character (appends to arc_ids, no duplicates)."""
        character = await self.repository.get_by_id(character_id)
        if not character:
            return None
        arc_ids = character.get("arc_ids", [])
        if arc_id not in arc_ids:
            arc_ids.append(arc_id)
        doc = await self.repository.update(character_id, {"arc_ids": arc_ids})
        return CharacterResponse(**doc) if doc else None
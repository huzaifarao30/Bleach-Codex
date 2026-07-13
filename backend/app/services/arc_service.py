from typing import Optional, List
from app.repositories.arc_repository import ArcRepository
from app.models.arcs import ArcCreate, ArcUpdate, ArcResponse


class ArcService:
    """
    Business logic for arcs. Routers call this — never the repository directly.
    """

    def __init__(self, repository: ArcRepository):
        self.repository = repository

    async def create_arc(self, payload: ArcCreate) -> ArcResponse:
        doc = payload.model_dump()
        doc["character_ids"] = []
        created = await self.repository.create(doc)
        return ArcResponse(**created)

    async def get_arc(self, arc_id: str) -> Optional[ArcResponse]:
        doc = await self.repository.get_by_id(arc_id)
        return ArcResponse(**doc) if doc else None

    async def list_arcs(self) -> List[ArcResponse]:
        docs = await self.repository.list_all()
        return [ArcResponse(**doc) for doc in docs]

    async def update_arc(self, arc_id: str, payload: ArcUpdate) -> Optional[ArcResponse]:
        update_data = payload.model_dump(exclude_none=True)
        if not update_data:
            return await self.get_arc(arc_id)
        doc = await self.repository.update(arc_id, update_data)
        return ArcResponse(**doc) if doc else None

    async def delete_arc(self, arc_id: str) -> bool:
        return await self.repository.delete(arc_id)
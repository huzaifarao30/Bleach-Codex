from typing import Optional, List
from app.repositories.source_repository import SourceRepository
from app.models.sources import SourceCreate, SourceUpdate, SourceResponse


class SourceService:
    """
    Business logic for sources. Routers call this — never the repository directly.
    """

    def __init__(self, repository: SourceRepository):
        self.repository = repository

    async def create_source(self, payload: SourceCreate) -> SourceResponse:
        doc = payload.model_dump()
        created = await self.repository.create(doc)
        return SourceResponse(**created)

    async def get_source(self, source_id: str) -> Optional[SourceResponse]:
        doc = await self.repository.get_by_id(source_id)
        return SourceResponse(**doc) if doc else None

    async def list_sources(self) -> List[SourceResponse]:
        docs = await self.repository.list_all()
        return [SourceResponse(**doc) for doc in docs]

    async def update_source(self, source_id: str, payload: SourceUpdate) -> Optional[SourceResponse]:
        update_data = payload.model_dump(exclude_none=True)
        if not update_data:
            return await self.get_source(source_id)
        doc = await self.repository.update(source_id, update_data)
        return SourceResponse(**doc) if doc else None

    async def delete_source(self, source_id: str) -> bool:
        return await self.repository.delete(source_id)
from typing import Optional, List
from app.repositories.lore_event_repository import LoreEventRepository
from app.repositories.source_repository import SourceRepository
from app.models.lore_events import LoreEventCreate, LoreEventUpdate, LoreEventResponse


class LoreEventService:
    """
    Business logic for lore events. Routers call this — never the repository directly.

    This service owns the Source<->LoreEvent join: whenever a lore event is
    returned, its source_ids are resolved into full source details via the
    SourceRepository, so the API response is ready to display without a
    second request from the frontend.
    """

    def __init__(self, repository: LoreEventRepository, source_repository: SourceRepository):
        self.repository = repository
        self.source_repository = source_repository

    async def _to_response(self, doc: dict) -> LoreEventResponse:
        sources = await self.source_repository.get_many_by_ids(doc.get("source_ids", []))
        return LoreEventResponse(**doc, sources=sources)

    async def create_lore_event(self, payload: LoreEventCreate) -> LoreEventResponse:
        doc = payload.model_dump()
        created = await self.repository.create(doc)
        return await self._to_response(created)

    async def get_lore_event(self, event_id: str) -> Optional[LoreEventResponse]:
        doc = await self.repository.get_by_id(event_id)
        return await self._to_response(doc) if doc else None

    async def list_lore_events(self) -> List[LoreEventResponse]:
        docs = await self.repository.list_all()
        return [await self._to_response(doc) for doc in docs]

    async def list_lore_events_by_status(self, status: str) -> List[LoreEventResponse]:
        docs = await self.repository.list_by_status(status)
        return [await self._to_response(doc) for doc in docs]

    async def update_lore_event(self, event_id: str, payload: LoreEventUpdate) -> Optional[LoreEventResponse]:
        update_data = payload.model_dump(exclude_none=True)
        if not update_data:
            return await self.get_lore_event(event_id)
        doc = await self.repository.update(event_id, update_data)
        return await self._to_response(doc) if doc else None

    async def delete_lore_event(self, event_id: str) -> bool:
        return await self.repository.delete(event_id)
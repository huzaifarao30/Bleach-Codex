from typing import Optional, List
from app.repositories.power_repository import PowerRepository
from app.models.powers import PowerCreate, PowerUpdate, PowerResponse


class PowerService:
    """
    Business logic for powers. Routers call this — never the repository directly.
    """

    def __init__(self, repository: PowerRepository):
        self.repository = repository

    async def create_power(self, payload: PowerCreate) -> PowerResponse:
        doc = payload.model_dump()
        doc["contradiction_ids"] = []
        created = await self.repository.create(doc)
        return PowerResponse(**created)

    async def get_power(self, power_id: str) -> Optional[PowerResponse]:
        doc = await self.repository.get_by_id(power_id)
        return PowerResponse(**doc) if doc else None

    async def list_powers(self) -> List[PowerResponse]:
        docs = await self.repository.list_all()
        return [PowerResponse(**doc) for doc in docs]

    async def list_powers_for_character(self, character_id: str) -> List[PowerResponse]:
        docs = await self.repository.list_for_character(character_id)
        return [PowerResponse(**doc) for doc in docs]

    async def update_power(self, power_id: str, payload: PowerUpdate) -> Optional[PowerResponse]:
        update_data = payload.model_dump(exclude_none=True)
        if not update_data:
            return await self.get_power(power_id)
        doc = await self.repository.update(power_id, update_data)
        return PowerResponse(**doc) if doc else None

    async def delete_power(self, power_id: str) -> bool:
        return await self.repository.delete(power_id)
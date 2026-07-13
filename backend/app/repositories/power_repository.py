from bson import ObjectId
from bson.errors import InvalidId
from typing import Optional, List


class PowerRepository:
    """
    Direct database access for the 'powers' collection.
    """

    def __init__(self, db):
        self.collection = db["powers"]

    async def create(self, power_data: dict) -> dict:
        result = await self.collection.insert_one(power_data)
        return await self.get_by_id(str(result.inserted_id))

    async def get_by_id(self, power_id: str) -> Optional[dict]:
        try:
            doc = await self.collection.find_one({"_id": ObjectId(power_id)})
        except InvalidId:
            return None
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def list_all(self) -> List[dict]:
        docs = []
        async for doc in self.collection.find():
            doc["_id"] = str(doc["_id"])
            docs.append(doc)
        return docs

    async def list_for_character(self, character_id: str) -> List[dict]:
        docs = []
        async for doc in self.collection.find({"character_id": character_id}):
            doc["_id"] = str(doc["_id"])
            docs.append(doc)
        return docs

    async def update(self, power_id: str, update_data: dict) -> Optional[dict]:
        try:
            await self.collection.update_one(
                {"_id": ObjectId(power_id)},
                {"$set": update_data},
            )
        except InvalidId:
            return None
        return await self.get_by_id(power_id)

    async def delete(self, power_id: str) -> bool:
        try:
            result = await self.collection.delete_one({"_id": ObjectId(power_id)})
        except InvalidId:
            return False
        return result.deleted_count == 1
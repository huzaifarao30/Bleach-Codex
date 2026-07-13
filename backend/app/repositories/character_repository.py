from bson import ObjectId
from bson.errors import InvalidId
from typing import Optional, List


class CharacterRepository:
    """
    Direct database access for the 'characters' collection.
    Services call this — nothing above this layer writes raw MongoDB queries.
    """

    def __init__(self, db):
        self.collection = db["characters"]

    async def create(self, character_data: dict) -> dict:
        result = await self.collection.insert_one(character_data)
        return await self.get_by_id(str(result.inserted_id))

    async def get_by_id(self, character_id: str) -> Optional[dict]:
        try:
            doc = await self.collection.find_one({"_id": ObjectId(character_id)})
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

    async def update(self, character_id: str, update_data: dict) -> Optional[dict]:
        try:
            await self.collection.update_one(
                {"_id": ObjectId(character_id)},
                {"$set": update_data},
            )
        except InvalidId:
            return None
        return await self.get_by_id(character_id)

    async def delete(self, character_id: str) -> bool:
        try:
            result = await self.collection.delete_one({"_id": ObjectId(character_id)})
        except InvalidId:
            return False
        return result.deleted_count == 1

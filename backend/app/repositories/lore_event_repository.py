from bson import ObjectId
from bson.errors import InvalidId
from typing import Optional, List


class LoreEventRepository:
    """
    Direct database access for the 'lore_events' collection
    (foreshadowing hints, payoffs, and contradictions).
    """

    def __init__(self, db):
        self.collection = db["lore_events"]

    async def create(self, event_data: dict) -> dict:
        result = await self.collection.insert_one(event_data)
        return await self.get_by_id(str(result.inserted_id))

    async def get_by_id(self, event_id: str) -> Optional[dict]:
        try:
            doc = await self.collection.find_one({"_id": ObjectId(event_id)})
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

    async def list_by_status(self, status: str) -> List[dict]:
        """
        Filter by review status (proposed / approved / rejected) — powers the
        Plot Hole Tracker's review workflow (e.g. 'show me only proposed contradictions
        awaiting my review').
        """
        docs = []
        async for doc in self.collection.find({"status": status}):
            doc["_id"] = str(doc["_id"])
            docs.append(doc)
        return docs

    async def update(self, event_id: str, update_data: dict) -> Optional[dict]:
        try:
            await self.collection.update_one(
                {"_id": ObjectId(event_id)},
                {"$set": update_data},
            )
        except InvalidId:
            return None
        return await self.get_by_id(event_id)

    async def delete(self, event_id: str) -> bool:
        try:
            result = await self.collection.delete_one({"_id": ObjectId(event_id)})
        except InvalidId:
            return False
        return result.deleted_count == 1
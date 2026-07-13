from bson import ObjectId
from bson.errors import InvalidId
from typing import Optional, List


class ArcRepository:
    """
    Direct database access for the 'arcs' collection.
    """

    def __init__(self, db):
        self.collection = db["arcs"]

    async def create(self, arc_data: dict) -> dict:
        result = await self.collection.insert_one(arc_data)
        return await self.get_by_id(str(result.inserted_id))

    async def get_by_id(self, arc_id: str) -> Optional[dict]:
        try:
            doc = await self.collection.find_one({"_id": ObjectId(arc_id)})
        except InvalidId:
            return None
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def list_all(self) -> List[dict]:
        docs = []
        # Sorted by order_index so the timeline always comes back in story order.
        async for doc in self.collection.find().sort("order_index", 1):
            doc["_id"] = str(doc["_id"])
            docs.append(doc)
        return docs

    async def update(self, arc_id: str, update_data: dict) -> Optional[dict]:
        try:
            await self.collection.update_one(
                {"_id": ObjectId(arc_id)},
                {"$set": update_data},
            )
        except InvalidId:
            return None
        return await self.get_by_id(arc_id)

    async def delete(self, arc_id: str) -> bool:
        try:
            result = await self.collection.delete_one({"_id": ObjectId(arc_id)})
        except InvalidId:
            return False
        return result.deleted_count == 1
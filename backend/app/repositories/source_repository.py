from bson import ObjectId
from bson.errors import InvalidId
from typing import Optional, List


class SourceRepository:
    """
    Direct database access for the 'sources' collection.
    """

    def __init__(self, db):
        self.collection = db["sources"]

    async def create(self, source_data: dict) -> dict:
        result = await self.collection.insert_one(source_data)
        return await self.get_by_id(str(result.inserted_id))

    async def get_by_id(self, source_id: str) -> Optional[dict]:
        try:
            doc = await self.collection.find_one({"_id": ObjectId(source_id)})
        except InvalidId:
            return None
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def get_many_by_ids(self, source_ids: List[str]) -> List[dict]:
        """
        Fetch multiple sources at once, given a list of ids.
        This is what powers the 'join' we discussed earlier — when a LoreEvent
        needs to show its full source details inline, this is how those get fetched.
        """
        object_ids = []
        for sid in source_ids:
            try:
                object_ids.append(ObjectId(sid))
            except InvalidId:
                continue
        docs = []
        async for doc in self.collection.find({"_id": {"$in": object_ids}}):
            doc["_id"] = str(doc["_id"])
            docs.append(doc)
        return docs

    async def list_all(self) -> List[dict]:
        docs = []
        async for doc in self.collection.find():
            doc["_id"] = str(doc["_id"])
            docs.append(doc)
        return docs

    async def update(self, source_id: str, update_data: dict) -> Optional[dict]:
        try:
            await self.collection.update_one(
                {"_id": ObjectId(source_id)},
                {"$set": update_data},
            )
        except InvalidId:
            return None
        return await self.get_by_id(source_id)

    async def delete(self, source_id: str) -> bool:
        try:
            result = await self.collection.delete_one({"_id": ObjectId(source_id)})
        except InvalidId:
            return False
        return result.deleted_count == 1
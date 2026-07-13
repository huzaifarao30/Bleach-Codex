from bson import ObjectId
from bson.errors import InvalidId
from typing import Optional, List


class RelationshipRepository:
    """
    Direct database access for the 'relationships' collection (family-tree edges).
    """

    def __init__(self, db):
        self.collection = db["relationships"]

    async def create(self, relationship_data: dict) -> dict:
        result = await self.collection.insert_one(relationship_data)
        return await self.get_by_id(str(result.inserted_id))

    async def get_by_id(self, relationship_id: str) -> Optional[dict]:
        try:
            doc = await self.collection.find_one({"_id": ObjectId(relationship_id)})
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
        """
        Every relationship where this character appears on either side.
        This is the building block the family-tree traversal will use.
        """
        docs = []
        cursor = self.collection.find({
            "$or": [
                {"character_a_id": character_id},
                {"character_b_id": character_id},
            ]
        })
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            docs.append(doc)
        return docs

    async def update(self, relationship_id: str, update_data: dict) -> Optional[dict]:
        try:
            await self.collection.update_one(
                {"_id": ObjectId(relationship_id)},
                {"$set": update_data},
            )
        except InvalidId:
            return None
        return await self.get_by_id(relationship_id)

    async def delete(self, relationship_id: str) -> bool:
        try:
            result = await self.collection.delete_one({"_id": ObjectId(relationship_id)})
        except InvalidId:
            return False
        return result.deleted_count == 1
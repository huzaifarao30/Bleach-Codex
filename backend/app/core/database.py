from pymongo import AsyncMongoClient
from app.core.config import settings


class Database:
    """
    Wraps a single MongoDB client/connection, shared across the whole app.
    Repositories pull collections from here rather than each opening their own connection.

    Uses PyMongo's native async API (AsyncMongoClient), not Motor — Motor is deprecated
    as of May 2026 in favor of asyncio support built directly into PyMongo itself.
    """

    client: AsyncMongoClient = None

    @classmethod
    def connect(cls):
        # Defaults (serverSelectionTimeoutMS=30000, connectTimeoutMS=20000) can be too
        # tight on a slower or less stable connection, especially right after uvicorn
        # --reload restarts and the client has to rediscover the whole Atlas replica
        # set from scratch. These are deliberately more generous.
        cls.client = AsyncMongoClient(
            settings.mongodb_uri,
            serverSelectionTimeoutMS=45000,
            connectTimeoutMS=30000,
            socketTimeoutMS=30000,
        )

    @classmethod
    def get_db(cls):
        if cls.client is None:
            cls.connect()
        return cls.client[settings.mongodb_db_name]

    @classmethod
    def close(cls):
        if cls.client is not None:
            cls.client.close()
            cls.client = None


def get_database():
    """Dependency-injectable accessor — routers/services call this, never touch Database directly."""
    return Database.get_db()
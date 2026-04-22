import logging
import os

from pymongo import AsyncMongoClient
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase

logger = logging.getLogger(__name__)

DB_URL = os.getenv("MONGODB_URL", "")
logger.info("DB URL %s", DB_URL)
DB_NAME = os.getenv("MONGODB_NAME", "woosterlab")


class MongoClientManager:
    def __init__(self):
        self.client: AsyncMongoClient | None = None
        self.db: AsyncDatabase | None = None

    async def init_db(self):
        """Get database and confirm available

        Raises:
            Exception: issues connecting to mongo
        """
        try:
            self.client = AsyncMongoClient(DB_URL)
            self.db = self.client.get_database(DB_NAME)
            ping_response = await self.db.command("ping")

            if int(ping_response["ok"]) != 1:
                raise Exception("Problem connecting to database")
            else:
                logger.debug("Connected to database")

        except Exception as error:
            logger.error("unable to load/connect to database")
            raise

    async def close(self):
        self.client.close()


db_client = MongoClientManager()


async def get_student_collection() -> AsyncCollection:
    """Load student collection

    Returns:
        AsyncCollection: student collection
    """
    return db_client.db.get_collection("student_collection")

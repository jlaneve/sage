"Service to interact with MongoDB"
import os
from logging import getLogger
from typing import Dict

from pymongo import MongoClient

logger = getLogger(__name__)

mongo_url = os.environ.get("MONGO_URL")

logger.info("Establishing connection to MongoDB...")
client = MongoClient(mongo_url)
logger.info("Connected.")

def insert_doc(doc: Dict[str, str]) -> bool:
    """
    Insert a command into the database
    """
    db = client["commands"]
    collection = db["recorded_commands"]
    result = collection.insert_one(doc)

    logger.info(f"Inserted document with ID: {result.inserted_id}")
    
    return True
"Service to interact with MongoDB"
import os
from logging import getLogger
from typing import Dict, List

from pymongo import MongoClient

from services.gen_embeddings import generate_embeddings

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

def retrieve_doc(prompt: str) -> List[Dict[str, str]]:
    """
    Retrieve a command from the database
    """

    vectors = generate_embeddings(prompt)

    result = client['commands']['recorded_commands'].aggregate([
        {
        "$vectorSearch": {
            "index": "default",
            "path": "summary_embeddings",
            "queryVector": vectors,
            "numCandidates": 30,
            "limit": 3,
            }
        },
        {
            "$project": {
                "summary_embeddings": False,
                "score": { "$meta": "vectorSearchScore" }
            }
        }
    ])

    logger.info(f"Retrieved documents: ")
    # filter if score is less than 0.8
    result = [i for i in result if i['score'] > 0.6]
    for i in result:
        logger.info(i)
        
    return result

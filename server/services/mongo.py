"Service to interact with MongoDB"
import os
from logging import getLogger
from typing import Dict

from pymongo import MongoClient
from nomic import embed

from routes.command import CommandPrompt

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

def retrieve_doc(command_prompt: CommandPrompt) -> Dict[str, str]:
    """
    Retrieve a command from the database
    """
    # # doc = collection.find_one({"_id": doc_id})

    embeddings_responses = embed.text(
        texts=[command_prompt.prompt],
        model='nomic-embed-text-v1.5',
        task_type='search_document',
        dimensionality=512,
    )

    # print(embeddings_responses)
    
    vectors = embeddings_responses['embeddings'][0]

    result = client['commands']['recorded_commands'].aggregate([
        {
        "$vectorSearch": {
            "index": "default",
            "path": "summary_embeddings",
            "queryVector": vectors,
            "numCandidates": 3,
            "limit": 3,
            }
        }
    ])

    for i in result:
        print(i)

    # logger.info(f"Retrieved document: {doc}")

    # return doc

# write  afooor
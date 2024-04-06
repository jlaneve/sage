"Service to interact with MongoDB"
import os
from logging import getLogger
from typing import Dict, List

from pymongo import MongoClient

from services.gen_embeddings import generate_embeddings
import cohere

api_key = os.environ["COHERE_API_KEY"]

co = cohere.Client(api_key)

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

    # result = client['commands']['recorded_commands'].aggregate([
    #     {
    #     "$vectorSearch": {
    #         "index": "default",
    #         "path": "summary_embeddings",
    #         "queryVector": vectors,
    #         "numCandidates": 30,
    #         "limit": 3,
    #         }
    #     },
    #     {
    #         "$project": {
    #             "summary_embeddings": False,
    #             "score": { "$meta": "vectorSearchScore" }
    #         }
    #     }
    # ])
    vector_penalty = 1
    full_text_penalty = 1
    result = client['commands']['recorded_commands'].aggregate([
  {
    "$vectorSearch": {
      "index": "default",
      "path": "summary_embeddings",
      "queryVector": vectors,
      "numCandidates": 30,
      "limit": 10
    }
  }, {
    "$group": {
      "_id": None,
      "docs": {"$push": "$$ROOT"}
    }
  }, {
    "$unwind": {
      "path": "$docs", 
      "includeArrayIndex": "rank"
    }
  }, {
    "$addFields": {
      "vs_score": {
        "$divide": [1.0, {"$add": ["$rank", vector_penalty, 1]}]
      }
    }
  }, {
    "$project": {
      "vs_score": 1, 
      "_id": "$docs._id", 
      "command": "$docs.command",
      "cwd": "$docs.cwd",
      "base_dir": "$docs.base_dir",
      "user": "$docs.user",
      "timestamp": "$docs.timestamp",
      "command_summary": "$docs.command_summary",
    }
  },   
  {
    "$unionWith": {
      "coll": "recorded_commands",
      "pipeline": [
        {
          "$search": {
            "index": "fts",
            "phrase": {
              "query": prompt,
              "path": "command_summary",
            }
          }
        }, {
          "$limit": 100
        }, {
          "$group": {
            "_id": None,
            "docs": {"$push": "$$ROOT"}
          }
        }, {
          "$unwind": {
            "path": "$docs", 
            "includeArrayIndex": "rank"
          }
        }, {
          "$addFields": {
            "fts_score": {
              "$divide": [
                1.0,
                {"$add": ["$rank", full_text_penalty, 1]}
              ]
            }
          }
        },
        {
          "$project": {
            "fts_score": 1,
            "_id": "$docs._id",
            "command": "$docs.command",
            "cwd": "$docs.cwd",
            "base_dir": "$docs.base_dir",
            "user": "$docs.user",
            "timestamp": "$docs.timestamp",
            "command_summary": "$docs.command_summary",
          }
        }
      ]
    }
  },
  {
    "$group": {
      "_id": "$command",
      "command": {"$first": "$command"},
      "cwd": {"$first": "$cwd"},
      "base_dir":  {"$first": "$base_dir"},
      "user": {"$first": "$user"},
      "timestamp": {"$first": "$timestamp"},
      "command_summary":  {"$first": "$command_summary"},
      "vs_score": {"$max": "$vs_score"},
      "fts_score": {"$max": "$fts_score"}
    }
  },
  {
    "$project": {
      "_id": 1,
      "command": 1,
      "cwd": 1,
      "base_dir": 1,
      "user": 1,
      "timestamp": 1,
      "command_summary": 1,
      "vs_score": {"$ifNull": ["$vs_score", 0]},
      "fts_score": {"$ifNull": ["$fts_score", 0]}
    }
  },
  {
    "$project": {
      "score": {"$add": ["$fts_score", "$vs_score"]},
      "_id": 1,
      "command": 1,
      "cwd": 1,
      "base_dir": 1,
      "user": 1,
      "timestamp": 1,
      "command_summary": 1,
      "vs_score": 1,
      "fts_score": 1
    }
  },
  {"$sort": {"score": -1}},
  {"$limit": 10}
])
    
    result = list(result)
    query = prompt

    # create mapping from "command_summary" field to each object in result
    summary_to_doc = {}
    summaries = []
    for doc in result:
      summary_to_doc[doc["command_summary"]] = doc
      summaries.append(doc["command_summary"])

    reranked_docs = co.rerank(model="rerank-english-v2.0", query=query, documents=summaries, top_n=3, return_documents=True)
    
    # print(reranked_docs)
    final_result = []
    for reranked_doc in reranked_docs.results:
      text = reranked_doc.document.text
      if reranked_doc.relevance_score > 0.6:
        obj = summary_to_doc[text]
        obj.update({"score": reranked_doc.relevance_score})
        final_result.append(obj)
      
    logger.info(f"Retrieved documents: ")
    # filter if score is less than 0.8
    # result = [i for i in result if i['score'] > 0.0]
    for i in final_result:
        logger.info(i)
        
    return final_result

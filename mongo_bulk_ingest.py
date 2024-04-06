import csv

# Open the input files
with open('all.cm', 'r') as cm_file, open('all.nl', 'r') as nl_file:
    # Read the lines from each file
    cm_lines = cm_file.readlines()
    nl_lines = nl_file.readlines()
    
import os
from typing import Dict, List

from pymongo import MongoClient

from server.services.gen_embeddings import generate_embeddings

mongo_url = os.environ.get("MONGO_URL")


client = MongoClient(mongo_url)
print("Connected.")

for i in range(0, len(cm_lines)):
    doc = {
        "command": cm_lines[i].strip(),
        "cwd": "/",
        "base_dir": "/",
        "user": "user",
        "timestamp": "2024-01-01T00:00:00Z",
        "command_summary": nl_lines[i],
    }

    vectors = generate_embeddings(cm_lines[i])

    doc["summary_embeddings"] = vectors
    db = client["commands"]
    collection = db["recorded_commands"]
    doc = {
        "command": doc["command"],
        "cwd": doc["cwd"],
        "base_dir": doc["base_dir"],
        "user": doc["user"],
        "timestamp": doc["timestamp"],
        "command_summary": doc["command_summary"],
        "summary_embeddings": doc["summary_embeddings"],
    }
    result = collection.insert_one(doc)

    print(f"Inserted document with ID: {result.inserted_id}")

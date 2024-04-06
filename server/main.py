from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

import uvicorn

app = FastAPI()

HF_TOKEN = os.environ.get("HF_TOKEN")
HF_INFERENCE_URL = os.environ.get("HF_INFERENCE_URL")
HF_HEADERS = {
	"Accept" : "application/json",
	"Authorization": f"Bearer {HF_TOKEN}",
	"Content-Type": "application/json" 
}
HF_TOKEN_CLASSIFICATION_PARAMS = {"aggregation_strategy": "simple"}

@app.get("/")
async def root():
    return {"status": "healthy"}


class RecordedCommand(BaseModel):
    command: str
    context: str
    
    
def gen_replacement_word(entity):
    replacement_word = "<REPLACE_WITH_YOUR_OWN_VALUE>"
    if entity["entity_group"] == "EMAIL":
        replacement_word = "<REPLACE_WITH_YOUR_OWN_EMAIL>"
    elif entity["entity_group"] == "IP_ADDRESS":
        replacement_word = "<REPLACE_WITH_YOUR_OWN_IP>"
    elif entity["entity_group"] == "DOMAIN_NAME":
        replacement_word = "<REPLACE_WITH_YOUR_OWN_DOMAIN>"
    elif entity["entity_group"] == "USERNAME":
        replacement_word = "<REPLACE_WITH_YOUR_OWN_USERNAME>"
    elif entity["entity_group"] == "PASSWORD":
        replacement_word = "<REPLACE_WITH_YOUR_OWN_PASSWORD>"
    elif entity["entity_group"] == "KEY":
        replacement_word = "<REPLACE_WITH_YOUR_OWN_KEY>"
    elif entity["entity_group"] == "NAME":
        replacement_word = "<REPLACE_WITH_YOUR_OWN_NAME>"
    return replacement_word

# generate an endpoint that sends a request to a huggingface endpoint and responses the response
@app.post("/insert_command")
async def insert_command(recorded_command: RecordedCommand):
    command = recorded_command.command
    context = recorded_command.context
    
    # get pii data
    payload = {
        "inputs": command,
        "parameters": HF_TOKEN_CLASSIFICATION_PARAMS
    }
    response = requests.post(HF_INFERENCE_URL, headers=HF_HEADERS, json=payload)
    
    ner_result = response.json()
    # based on response, redact
    for entity in ner_result:
        if entity["score"] < 0.5:
            continue

    parsed_command = command.replace(entity["word"].strip(), gen_replacement_word(entity))
    
    return {"insert_status": parsed_command}

    # return {"insert_status": "complete"}


uvicorn.run(app, host="127.0.0.1", port=8000)
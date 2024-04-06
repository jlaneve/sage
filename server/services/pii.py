"PII redaction service"
import os
from typing import Dict
import requests

HF_TOKEN = os.environ.get("HF_TOKEN")
HF_INFERENCE_URL = os.environ.get("HF_INFERENCE_URL")
HF_HEADERS = {
	"Accept" : "application/json",
	"Authorization": f"Bearer {HF_TOKEN}",
	"Content-Type": "application/json" 
}
HF_TOKEN_CLASSIFICATION_PARAMS = {"aggregation_strategy": "simple"}


def gen_replacement_word(entity: Dict[str, str]) -> str:
    """
    Generate a replacement word for a given entity
    """
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

def redact_command(cmd: str) -> str:
    """
    Redact PII from a command string
    """
    payload = {
        "inputs": cmd,
        "parameters": HF_TOKEN_CLASSIFICATION_PARAMS,
    }

    response = requests.post(HF_INFERENCE_URL, headers=HF_HEADERS, json=payload)
    ner_result = response.json()

    # based on response, redact
    for entity in ner_result:
        if entity["score"] < 0.9:
            continue
        parsed_command = cmd.replace(entity["word"].strip(), gen_replacement_word(entity))
    
    return parsed_command
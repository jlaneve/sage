"PII redaction service"
import os
from typing import Dict
import requests
from typing import Dict

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
    replacement_word = {
        "EMAIL": "<REPLACE_WITH_YOUR_OWN_EMAIL_OR_USERNAME@HOST>",
        "IP_ADDRESS": "<REPLACE_WITH_YOUR_OWN_IP>",
        "DOMAIN_NAME": "<REPLACE_WITH_YOUR_OWN_DOMAIN>",
        "USERNAME": "<REPLACE_WITH_YOUR_OWN_USERNAME>",
        "PASSWORD": "<REPLACE_WITH_YOUR_OWN_PASSWORD>",
        "KEY": "<REPLACE_WITH_YOUR_OWN_KEY>",
        "NAME": "<REPLACE_WITH_YOUR_OWN_NAME>",
    }.get(entity.get("entity_group"), "Invalid entity group")
    
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

    parsed_command = cmd
    # based on response, redact
    for entity in ner_result:
        if entity["score"] < 0.9:
            continue
        parsed_command = cmd.replace(entity["word"].strip(), gen_replacement_word(entity))
    
    return parsed_command
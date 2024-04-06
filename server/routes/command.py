from logging import getLogger

from fastapi import APIRouter

from models.command import CommandPrompt, RecordedCommand
from services.gen_embeddings import generate_embeddings
from services.gen_cmd_summary import generate_command_summary
from services.pii_redaction import redact_command
from services.mongo import insert_doc, retrieve_doc

logger = getLogger(__name__)

cmd_router = APIRouter()


@cmd_router.post("/insert_command")
async def insert_command(req: RecordedCommand):
    """
    Processes a command. Redacts PII and returns the redacted command
    """
    redacted_cmd = redact_command(req.command)

    cmd_summary = generate_command_summary(redacted_cmd)
    doc = {
        "command": redacted_cmd,
        "cwd": req.cwd,
        "base_dir": req.base_dir,
        "user": req.user,
        "timestamp": req.timestamp,
        "command_summary":cmd_summary,
    }

    logger.info(f"Inserting command: {doc}")
    
    vectors = generate_embeddings(req.command)
    
    doc["summary_embeddings"] = vectors
    
    insert_doc(doc)

    # turn object id to a str
    doc["_id"] = str(doc["_id"])

    return doc

@cmd_router.post("/complete_command")
async def complete_command(req: CommandPrompt):
    """
    Based on prompt. Returns the top relevant commands or suggest one if none found
    """

    doc = {
        "prompt": req.prompt,
        "cwd": req.cwd,
        "base_dir": req.base_dir,
        "user": req.user,
        "timestamp": req.timestamp,
    }

    logger.info(f"Retrieving command: {doc}")

    retrieved_docs = retrieve_doc(req)

    # # turn object id to a str
    for doc in retrieved_docs:
        doc["_id"] = str(doc["_id"])
        
    return {"retrieved_docs": list(retrieved_docs)}
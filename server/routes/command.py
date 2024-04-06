from logging import getLogger
from typing import List

from fastapi import APIRouter

from models.command import RecordedCommand, CommandOutput, command_output, RankedCommandOutput, ranked_command_output
from services.gen_embeddings import generate_embeddings
from services.llm_services import complete_command_code_with_rag, generate_command_summary
from services.pii_redaction import redact_command
from services.mongo import insert_doc, retrieve_doc

logger = getLogger(__name__)

cmd_router = APIRouter()


@cmd_router.post("/insert_command")
async def insert_command(req: RecordedCommand) -> CommandOutput:
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

    return command_output(doc)

@cmd_router.post("/complete_command")
async def complete_command(prompt: str) -> List[RankedCommandOutput]:
    """
    Based on prompt. Returns the top relevant commands or suggest one if none found
    """
    logger.info(f"Retrieving commands for: {prompt}")

    retrieved_docs = retrieve_doc(prompt)

    # sort by score
    retrieved_docs = sorted(retrieved_docs, key=lambda x: x["score"], reverse=True)

    llm_generated_code = complete_command_code_with_rag(prompt, retrieved_docs)
    return {"retrieved_docs": list([ranked_command_output(doc) for doc in retrieved_docs]), "llm_generated_code": llm_generated_code}

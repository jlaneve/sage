from logging import getLogger

from fastapi import APIRouter
from pydantic import BaseModel

from services.pii_redaction import redact_command
from services.mongo import insert_doc

logger = getLogger(__name__)

cmd_router = APIRouter()

class RecordedCommand(BaseModel):
    command: str
    cwd: str
    base_dir: str
    user: str
    timestamp: str


@cmd_router.post("/insert_command")
async def insert_command(req: RecordedCommand):
    """
    Processes a command. Redacts PII and returns the redacted command
    """
    redacted_cmd = redact_command(req.command)

    doc = {
        "command": redacted_cmd,
        "cwd": req.cwd,
        "base_dir": req.base_dir,
        "user": req.user,
        "timestamp": req.timestamp
    }

    logger.info(f"Inserting command: {doc}")
    insert_doc(doc)

    return doc
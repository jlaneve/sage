from fastapi import APIRouter
from pydantic import BaseModel

from services.pii import redact_command

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

    return redacted_cmd
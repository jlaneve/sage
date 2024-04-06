from pydantic import BaseModel


class RecordedCommand(BaseModel):
    command: str
    cwd: str
    base_dir: str
    user: str
    timestamp: str

class CommandPrompt(BaseModel):
    prompt: str
    cwd: str
    base_dir: str
    user: str
    timestamp: str
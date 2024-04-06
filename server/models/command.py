from pydantic import BaseModel
from typing import Dict, List


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

class CommandOutput(BaseModel):
    _id: str
    command: str
    cwd: str
    base_dir: str
    user: str
    timestamp: str
    command_summary: str

class RankedCommandOutput(BaseModel):
    _id: str
    command: str
    cwd: str
    base_dir: str
    user: str
    timestamp: str
    command_summary: str
    score: float

class RetrievalAndOutput(BaseModel):
    retrieved_docs: List[RankedCommandOutput]
    llm_generated_code: str
    
def command_output(input: Dict[str, str]) -> CommandOutput:
    return CommandOutput(
        _id=str(input["_id"]),
        command=input["command"],
        cwd=input["cwd"],
        base_dir=input["base_dir"],
        user=input["user"],
        timestamp=input["timestamp"],
        command_summary=input["command_summary"],
    )

def ranked_command_output(input: Dict[str, str]) -> RankedCommandOutput:
    return RankedCommandOutput(
        _id=str(input["_id"]),
        command=input["command"],
        cwd=input["cwd"],
        base_dir=input["base_dir"],
        user=input["user"],
        timestamp=input["timestamp"],
        command_summary=input["command_summary"],
        score=input["score"]
    )
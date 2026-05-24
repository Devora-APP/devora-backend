from pydantic import BaseModel


class GenerateRequest(BaseModel):
    prompt: str
    language: str


class DebugRequest(BaseModel):
    code: str
    language: str


class ExecuteRequest(BaseModel):
    code: str
    language: str
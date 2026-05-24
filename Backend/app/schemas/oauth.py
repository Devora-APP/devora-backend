from pydantic import BaseModel

class GoogleAuthRequest(BaseModel):
    token: str

class GitHubAuthRequest(BaseModel):
    code: str
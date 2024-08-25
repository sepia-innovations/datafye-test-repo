from pydantic import BaseModel

class PostMessageRequest(BaseModel):
    message: str

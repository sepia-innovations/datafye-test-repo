from pydantic import BaseModel
from typing import Optional

class CreateChannelRequest(BaseModel):
    channel_name: str
    is_private: Optional[bool] = False
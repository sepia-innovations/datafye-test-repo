from pydantic import BaseModel, EmailStr
from typing import List

class AddUserToChannelRequest(BaseModel):
    user_email_list: List[EmailStr]
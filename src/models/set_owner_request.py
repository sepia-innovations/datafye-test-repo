from pydantic import BaseModel, EmailStr

class SetOwnerRequest(BaseModel):
    user_email: EmailStr

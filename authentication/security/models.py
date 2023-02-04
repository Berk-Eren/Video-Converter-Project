from pydantic import BaseModel


class UserInfo(BaseModel):
    email: str
    username: str

from pydantic import BaseModel


class UserCredentials(BaseModel):
    username: str
    password: str


class UserCreation(UserCredentials):
    email: str
    password2: str

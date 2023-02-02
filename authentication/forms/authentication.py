from fastapi import Form
from typing import Optional


class UserCredentials:
    def __init__(
        self,
        username: str = Form(),
        password: str = Form()
    ):
        self.username = username
        self.password = password

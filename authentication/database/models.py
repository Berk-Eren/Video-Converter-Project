from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    username = Column(String, unique=True)

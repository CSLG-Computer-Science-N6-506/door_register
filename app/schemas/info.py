from pydantic import BaseModel
from typing import List

class Info(BaseModel):
    password: str
    roles: list
    token: str
    introduction: str
    avatar: str
    name: str
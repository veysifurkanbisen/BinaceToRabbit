import uuid
from pydantic import BaseModel, Field

class Queue(BaseModel):
    userName: str = Field(...)
    symbol: str = Field(...)

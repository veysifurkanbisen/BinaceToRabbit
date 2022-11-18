import uuid
from pydantic import BaseModel, Field

class Queue(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    userName: str = Field(...)
    symbol: str = Field(...)
    interval: str = Field(...)
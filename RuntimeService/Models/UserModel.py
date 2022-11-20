from pydantic import BaseModel, Field

class User(BaseModel):
    userName: str = Field(...)
    symbol: str = Field(...)
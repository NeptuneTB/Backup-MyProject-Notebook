from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing_extensions import Annotated

class MachineData(BaseModel):
    timestamp: datetime
    temperature: Annotated[float, ...]
    pressure: Annotated[float, ...]
    speed: Annotated[float, ...]
    
class User(BaseModel):
    username: str
    password: str
    api_key: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
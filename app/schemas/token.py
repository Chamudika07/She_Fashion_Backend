from pydantic import BaseModel
from typing import Optional
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
#this is to store the data we encoded in the token
class TokenData(BaseModel):
    id: Optional[int] = None
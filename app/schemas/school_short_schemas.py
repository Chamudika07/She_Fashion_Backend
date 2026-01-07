from pydantic import BaseModel
from datetime import datetime

class SchoolShortCreate(BaseModel):
    size : int
    color : str
    type : str
    quntity : int
    
class SchoolShortOut(BaseModel):
    id : int
    size : int
    color : str
    type : str
    quntity : int
    created_at : datetime

    class Config:
        orm_mode = True
        
class ShortQuntityUpdate(BaseModel):
    size : int
    color : str
    type : str
    quntity : int
    action : str  # "sell" or "buy"
    
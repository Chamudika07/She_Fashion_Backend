from pydantic import BaseModel
from datetime import datetime

class SchoolShirtCreate(BaseModel):
    size : float
    quntity : int
    
class SchoolShirtOut(BaseModel):
    id : int
    size : float
    quntity : int
    created_at : datetime

    class Config:
        orm_mode = True
        
class ShirtQuntityUpdate(BaseModel):
    size : float
    quntity : int
    action : str  # "sell" or "buy"
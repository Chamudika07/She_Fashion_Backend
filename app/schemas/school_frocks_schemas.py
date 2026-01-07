from pydantic import BaseModel
from datetime import datetime

class SchoolFrock(BaseModel):
    size : int
    quntity : int
    
class SchoolFrockOut(BaseModel):
    id : int
    size : int
    quntity : int
    created_at : datetime

    class Config:
        orm_mode = True
        
class FrockQuntityUpdate(BaseModel):
    size : int
    quntity : int
    action : str  # "sell" or "buy"
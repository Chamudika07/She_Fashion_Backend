from pydantic import BaseModel
from datetime import datetime

class SchoolFrock(BaseModel):
    size : str
    quntity : int
    
class SchoolFrockOut(BaseModel):
    id : int
    size : str
    quntity : int
    created_at : datetime

    class Config:
        orm_mode = True
        
class FrockQuntityUpdate(BaseModel):
    size : str 
    quntity : int
    action : str  # "sell" or "buy"
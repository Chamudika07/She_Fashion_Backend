from pydantic import BaseModel
from datetime import datetime

class ScholeShoesCreate(BaseModel):
    size : int
    type : str
    boysORgirls : str
    quntity : int
    
class ScholeShoesOut(BaseModel):
    id : int
    size : int
    type : str
    boysORgirls : str
    quntity : int
    created_at : datetime

    class Config:
        orm_mode = True
    
class ShoeQuntityUpdate(BaseModel):
    size : int
    type : str
    boysORgirls : str
    quntity : int
    action : str  # "sell" or "buy"
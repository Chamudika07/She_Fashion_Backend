from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status , Response
from .. import models, utils , oauth2
from ..database import get_db
from ..schemas import school_frocks_schemas 
from typing import List

router = APIRouter(
    prefix="/frocks",
    tags=['Schoole Frocks']
)   

# Create a new school frock
@router.post("", status_code=status.HTTP_201_CREATED, response_model=school_frocks_schemas.SchoolFrockOut)
def create_frock(frock: school_frocks_schemas.SchoolFrock, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    
    exit_frock = db.query(models.SchoolFrocks).filter(models.SchoolFrocks.size == frock.size).first()
    
    if exit_frock:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Frock size {frock.size} already exists")
    
    else:
        new_frock = models.SchoolFrocks(**frock.dict())
        db.add(new_frock)
        db.commit() 
        db.refresh(new_frock)
        return new_frock
    
# Get all school frocks
@router.get("", response_model=List[school_frocks_schemas.SchoolFrockOut])
def get_all_frocks(db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    
    frocks = db.query(models.SchoolFrocks).all()
    return frocks

#buy and sell school frocks
@router.put("/quantity", response_model=school_frocks_schemas.SchoolFrockOut)
def update_frock_quantity( frock_update: school_frocks_schemas.FrockQuntityUpdate, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    
    frock_query = db.query(models.SchoolFrocks).filter(models.SchoolFrocks.size == frock_update.size)
    frock = frock_query.first()
    
    if not frock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Frock size {frock_update.size} not found")
    
    if frock_update.action == "sell":
        if frock.quntity < frock_update.quntity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient quantity to sell")
        frock.quntity -= frock_update.quntity
    elif frock_update.action == "buy":
        frock.quntity += frock_update.quntity
    
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid action. Use 'buy' or 'sell'.")
    
    frock_query.update({"quntity": frock.quntity}, synchronize_session=False)
    db.commit()
    return frock_query.first()
    
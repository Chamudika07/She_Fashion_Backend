from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status , Response
from .. import models, utils , oauth2
from ..database import get_db
from ..schemas import school_shirt 
from typing import List

router = APIRouter(
    prefix="/shirts",
    tags=['Schoole Shirts']
) 


# Create a new school shirt
@router.post("", status_code=status.HTTP_201_CREATED, response_model=school_shirt.SchoolShirtOut)
def create_shirt(shirt: school_shirt.SchoolShirtCreate, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    
    exit_shirt = db.query(models.SchoolShirts).filter(models.SchoolShirts.size == shirt.size).first()
    
    if exit_shirt:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Shirt size {shirt.size} already exists")
    
    else:
        new_shirt = models.SchoolShirts(**shirt.dict())
        db.add(new_shirt)
        db.commit() 
        db.refresh(new_shirt)
        return new_shirt
    
# Get all school shirts
@router.get("", response_model=List[school_shirt.SchoolShirtOut])
def get_all_shirts(db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    
    shirts = db.query(models.SchoolShirts).all()
    return shirts

#buy and sell school shirts
@router.put("/quantity", response_model=school_shirt.SchoolShirtOut)
def update_shirt_quantity( shirt_update: school_shirt.ShirtQuntityUpdate, 
                        db: Session = Depends(get_db),
                        current_user: int = Depends(oauth2.get_current_user)):
    
    shirt_query = db.query(models.SchoolShirts).filter(models.SchoolShirts.size == shirt_update.size)
    shirt = shirt_query.first()
    
    if not shirt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Shirt with size {shirt_update.size} not found")
    
    if shirt_update.action == "sell":
        if shirt.quntity < shirt_update.quntity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Not enough shirts in stock to sell")
        shirt.quntity -= shirt_update.quntity
    
    elif shirt_update.action == "buy":
        shirt.quntity += shirt_update.quntity
    
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Action must be either 'sell' or 'buy'")
    
    shirt_query.update({"quntity": shirt.quntity}, synchronize_session=False)
    db.commit()
    db.refresh(shirt)
    
    return shirt
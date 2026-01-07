from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status , Response
from .. import models, utils , oauth2
from ..database import get_db
from ..schemas import school_short_schemas
from typing import List

router = APIRouter(
    prefix="/shorts",
    tags=['Schoole Shorts']
)

# Create a new school short
@router.post("", status_code=status.HTTP_201_CREATED, response_model=school_short_schemas.SchoolShortOut)
def create_short(short: school_short_schemas.SchoolShortCreate, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    
    exit_short = db.query(models.SchoolShorts).filter(
        models.SchoolShorts.size == short.size,
        models.SchoolShorts.color == short.color,
        models.SchoolShorts.type == short.type
    ).first()
    
    if exit_short:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Short of size {short.size}, color {short.color}, type {short.type} already exists")
    
    else:
        new_short = models.SchoolShorts(**short.dict())
        db.add(new_short)
        db.commit() 
        db.refresh(new_short)
        return new_short
    
# Get all school shorts
@router.get("", response_model=List[school_short_schemas.SchoolShortOut])
def get_all_shorts(db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    shorts = db.query(models.SchoolShorts).all()
    return shorts

# Update school short quantity
@router.put("", response_model=school_short_schemas.SchoolShortOut)
def update_short_quantity(update_data: school_short_schemas.ShortQuntityUpdate, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    
    short = db.query(models.SchoolShorts).filter(
        models.SchoolShorts.size == update_data.size,
        models.SchoolShorts.color == update_data.color,
        models.SchoolShorts.type == update_data.type
    ).first()
    
    if not short:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short not found")
    
    if update_data.action == "sell":
        if short.quntity < update_data.quntity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient quantity to sell")
        short.quntity -= update_data.quntity
    elif update_data.action == "buy":
        short.quntity += update_data.quntity
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid action. Use 'sell' or 'buy'.")
    
    db.commit()
    db.refresh(short)
    return short    

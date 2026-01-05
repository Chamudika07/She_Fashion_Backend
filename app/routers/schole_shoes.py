from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status , Response
from .. import models, utils , oauth2
from ..database import get_db
from ..schemas import schole_shoes_schemas
from typing import List

router = APIRouter(
    prefix="/shoes",
    tags=['Schoole Shoes']
)   

# Create a new school shoe
@router.post("", status_code=status.HTTP_201_CREATED, response_model=schole_shoes_schemas.ScholeShoesOut)
def create_school_shoe(shoe: schole_shoes_schemas.ScholeShoesCreate, db: Session = Depends(get_db) , current_user: int = Depends(oauth2.get_current_user)):
    new_shoe = models.SchoolShoes(**shoe.dict())
    
    if new_shoe.quntity < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Quantity cannot be negative")
    
    elif new_shoe.size <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Size must be a positive integer")
    
    before = db.query(models.SchoolShoes).filter(models.SchoolShoes.size == new_shoe.size,
                                                  models.SchoolShoes.type == new_shoe.type,
                                                  models.SchoolShoes.boysORgirls == new_shoe.boysORgirls).first()
    if before:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This shoe entry already exists because only you can update the quantity of existing shoes.")

    else:
        db.add(new_shoe)
        db.commit()
        db.refresh(new_shoe)
        
        return new_shoe
    

# Get all school shoes
@router.get("", response_model=List[schole_shoes_schemas.ScholeShoesOut])
def get_all_school_shoes(db: Session = Depends(get_db)):
    shoes = db.query(models.SchoolShoes).all()
    return shoes



# create sell and buy endpoint
@router.put("/quantity", response_model=schole_shoes_schemas.ScholeShoesOut)
def update_shoe_quntity(shoe_update: schole_shoes_schemas.ShoeQuntityUpdate, db: Session = Depends(get_db)):
    
    shoe_query = db.query(models.SchoolShoes).filter(
    models.SchoolShoes.size == shoe_update.size,
    models.SchoolShoes.type == shoe_update.type,
    models.SchoolShoes.boysORgirls == shoe_update.boysORgirls
)
    shoe = shoe_query.first()

    if not shoe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Shoe with size: {shoe_update.size}, type: {shoe_update.type}, boysORgirls: {shoe_update.boysORgirls} not found")
    
    if shoe_update.quntity <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Quantity must be a positive integer")
    #SELL 
    if shoe_update.action == "sell":
        if shoe.quntity < shoe_update.quntity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Not enough quantity to sell")
        shoe.quntity -= shoe_update.quntity

    elif shoe_update.action == "buy":
        shoe.quntity += shoe_update.quntity

    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid action. Use 'sell' or 'buy'.")

    db.commit()
    db.refresh(shoe)
    return shoe

#update shoe quantity by ID
@router.put("/{shoe_id}", response_model=schole_shoes_schemas.ScholeShoesOut)
def update_shoe_quantity(shoe_id: int, updated_shoe: schole_shoes_schemas.ScholeShoesCreate, db: Session = Depends(get_db)):
    shoe_query = db.query(models.SchoolShoes).filter(models.SchoolShoes.id == shoe_id)
    shoe = shoe_query.first()

    if not shoe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Shoe with id: {shoe_id} not found")

    if updated_shoe.quntity < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Quantity cannot be negative")

    shoe_query.update(updated_shoe.dict(), synchronize_session=False)
    db.commit()
    return shoe_query.first()

#delete a shoe entry
@router.delete("/{shoe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shoe(shoe_id: int, db: Session = Depends(get_db)):
    shoe_query = db.query(models.SchoolShoes).filter(models.SchoolShoes.id == shoe_id)
    shoe = shoe_query.first()

    if not shoe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Shoe with id: {shoe_id} not found")

    shoe_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



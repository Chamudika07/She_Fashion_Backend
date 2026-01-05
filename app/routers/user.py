from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException , status
from .. import models , utils , oauth2
from ..database import get_db
from ..schemas import user_schemas , token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(
    prefix="/users",
    tags=['Users']
)

#create a new user
@router.post("" , status_code = status.HTTP_201_CREATED, response_model=user_schemas.UserOut)
def create_user(user: user_schemas.UserCreate , db: Session = Depends(get_db)):

    #check if user with same email already exists
    exiting_user = db.query(models.User).filter(models.User.email == user.email).first() 
    if exiting_user:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST , 
                            detail = f"user with email: {user.email} already exists")
    
    #hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#login user
@router.post("/login" , response_model=token.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password , user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Password")
    
    #create a token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    
    return {"access_token": access_token , "token_type": "bearer"}
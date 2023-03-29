import logging
from fastapi import APIRouter
from fastapi import status, HTTPException, Response, Depends
from sqlalchemy.orm import Session

from src.db.models.address import User
from src.db.session import get_db
from . import schemas
from .hashing import Hash

router = APIRouter(
    prefix='/v1.0/users',
        tags=['User Management']
    )


@router.post('/save_user_details', response_model=schemas.ShowUser, status_code=status.HTTP_200_OK)
def create_user(request: schemas.User, db: Session=Depends(get_db)):
    try:
        new_user = User(name=request.name, email=request.email,password=Hash.encrypt(request.password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        db.close()
        return new_user
    except Exception as exception:
        logging.error(exception)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in saving user details.")


@router.get('/{user_id}', response_model=schemas.ShowUser, status_code=status.HTTP_200_OK)
def get_user(user_id, response:Response, db: Session=Depends(get_db)):
    try:
        user_details = db.query(User).filter(User.id == user_id).first()
        if not user_details:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "user not found")
        return user_details
    except Exception as exception:
        logging.error(exception)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in getting user details.")

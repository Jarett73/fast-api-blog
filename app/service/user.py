from app.authentication.hashing import Hash
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas


def fetch_all_users(db: Session):
    users = db.query(models.User).all()
    return list(users)


def fetch_specific_user(id:int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")
    return user


def create_user(request: schemas.User, db: Session):
    try:
        new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
        db.add(new_user)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Something went wrong while creating a new user, error: {e}")
    response = {"status": "Success", "message": "User created Successfully."}
    return response


def update_user(id:int, request: schemas.User, db: Session):
    try:
        user = db.query(models.User).filter(models.User.id == id)

        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with id {id} not found")

        user.update(request)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Something went wrong while updating the user, error: {e}")

    response = {"status": "Success", "message": "User updated Successfully."}
    return response


def delete_user(id:int, db: Session):
    try:
        user = db.query(models.User).filter(models.User.id == id).first()

        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with id {id} not found")

        user.delete()
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Something went wrong while deleting the user, error: {e}")

    response = {"status": "Success", "message": "User deleted Successfully."}
    return response

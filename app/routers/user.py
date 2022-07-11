from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import database, schemas
from app.authentication import oauth2
from app.service.user import fetch_all_users, fetch_specific_user, create_user, update_user, delete_user

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db_conn = database.get_db


@router.get('/', response_model=List[schemas.ShowAllUsers])
def _fetch_all_users(db: Session = Depends(get_db_conn), current_user: schemas.User = Depends(
    oauth2.get_current_user)):
    """Fetch all the users from the database"""
    return fetch_all_users(db)


@router.get('/{id}', response_model=schemas.ShowUser)
def _fetch_specific_user(id:int, db: Session = Depends(get_db_conn), current_user: schemas.User = Depends(
    oauth2.get_current_user)):
    """Fetch user based on the user id"""
    return fetch_specific_user(id, db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def _create_new_user(request: schemas.User, db: Session = Depends(get_db_conn)):
    """Creates a new user based on the passed payload"""
    return create_user(request, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def _update_user(id:int, request: schemas.User, db: Session = Depends(get_db_conn), current_user: schemas.User = Depends(
    oauth2.get_current_user)):
    """Updates the user based on the id with passed payload"""
    return update_user(id, request, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def _delete_user(id:int, db: Session = Depends(get_db_conn), current_user: schemas.User = Depends(
    oauth2.get_current_user)):
    """Deletes the user based on the user id"""
    return delete_user(id, db)

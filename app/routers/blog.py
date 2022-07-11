from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import schemas, database
from app.authentication import oauth2
from app.service.blog import fetch_all_blogs, create_blog, delete_blog, update_blog, fetch_specific_blog

router = APIRouter(
    prefix="/blog",
    tags=['Blogs']
)

get_db_conn = database.get_db


@router.get('/', response_model=List[schemas.ShowBlog])
def _fetch_all_blogs(db: Session = Depends(get_db_conn), current_user: schemas.User = Depends(
    oauth2.get_current_user)):
    """Fetch all the blogs from the database"""
    return fetch_all_blogs(db)


@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def _fetch_specific_blog(id:int, db: Session = Depends(get_db_conn), current_user: schemas.User = Depends(
    oauth2.get_current_user)):
    """Fetch blog based on the blog id"""
    return fetch_specific_blog(id, db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def _create_new_blog(request: schemas.Blog, db: Session = Depends(get_db_conn), current_user: schemas.User = Depends(
    oauth2.get_current_user)):
    """Creates a new blog based on the passed payload"""
    return create_blog(request, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def _update_blog(id:int, request: schemas.Blog, db: Session = Depends(get_db_conn), current_user: schemas.User = Depends(
    oauth2.get_current_user)):
    """Updates the blog based on the id with passed payload"""
    return update_blog(id, request, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def _delete_blog(id:int, db: Session = Depends(get_db_conn), current_user: schemas.User = Depends(
    oauth2.get_current_user)):
    """Deletes the blog based on the blog id"""
    return delete_blog(id, db)

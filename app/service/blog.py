from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas


def fetch_all_blogs(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def fetch_specific_blog(id:int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not available")
    return blog


def create_blog(request: models.Blog, db: Session):
    try:
        new_blog = models.Blog(title=request.title, body=request.body, user_id=request.creator_id)
        db.add(new_blog)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Something went wrong while creating a new blog, error: {e}")
    response = {"status": "Success", "message": "Blog created Successfully."}
    return response


def update_blog(id:int, request: schemas.Blog, db: Session):
    try:
        blog = db.query(models.Blog).filter(models.Blog.id == id)

        if not blog.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Blog with id {id} not found")

        blog.update(request)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Something went wrong while updating the blog, error: {e}")

    response = {"status": "Success", "message": "Blog updated Successfully."}
    return response


def delete_blog(id:int, db: Session):
    try:
        blog = db.query(models.Blog).filter(models.Blog.id == id).first()

        if not blog.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Blog with id {id} not found")

        blog.delete()
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Something went wrong while deleting the blog, error: {e}")

    response = {"status": "Success", "message": "Blog deleted Successfully."}
    return response

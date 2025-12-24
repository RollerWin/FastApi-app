from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.deps import get_current_user
from src.db.session import get_session
from src.repositories import post as post_repository
from src.schemas.post import PostCreate, PostRead, PostUpdate

router = APIRouter()


@router.get("/", response_model=list[PostRead])
def list_posts(
    skip: int = 0,
    limit: int = 20,
    session: Session = Depends(get_session),
):
    return post_repository.list_posts(session, skip=skip, limit=limit)


@router.get("/{post_id}", response_model=PostRead)
def get_post(post_id: int, session: Session = Depends(get_session)):
    post = post_repository.get_post(session, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def create_post(
    post_in: PostCreate,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return post_repository.create_post(
        session,
        title=post_in.title,
        body=post_in.body,
        author_id=current_user.id,
    )


@router.put("/{post_id}", response_model=PostRead)
def update_post(
    post_id: int,
    post_in: PostUpdate,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    post = post_repository.get_post(session, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights")
    return post_repository.update_post(
        session, post, title=post_in.title, body=post_in.body
    )


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    post = post_repository.get_post(session, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights")
    post_repository.delete_post(session, post)

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.post import Post


def list_posts(session: Session, *, skip: int = 0, limit: int = 20) -> list[Post]:
    result = session.execute(
        select(Post).order_by(Post.created_at.desc()).offset(skip).limit(limit)
    )
    return list(result.scalars().all())


def get_post(session: Session, post_id: int) -> Post | None:
    return session.get(Post, post_id)


def create_post(session: Session, *, title: str, body: str, author_id: int) -> Post:
    post = Post(title=title, body=body, author_id=author_id)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


def update_post(session: Session, post: Post, *, title: str | None, body: str | None) -> Post:
    if title is not None:
        post.title = title
    if body is not None:
        post.body = body
    session.commit()
    session.refresh(post)
    return post


def delete_post(session: Session, post: Post) -> None:
    session.delete(post)
    session.commit()

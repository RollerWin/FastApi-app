from sqlalchemy.orm import Session

from src.core.security import create_access_token, get_password_hash, verify_password
from src.repositories import user as user_repository


def register_user(session: Session, *, email: str, username: str, password: str):
    hashed_password = get_password_hash(password)
    return user_repository.create_user(
        session, email=email, username=username, hashed_password=hashed_password
    )


def authenticate_user(session: Session, *, username: str, password: str):
    user = user_repository.get_by_username(session, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token_for_user(user_id: int) -> str:
    return create_access_token(subject=str(user_id))

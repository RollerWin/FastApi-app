from fastapi import FastAPI

from src.api.routers import auth, posts, users
from src.db.base import Base
from src.db.session import engine
import src.models as models

app = FastAPI(title="Simple Blog API")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}

from fastapi import FastAPI, HTTPException
from typing import Optional
from app.schemas import PostCreate, PostResponse
from app.db import create_db_and_table, get_async_session, Posts
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

# Táto funkcia sa spustí pri štarte aplikácie.
# Najprv vytvorí databázu a tabuľky a až potom dovolí aplikácii pokračovať.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Vytvorenie databázy a tabuliek
    await create_db_and_table()
    yield

app = FastAPI(lifespan=lifespan)

text_posts = {
    1: {"title": "New Post", "content": "Cool text posts."},
    2: {"title": "Another Post", "content": "More text posts."},
    3: {"title": "Last Post", "content": "Final text post."},
    4: {"title": "four Post", "content": "Cool four text posts."},
    5: {"title": "fifth Post", "content": "More fifth posts."},
    6: {"title": "Last Post", "content": "Final text post."},
    7: {"title": "7th Post", "content": "Cool text posts."},
    8: {"title": "Another Post", "content": "More text posts."},
    9: {"title": "Last Post", "content": "Final text post."},
    10: {"title": "New Post", "content": "Cool text posts."},
}


@app.get("/posts")
def get_all_posts(limit: Optional[int] = None):
    if limit is not None:
        return dict(list(text_posts.items())[:limit])
    return text_posts


@app.get("/posts/{id}")
def get_post(id: int) -> PostResponse:
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return text_posts.get(id)


@app.post("/posts")
def create_post(post: PostCreate) -> PostResponse:
    new_post = {'title': post.title, 'content': post.content}
    indx = len(text_posts)+1
    text_posts[indx] = new_post
    return new_post


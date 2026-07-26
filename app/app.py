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

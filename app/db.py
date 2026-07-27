from collections.abc import AsyncGenerator
import uuid

from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime

# toto nam vytvori lokalnu databazu(subor) sqlite v nasom pocitaci a ak potom budeme chcet ju deploynut dame namiesto tej cety nejaku realnu url adresu kde bude ta databaza sidlit
DATABASE_URL = 'sqlite+aiosqlite:///./test.db' 

# vzor z ktoreho budu dedit vsetky tabulky, ktore budu vytvorene v databaze
class Base(DeclarativeBase):
    pass

class Post(Base):
    __tablename__ = 'posts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caption = Column(Text)
    url = Column(String)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_marker = async_sessionmaker(engine, expire_on_commit=False)

# tymto vytvorime vsetky tabulky v databaze ktore dedia z Base, teda v tomto pripade tabulku Posts
async def create_db_and_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# toto vytvori session, ktora sa bude pouzivat na komunikaciu s databazou, a potom sa session zavrie
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_marker() as session:
        yield session


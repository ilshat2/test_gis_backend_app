import os
from dotenv import load_dotenv
from typing import AsyncGenerator
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER", "ilshat")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "6330")
POSTGRES_DB = os.getenv("POSTGRES_DB", "testdb")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# URL подключения к базе данных
DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Создание асинхронного движка SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Фабрика асинхронных сессий
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Базовый класс для моделей ORM
Base = declarative_base()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Асинхронный генератор сессии базы данных.
    Используется в качестве зависимости FastAPI.
    """
    async with AsyncSessionLocal() as session:
        yield session

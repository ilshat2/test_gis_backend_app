from typing import AsyncGenerator
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


# URL подключения к базе данных
DATABASE_URL = "postgresql+asyncpg://ilshat:6330@localhost:5432/testdb"

# Создание асинхронного движка SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Фабрика асинхронных сессий
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Базовый класс для моделей ORM
Base = declarative_base()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Асинхронный генератор сессии базы данных.
    Используется в качестве зависимости FastAPI.
    """
    async with AsyncSessionLocal() as session:
        yield session

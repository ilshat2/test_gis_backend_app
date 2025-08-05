import sys
import os
import asyncio
import app.models_cache
from app.db import engine, Base

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


async def init_models() -> None:
    """
    Создаёт все таблицы в базе данных (если их еще нет).
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Выполняем создание таблиц при старте
asyncio.run(init_models())

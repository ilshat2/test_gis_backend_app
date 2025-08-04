import asyncio
import models_cache
from db import engine, Base


async def init_models() -> None:
    """
    Создаёт все таблицы в базе данных (если их еще нет).
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Выполняем создание таблиц при старте
asyncio.run(init_models())

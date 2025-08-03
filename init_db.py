import asyncio
import models_cache
from db import engine, Base


async def init_models():
    """
    Создаёт все таблицы в базе данных, если их ещё нет.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(init_models())

import math
import asyncio
from google_sheets_access import append_row
from models import Location
from decimal import Decimal
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models_cache import LocationCache
from geometry import generate_circle_geojson


class LocationService:
    """
    Сервис для работы с локациями:
    - Читает/пишет кэш в postgresql
    - Генерирует geojson
    - Созраняет данные в гугл таблицу
    """

    async def save_location(self, data: Location, session: AsyncSession):
        """
        Сохраняет локацию:
        - Проверяет кэш по id в postgresql
        - Если запись есть возвращает ее сразу, если нет
        имитирует долгую операцию (5 секунд) и сохраняет данные
        в базу данных и гугл таблицу
        """

        # Проверка кэша
        cache = await session.execute(
            select(LocationCache).where(LocationCache.id == data.id)
        )
        cache_obj = cache.scalar_one_or_none()
        if cache_obj:
            return cache_obj.geojson

        # Имитация долгой операции: +5 секунд.
        await asyncio.sleep(5)

        # Вычисление площади покрытия
        coverage_area = data.radius**2 * Decimal(str(math.pi))
        geojson = await generate_circle_geojson(data, coverage_area)

        # Сохранение в гугл таблицу
        await append_row(data.to_row(str(coverage_area)))

        # Сохранение в базу данных
        cache_entry = LocationCache(
            id=data.id,
            date=data.date,
            name=data.name,
            lon=data.lon,
            lat=data.lat,
            radius=data.radius,
            coverage_area=coverage_area,
            geojson=geojson,
        )
        session.add(cache_entry)
        await session.commit()
        return geojson

    async def to_geojson(self, data: Location, coverage_area, num_points=64):
        """
        Генерирует geojson полигоном круга вокруг точки.
        """
        return await generate_circle_geojson(data, coverage_area, num_points)

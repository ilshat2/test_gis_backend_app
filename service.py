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
    - Читает/пишет кэш в PostgreSQL.
    - Генерирует GeoJSON.
    - Сохраняет данные в Google Sheets.
    """

    async def save_location(
            self, data: Location, session: AsyncSession
    ) -> dict:
        """
        Сохраняет локацию:
        - Проверяет кэш по id.
        - Если запись новая: имитирует долгую операцию (5с),
          сохраняет данные в БД и Google Sheets.
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

        # Сохранение в Google Sheets
        await append_row(data.to_row(str(coverage_area)))

        # Сохранение в БД
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

    async def to_geojson(
        self, data: Location, coverage_area: Decimal, num_points: int = 64
    ) -> dict:
        """
        Генерирует GeoJSON полигон круга вокруг точки.
        """
        return await generate_circle_geojson(data, coverage_area, num_points)

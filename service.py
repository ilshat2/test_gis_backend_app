import math
import asyncio
from google_sheets_access import append_row
from models import Location
from decimal import Decimal
from geometry import generate_circle_geojson


class LocationService:
    """
    Сервис для работы с объектами Location.
    """

    async def save_location(self, data: Location):
        """
        Сохраняет данные о локации в гугл таблицу.
        Дополнительно вычисляет площадь покрытия
        и добавляет её как отдельное значение.
        Имитация долгой операции: +5 секунд.
        """
        await asyncio.sleep(5)
        coverage_area = data.radius**2 * Decimal(str(math.pi))
        await append_row(data.to_row(str(coverage_area)))
        return coverage_area

    async def to_geojson(self, data: Location, coverage_area, num_points=64):
        """
        Возвращает geojson объект с полигоном вокруг точки.
        """
        return await generate_circle_geojson(data, coverage_area, num_points)

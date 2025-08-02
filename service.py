import math
from google_sheets_access import append_row
from models import Location
from decimal import Decimal


class LocationService:
    """
    Сервис для работы с объектами Location.
    """

    async def save_location(self, data: Location):
        """
        Сохраняет данные о локации в гугл таблицу.
        Дополнительно вычисляет площадь покрытия
        и добавляет её как отдельное значение.
        """
        coverage_area = data.radius**2 * Decimal(str(math.pi))
        await append_row(data.to_row(str(coverage_area)))
        return coverage_area

    def to_geojson(self, data: Location, coverage_area):
        """
        Возвращает geojson объект со всеми свойствами.
        """
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    float(data.lon),
                    float(data.lat),
                ],  # важен порядок [lon, lan]
            },
            "properties": {
                "id": data.id,
                "date": data.date,
                "name": data.name,
                "lon": float(data.lon),
                "lat": float(data.lat),
                "radius": float(data.radius),
                "coverage_area": float(coverage_area),
            },
        }

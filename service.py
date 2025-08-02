import math
import pyproj
from google_sheets_access import append_row
from models import Location
from decimal import Decimal
from shapely.geometry import Point, mapping
from shapely.ops import transform


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

    def to_geojson(self, data: Location, coverage_area, num_points=64):
        """
        Возвращает geojson объект с полигоном вокруг точки.
        """
        proj_wgs84 = pyproj.CRS("EPSG:4326")
        proj_merc = pyproj.CRS("EPSG:3857")
        project_to_m = pyproj.Transformer.from_crs(
            proj_wgs84, proj_merc, always_xy=True
        ).transform
        project_to_deg = pyproj.Transformer.from_crs(
            proj_merc, proj_wgs84, always_xy=True
        ).transform

        centre_point = transform(project_to_m, Point(float(data.lon), float(data.lat)))
        circle = centre_point.buffer(
            float(data.radius),
            resolution=num_points,
        )
        circle_wgs84 = transform(project_to_deg, circle)

        return {
            "type": "Feature",
            "geometry": mapping(circle_wgs84),
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

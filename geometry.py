import pyproj
import asyncio
from shapely.geometry import Point, mapping
from shapely.ops import transform


def _generate_circle_geojson_sync(data, coverage_area, num_points):
    """
    Синхронная функция генерации geojson полигона круга вокруг точки.
    Используется внутри одного потока.
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


async def generate_circle_geojson(data, coverage_area, num_points=64):
    """
    Асинхронная функция вызывает синхронную функцию
    _generate_circle_geojson_sync в отдельном потоке.
    """
    return await asyncio.to_thread(
        _generate_circle_geojson_sync, data, coverage_area, num_points
    )

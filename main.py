from fastapi import FastAPI
from models import Location
from service import LocationService
from google_sheets_access import get_all_values


app = FastAPI()
service = LocationService()


@app.post("/")
async def create_location(location: Location):
    """
    Принимает данные о локации, сохраняет их в гугл таблицу и возвращает
    объект в формате geojson с вычисленной площадью покрытия.
    """
    coverage_area = await service.save_location(location)
    return service.to_geojson(location, coverage_area)


@app.get("/")
async def list_location():
    """
    Читаем все данные из таблицы.
    """
    data = await get_all_values()
    return {"rows": data}

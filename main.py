from fastapi import FastAPI
from models import Location
from service import LocationService
from google_sheets_access import get_all_values


app = FastAPI()
service = LocationService()


@app.post("/")
async def create_location(location: Location):
    """Принимаем локацию и записываем её в таблицу."""
    await service.save_location(location)
    return {"status": "ok", "message": "Location saved"}


@app.get("/")
async def list_location():
    """Читаем все данные из таблицы."""
    data = await get_all_values()
    return {"rows": data}

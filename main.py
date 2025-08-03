from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from models import Location
from service import LocationService
from google_sheets_access import get_all_values


app = FastAPI()
service = LocationService()


@app.post("/")
async def create_location(
    location: Location, session: AsyncSession = Depends(get_session)
):
    """
    Создает новую локацию:
    - Проверяет кэш postgresql
    - Если запрос выполне впервые то инициируется долгая операция,
    данные сохраняются в гугл таблицу, и базу данных
    - Возвращает данные в geijson формате
    """
    return await service.save_location(location, session)


@app.get("/")
async def list_location():
    """
    Читает все данные из таблицы.
    """
    data = await get_all_values()
    return {"rows": data}

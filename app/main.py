from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.models import Location
from app.service import LocationService


app = FastAPI()
service = LocationService()


@app.post("/")
async def create_location(
    location: Location, session: AsyncSession = Depends(get_session)
) -> dict:
    """
    Создает новую локацию.
    - Проверяет кэш в PostgreSQL.
    - Если запись новая: имитирует долгую операцию,
      сохраняет данные в Google Sheets и PostgreSQL.
    - Возвращает данные в формате GeoJSON.
    """
    return await service.save_location(location, session)

# FastAPI Location Service

Приложение для работы с локациями:

- Принимает координаты точки и радиус.
- Генерирует GeoJSON с кругом.
- Сохраняет результат в PostgreSQL и Google Sheets.
- Использует кэширование для ускорения.

## Стек

- Python 3.11
- FastAPI
- PostgreSQL (asyncpg)
- SQLAlchemy (asyncio)
- Google Sheets API
- Shapely, PyProj

---

## Локальный запуск

1. Клонируйте репозиторий:

```bash
git clone git@github.com:ilshat2/test_gis_backend_app.git

cd test_gis_backend_app.git

```

2. Создайте виртуальное окружение и установите зависимости:

```
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Создайте .env файл по примеру .env.example и укажите доступ к БД и Google Sheets.

4. Запустите приложение:

```
uvicorn app.main:app --reload
```

## Эндпоинты

- POST / — создать локацию (возвращает GeoJSON).

Пример запроса:

```
{ "name: 'Moscow'  # Опциональный параметр
  "lon": 31.1,
  "lat": 65.12,
  "radius": 500
}
```

---

Ссылка на [Google Sheets](https://docs.google.com/spreadsheets/d/1C35kpV9UfKaBHL0VwxU7SWIFhQD0ymqeZuGBqKI1vY0/edit?pli=1&gid=0#gid=0)

---

Для проверки работы я могу залить в репозиторий файл `data-table.json` с данными от сервисного аккаунта.

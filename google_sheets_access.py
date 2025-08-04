import os
import gspread
import asyncio
from typing import List
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials


# Загружаем переменные окружения
load_dotenv()

# Файл сервисного аккаунта и URL таблицы
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
SPREADSHEET_URL = os.getenv("SPREADSHEET_URL")

# Скоупы для работы с Google Sheets
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# Авторизация и открытие таблицы
_creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
_client = gspread.authorize(_creds)
_spreadsheet = _client.open_by_url(SPREADSHEET_URL)
_sheet = _spreadsheet.sheet1


async def append_row(row: List[str]) -> None:
    """
    Добавляет одну строку в Google Sheets.
    """
    return await asyncio.to_thread(_sheet.append_row, row)

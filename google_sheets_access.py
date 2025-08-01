import os
import gspread
import asyncio
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials


load_dotenv()


SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
SPREADSHEET_URL = os.getenv("SPREADSHEET_URL")
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# Авторизация
_creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
_client = gspread.authorize(_creds)
_spreadsheet = _client.open_by_url(SPREADSHEET_URL)
_sheet = _spreadsheet.sheet1


async def append_row(row: list):
    """
    Добавляет одну строку в таблицу.
    """
    return await asyncio.to_thread(_sheet.append_row, row)


async def get_all_values():
    """
    Возвращает все строки таблицы как список списков.
    """
    return await asyncio.to_thread(_sheet.get_all_values)

import math
from fastapi import FastAPI
from models import Location
from google_sheets_access import append_row, get_all_values


app = FastAPI()


@app.post("/")
async def save_and_convert_coordinates(coords: Location):
    coverage_area = coords.radius * math.pi
    return append_row(coords)


append_row(["sffd", "esgsg", 38])

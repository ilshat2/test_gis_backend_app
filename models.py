from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
import uuid


class Location(BaseModel):
    id: str = str(uuid.uuid4())
    date: str = str(datetime.now())
    name: str = None
    lat: Decimal
    lon: Decimal
    radius: Decimal


loc = Location(name="Нью-Васюки", lat=16.3248242424942942043, lon=19, radius=5)

#print(loc.id)

from pydantic import BaseModel
from decimal import Decimal
import uuid


class Location(BaseModel):
    id: str = str(uuid.uuid4())
    name: str = None
    lat: Decimal
    lon: Decimal


loc = Location(name="Нью-Васюки", lat=16.3248242424942942043, lon=19)
print(loc)

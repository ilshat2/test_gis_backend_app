import uuid
from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime


class Location(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    date: str = Field(default_factory=lambda: str(datetime.now()))
    name: str = None
    lon: Decimal
    lat: Decimal
    radius: Decimal

    def to_row(self, sq):
        """
        Возвращает данные в виде списка для записи в таблицу.
        """
        base = [
            self.id,
            self.date,
            self.name,
            str(self.lat),
            str(self.lon),
            str(self.radius),
        ]
        base.append(sq)
        return base

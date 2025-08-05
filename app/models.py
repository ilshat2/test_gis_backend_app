import uuid
from decimal import Decimal
from typing import Any
from datetime import datetime
from pydantic_core import ErrorDetails, PydanticCustomError
from pydantic import BaseModel, Field, model_validator, ValidationError


class Location(BaseModel):
    """
    Pydantic-модель для валидации данных локации.
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    date: datetime = Field(default_factory=datetime.now)
    name: str = Field(None, max_length=50)
    lon: Decimal = Field(
        ..., ge=-180, le=180, description="Долгота в градусах (-180..180)"
    )
    lat: Decimal = Field(..., gt=-90, le=90, description="Широта в градусах (-90..90)")
    radius: Decimal = Field(
        ..., gt=0, le=10000, description="Радиус в метрах (0..10000)"
    )

    @model_validator(mode="before")
    @classmethod
    def check_all(cls, values: dict[str, Any]) -> dict:
        """
        Проверяет поля модели и собирает все ошибки.
        """
        errors: list[ErrorDetails] = []

        lon = values.get("lon")
        lat = values.get("lat")
        radius = values.get("radius")

        if lon is None or not (-180 <= float(lon) <= 180):
            errors.append(
                ErrorDetails(
                    type=PydanticCustomError(
                        "value_error",
                        "Долгота должна быть в диапазоне от -180 до 180 градусов.",
                        {"value": lon},
                    ),
                    loc=("lon",),
                    input=lon,
                )
            )

        if lat is None or not (-90 <= float(lat) <= 90):
            errors.append(
                ErrorDetails(
                    type=PydanticCustomError(
                        "value_error",
                        "Широта должна быть в диапазоне от -90 до 90 градусов.",
                        {"value": lat},
                    ),
                    loc=("lat",),
                    input=lat,
                )
            )

        if radius is None or not (0 < float(radius) <= 10000):
            errors.append(
                ErrorDetails(
                    type=PydanticCustomError(
                        "value_error",
                        "Радиус должен быть положительным и не больше 10000 метров.",
                        {"value": radius},
                    ),
                    loc=("radius",),
                    input=radius,
                )
            )

        if errors:
            raise ValidationError.from_exception_data(
                title="ValidationError", line_errors=errors
            )

        return values

    def to_row(self, sq: str) -> list[str]:
        """
        Преобразует данные в список для записи в Google Sheets.
        """
        return [
            self.id,
            self.date.isoformat(),
            self.name,
            str(self.lat),
            str(self.lon),
            str(self.radius),
            sq,
        ]

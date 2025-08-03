import datetime
from db import Base
from sqlalchemy import Column, String, Numeric, JSON, TIMESTAMP


class LocationCache(Base):
    """
    Модель кэша в postgresql.
    Хранит данные о локациях с готовым geojson.
    """

    __tablename__ = "location_cache"

    id = Column(String, primary_key=True, index=True)
    date = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    name = Column(String)
    lon = Column(Numeric)
    lat = Column(Numeric)
    radius = Column(Numeric)
    coverage_area = Column(Numeric)
    geojson = Column(JSON)

import math
from google_sheets_access import append_row
from models import Location
from decimal import Decimal


class LocationService:
    async def save_location(self, data: Location):
        coverage_area = data.radius**2 * Decimal(str(math.pi))
        await append_row(data.to_row(str(coverage_area)))

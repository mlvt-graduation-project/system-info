from pydantic import BaseModel

class DayMonthYearRequest(BaseModel):
    """Represents the request body for converting a day/month/year to timestamp."""
    day: int
    month: int
    year: int

class TimestampResponse(BaseModel):
    """Represents the response body containing the timestamp or any error message."""
    timestamp: int | None = None
    error: str | None = None
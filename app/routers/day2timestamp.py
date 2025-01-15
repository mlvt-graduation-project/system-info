from fastapi import APIRouter
from .schemas import DayMonthYearRequest, TimestampResponse
from ..utils.convert_day import ConvertDayToTimestamp

router = APIRouter()

@router.post("/timestamp", response_model=TimestampResponse)
def get_timestamp(body: DayMonthYearRequest) -> TimestampResponse:
    """
    Return the unix timestamp for given day, month, year.

    Example request body:
        {
          "day": 15,
          "month": 1,
          "year": 2025
        }
    """
    timestamp, err = ConvertDayToTimestamp(body.day, body.month, body.year)
    if err:
        return TimestampResponse(error=err)
    return TimestampResponse(timestamp=timestamp)
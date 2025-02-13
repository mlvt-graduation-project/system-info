from fastapi import APIRouter
from .schemas import DayMonthYearRequest, TimestampResponse
from ..utils.convert_day import ConvertDayToTimestamp
from ..utils.logging_setup import GetLogger

router = APIRouter()
logger = GetLogger()

@router.post("/timestamp", response_model=TimestampResponse)
def GetTimestamp(body: DayMonthYearRequest) -> TimestampResponse:
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
        logger.error(f"Error converting date: {err}")
        return TimestampResponse(error=err)
    logger.info(f"Successfully converted to timestamp={timestamp}")
    return TimestampResponse(timestamp=timestamp)
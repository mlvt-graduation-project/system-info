from fastapi import APIRouter
from .schemas import DayMonthYearRequest, TimestampResponse
from ..utils.convert_day import ConvertDayToTimestamp
from ..utils.logging_setup import get_logger

router = APIRouter()
logger = get_logger()

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
    logger.info(f"Received request: day={DayMonthYearRequest.day}, month={DayMonthYearRequest.month}, year={DayMonthYearRequest.year}")
    timestamp, err = ConvertDayToTimestamp(body.day, body.month, body.year)
    if err:
        logger.error(f"Error converting date: {err}")
        return TimestampResponse(error=err)
    logger.info(f"Successfully converted to timestamp={timestamp}")
    return TimestampResponse(timestamp=timestamp)
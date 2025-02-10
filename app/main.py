from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager
from .routers.day2timestamp import router as day2timestamp_router
from .utils.logging_setup import GetLogger
from app.database.MongoDB_connect import MongoDBManager
from app.database.Postgres_connect import PostgresManager

logger = GetLogger()

async def lifespan(app: FastAPI):
    # define the startup tasks
    logger.info("Application startup")
    logger.info("Start connecting to Postgres")
    PostgresDB = PostgresManager()
    PostgresDB.initializePool(minConn= 1, maxConn=20)
    logger.info("Start connecting to MongoDB")
    MongoDB = MongoDBManager()
    MongoDB.connect()
    yield
    # define shutdown tasks
    logger.info("Application shutdown")
    PostgresDB.closePool()
    MongoDB.disconnect()


app = FastAPI(lifespan=lifespan)


app.include_router(day2timestamp_router, prefix="/day2timestamp", tags=["Day2Timestamp"])

# Custom handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()} | Body: {await request.body()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body if hasattr(exc, 'body') else None},
    )


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
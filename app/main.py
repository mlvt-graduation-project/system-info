from fastapi import FastAPI
import uvicorn

# IMPORTANT: Must reference `routers` (plural), 
# since your folder is now named `routers`
from .routers.day2timestamp import router as day2timestamp_router

app = FastAPI()

app.include_router(day2timestamp_router, prefix="/day2timestamp", tags=["Day2Timestamp"])

@app.get("/")
def read_root():
    return {"message": "Hello World!"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

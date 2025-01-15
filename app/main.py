from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routers import my_router

app = FastAPI(title="My FastAPI App")

# Optional: Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router
app.include_router(my_router.router, prefix="/api", tags=["API"])

@app.on_event("startup")
def on_startup():
    # Optional startup tasks: database migrations, etc.
    pass

@app.on_event("shutdown")
def on_shutdown():
    # Optional cleanup tasks
    pass
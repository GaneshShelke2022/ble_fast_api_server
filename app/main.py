import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import get_settings
from .routers import room_router, board_router, device_router, state_router, websocket_router
from .auth import auth_router
from .database import engine, Base
from .utils.logger import logger
from .middleware.auth_middleware import JWTAuthMiddleware
from sqlalchemy.ext.asyncio import AsyncEngine

settings = get_settings()

app = FastAPI(title="BLE Mesh Smart Home Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT middleware
app.add_middleware(JWTAuthMiddleware)

# include routers
app.include_router(auth_router.router)
app.include_router(room_router.router)
app.include_router(board_router.router)
app.include_router(device_router.router)
app.include_router(state_router.router)
app.include_router(websocket_router.router)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting BLE Mesh backend...")
    # create tables if not exist (for quick start). For production use Alembic.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables ensured")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

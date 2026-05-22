import logging
import os
import tomllib
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fasttwilio.db_manager import db_client
from fasttwilio.routers.auth_router import auth_router
from fasttwilio.routers.student_router import student_router
from fasttwilio.routers.twilio_router import twilio_router
from fasttwilio.routers.notification_router import notification_router

logger = logging.getLogger(__name__)


# get project version from pyproject.toml
version = "0.0.1"
with open(Path(__file__).parent.parent / "pyproject.toml", "rb") as f:
    toml_dict = tomllib.load(f)
    version = toml_dict["project"]["version"]


@asynccontextmanager
async def db_lifespan(app: FastAPI):
    """FastAPI lifespan function to initialize mongo client collection

    Args:
        app (FastAPI): FastAPI app
    """
    await db_client.init_db()
    yield
    await db_client.close()


app = FastAPI(
    title="Lab FastAPI and Twilio",
    description="Notification Service with Twilio and MongoDB",
    version=version,
    lifespan=db_lifespan,
)

# cors
origins = os.getenv("CORS_ORIGINS", "[]")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(twilio_router)
app.include_router(student_router)
app.include_router(auth_router)
app.include_router(notification_router)


@app.get("/health")
async def health_check():
    """health check endpoint
    Returns:
        json: status ok
    """
    return {"status": "ok"}

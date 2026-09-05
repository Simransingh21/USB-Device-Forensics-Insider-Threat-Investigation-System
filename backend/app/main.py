from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine

import app.models.usb_device
import app.models.finding
import app.models.scan
import app.models.event_log

from app.api import usb
from app.api import dashboard
from app.api import registry
from app.api import scan
from app.api import timeline
from app.api import suspicious
from app.api import report


# --------------------------------------------------
# Database Initialization
# --------------------------------------------------

Base.metadata.create_all(bind=engine)


# --------------------------------------------------
# FastAPI Application
# --------------------------------------------------

app = FastAPI(
    title="USB Device Forensics API",
    description=(
        "Backend API for USB Device Forensics and "
        "Insider Threat Investigation System"
    ),
    version="1.0.0"
)


# --------------------------------------------------
# CORS Configuration
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# API Routers
# --------------------------------------------------

app.include_router(usb.router)
app.include_router(registry.router)
app.include_router(scan.router)
app.include_router(timeline.router)
app.include_router(dashboard.router)
app.include_router(suspicious.router)
app.include_router(report.router)


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Welcome to USB Device Forensics API",
        "status": "Running Successfully"
    }


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "Healthy",
        "server": "FastAPI"
    }
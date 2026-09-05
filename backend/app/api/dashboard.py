from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.database import get_db
from app.models.scan import Scan
from app.models.usb_device import USBDevice
from app.models.event_log import EventLog
from app.models.finding import Finding
from app.utils.logger import logger

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def dashboard(db: Session = Depends(get_db)):

    logger.info("Loading dashboard statistics.")

    total_scans = db.query(Scan).count()
    total_usb = db.query(USBDevice).count()
    total_logs = db.query(EventLog).count()
    total_findings = db.query(Finding).count()

    last_scan = (
        db.query(func.max(Scan.start_time))
        .scalar()
    )

    logger.info("Dashboard statistics loaded successfully.")

    return {
        "success": True,
        "message": "Dashboard loaded successfully.",
        "data": {
            "total_scans": total_scans,
            "total_usb_devices": total_usb,
            "total_event_logs": total_logs,
            "total_findings": total_findings,
            "last_scan": last_scan,
            "system_health": "Healthy"
        }
    }
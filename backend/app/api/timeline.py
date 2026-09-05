from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.event_log import EventLog
from app.utils.logger import logger

router = APIRouter(
    prefix="/timeline",
    tags=["Timeline"]
)


def format_event(source: str):

    source = source.lower()

    if "kernel-pnp" in source:
        return "USB Device Connected"

    if "driverframeworks" in source:
        return "USB Driver Initialized"

    if "disk" in source:
        return "Storage Device Detected"

    if "partition" in source:
        return "Volume Mounted"

    if "bsthusb" in source or "bthusb" in source:
        return "Bluetooth USB Activity"

    return source


@router.get("/{scan_id}")
def get_timeline(
    scan_id: int,
    db: Session = Depends(get_db)
):

    logger.info(f"Loading timeline for Scan ID {scan_id}")

    events = (
        db.query(EventLog)
        .filter(EventLog.scan_id == scan_id)
        .order_by(EventLog.timestamp)
        .all()
    )

    timeline = []

    for event in events:

        timeline.append({

            "time": event.timestamp,

            "event_id": event.event_id,

            "source": format_event(event.source)

        })

    logger.info(f"Timeline loaded with {len(timeline)} events.")

    return {
        "success": True,
        "message": "Timeline fetched successfully.",
        "data": {
            "scan_id": scan_id,
            "events": timeline
        }
    }
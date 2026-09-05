from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.event_log import EventLog
from app.services.suspicious_service import SuspiciousService
from app.utils.logger import logger

router = APIRouter(
    prefix="/suspicious",
    tags=["Suspicious Activity"]
)


@router.get("/{scan_id}")
def suspicious(scan_id: int, db: Session = Depends(get_db)):

    logger.info(f"Analyzing suspicious activity for Scan ID {scan_id}")

    events = (
        db.query(EventLog)
        .filter(EventLog.scan_id == scan_id)
        .all()
    )

    findings = SuspiciousService().analyze(events)

    logger.info(f"Found {len(findings)} suspicious finding(s).")

    return {
        "success": True,
        "message": "Suspicious activity analysis completed.",
        "data": {
            "scan_id": scan_id,
            "total_findings": len(findings),
            "findings": findings
        }
    }
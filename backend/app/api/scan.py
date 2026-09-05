from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.scan_service import ScanService
from app.forensic.scan_engine import ScanEngine
from app.services.eventlog_service import EventLogService
from app.services.suspicious_service import SuspiciousService
from app.services.finding_service import FindingService
from app.utils.logger import logger

router = APIRouter(
    prefix="/scan",
    tags=["Scan"]
)


@router.post("/start")
def start_scan(db: Session = Depends(get_db)):

    logger.info("Starting new forensic investigation.")

    scan_service = ScanService()

    scan = scan_service.start_scan(db)

    logger.info(f"Created Scan ID: {scan.id}")

    engine = ScanEngine()

    logger.info("Running forensic scan engine.")

    results = engine.run_scan()

    events = results["event_logs"]

    logger.info(f"Collected {len(events)} event(s) from scan engine.")

    class FakeEvent:
        def __init__(self, event):
            self.source = event["source"]
            self.timestamp = event["time"]

    fake_events = [FakeEvent(event) for event in events]

    logger.info("Analyzing suspicious activities.")

    findings = SuspiciousService().analyze(fake_events)

    logger.info(f"Generated {len(findings)} suspicious finding(s).")

    FindingService().save_findings(
        db,
        scan.id,
        findings
    )

    logger.info("Suspicious findings saved to database.")

    event_service = EventLogService()

    logger.info("Saving event logs to database.")

    event_service.save_events(
        db,
        scan.id,
        events
    )

    artifacts = (
        results["summary"]["registry_devices"]
        +
        results["summary"]["event_logs"]
    )

    logger.info(
        f"Total forensic artifacts collected: {artifacts}"
    )

    completed_scan = scan_service.finish_scan(
        db,
        scan,
        artifacts
    )

    logger.info(
        f"Investigation completed successfully. Scan ID: {completed_scan.id}"
    )

    return {
        "success": True,
        "message": "Forensic investigation completed successfully.",
        "data": {
            "scan_id": completed_scan.id,
            "status": completed_scan.status,
            "summary": results["summary"],
            "results": results
        }
    }
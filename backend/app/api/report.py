from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.event_log import EventLog
from app.reports.pdf_report import PDFReport
from app.services.suspicious_service import SuspiciousService
from app.utils.logger import logger

router = APIRouter(
    prefix="/report",
    tags=["Report"]
)


@router.get("/{scan_id}")
def generate_report(
    scan_id: int,
    db: Session = Depends(get_db)
):

    logger.info(f"Generating report for Scan ID {scan_id}")

    timeline = (
        db.query(EventLog)
        .filter(EventLog.scan_id == scan_id)
        .all()
    )

    suspicious = SuspiciousService().analyze(
        timeline
    )

    filename = PDFReport().generate(
        scan_id,
        timeline,
        suspicious
    )

    logger.info("Report generated successfully.")

    return FileResponse(
        filename,
        media_type="application/pdf",
        filename=f"scan_{scan_id}.pdf"
    )
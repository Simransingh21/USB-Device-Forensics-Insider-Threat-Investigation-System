from datetime import datetime

from sqlalchemy.orm import Session

from app.models.scan import Scan


class ScanService:

    def start_scan(self, db: Session):

        scan = Scan(
            start_time=datetime.utcnow(),
            status="Running",
            total_artifacts=0
        )

        db.add(scan)
        db.commit()
        db.refresh(scan)

        return scan

    def finish_scan(
        self,
        db: Session,
        scan: Scan,
        artifacts: int
    ):

        scan.end_time = datetime.utcnow()

        scan.status = "Completed"

        scan.total_artifacts = artifacts

        db.commit()

        db.refresh(scan)

        return scan
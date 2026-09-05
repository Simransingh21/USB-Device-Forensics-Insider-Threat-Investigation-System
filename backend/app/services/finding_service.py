from sqlalchemy.orm import Session

from app.models.finding import Finding


class FindingService:

    def save_findings(
        self,
        db: Session,
        scan_id: int,
        findings: list
    ):

        for finding in findings:

            db.add(

                Finding(

                    scan_id=scan_id,

                    severity=finding["severity"],

                    title=finding["reason"],

                    description=finding["reason"],

                    timestamp=finding["time"]

                )

            )

        db.commit()
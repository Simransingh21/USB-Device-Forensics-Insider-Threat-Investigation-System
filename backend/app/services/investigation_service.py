from app.forensic.scan_engine import ScanEngine
from app.services.eventlog_service import EventLogService
from app.services.suspicious_service import SuspiciousService
from app.services.finding_service import FindingService


class FakeEvent:

    def __init__(self, event):

        self.source = event["source"]

        self.timestamp = event["time"]


class InvestigationService:

    def run(self, db, scan):

        engine = ScanEngine()

        results = engine.run_scan()

        EventLogService().save_events(
            db,
            scan.id,
            results["event_logs"]
        )

        fake_events = [

            FakeEvent(e)

            for e in results["event_logs"]

        ]

        findings = SuspiciousService().analyze(
            fake_events
        )

        FindingService().save_findings(
            db,
            scan.id,
            findings
        )

        return results, findings
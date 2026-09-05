from sqlalchemy.orm import Session

from app.models.event_log import EventLog


class EventLogService:

    def save_events(
        self,
        db: Session,
        scan_id: int,
        events: list
    ):

        for event in events:

            log = EventLog(

                scan_id=scan_id,

                event_id=event["event_id"],

                source=event["source"],

                timestamp=event["time"]

            )

            db.add(log)

        db.commit()
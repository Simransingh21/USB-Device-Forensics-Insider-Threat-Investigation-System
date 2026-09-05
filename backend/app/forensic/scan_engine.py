from app.forensic.collectors.registry_collector import RegistryCollector
from app.forensic.eventlog_collector import EventLogCollector


class ScanEngine:

    def run_scan(self):

        registry_collector = RegistryCollector()
        eventlog_collector = EventLogCollector()

        registry_result = registry_collector.collect()
        eventlog_result = eventlog_collector.collect()

        return {
            "registry": registry_result,
            "event_logs": eventlog_result,
            "summary": {
                "registry_devices": len(
                    registry_result.get("devices", [])
                ),
                "event_logs": len(eventlog_result)
            }
        }
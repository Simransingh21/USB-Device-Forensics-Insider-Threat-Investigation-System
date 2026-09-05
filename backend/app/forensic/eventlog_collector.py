import win32evtlog

from app.utils.logger import logger

USB_KEYWORDS = [
    "USB",
    "USBSTOR",
    "Disk",
    "Volume",
    "Removable",
    "Storage",
    "DriverFrameworks",
    "Kernel-PnP",
    "Partition"
]


class EventLogCollector:

    LOG_NAME = "System"

    def collect(self):

        logger.info("Starting Windows Event Log collection.")

        usb_events = []

        try:

            server = "localhost"

            handle = win32evtlog.OpenEventLog(
                server,
                self.LOG_NAME
            )

            flags = (
                win32evtlog.EVENTLOG_BACKWARDS_READ
                |
                win32evtlog.EVENTLOG_SEQUENTIAL_READ
            )

            scanned = 0

            while scanned < 500:

                events = win32evtlog.ReadEventLog(
                    handle,
                    flags,
                    0
                )

                if not events:
                    break

                for event in events:

                    scanned += 1

                    source = str(event.SourceName)

                    if any(
                        keyword.lower() in source.lower()
                        for keyword in USB_KEYWORDS
                    ):

                        usb_events.append({

                            "event_id": event.EventID & 0xFFFF,

                            "source": source,

                            "time": str(event.TimeGenerated)

                        })

            logger.info(
                f"Event Log collection completed. "
                f"Scanned {scanned} events and found {len(usb_events)} USB-related event(s)."
            )

            return usb_events

        except Exception as e:

            logger.error(
                f"Failed to collect Windows Event Logs: {str(e)}"
            )

            return []
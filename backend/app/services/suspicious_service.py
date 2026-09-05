from datetime import datetime


class SuspiciousService:

    def analyze(self, events):

        suspicious = []

        for event in events:

            source = event.source.lower()

            timestamp = event.timestamp

            # Rule 1
            if "kernel-pnp" in source:

                suspicious.append({
                    "severity": "LOW",
                    "reason": "USB Device Connected",
                    "time": timestamp
                })

            # Rule 2
            if "driverframeworks" in source:

                suspicious.append({
                    "severity": "MEDIUM",
                    "reason": "USB Driver Loaded",
                    "time": timestamp
                })

            # Rule 3
            try:
                hour = datetime.fromisoformat(timestamp).hour

                if hour >= 20 or hour <= 6:

                    suspicious.append({
                        "severity": "HIGH",
                        "reason": "USB Activity Outside Office Hours",
                        "time": timestamp
                    })

            except Exception:
                pass

        return suspicious
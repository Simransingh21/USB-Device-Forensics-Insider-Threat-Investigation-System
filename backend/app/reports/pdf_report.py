import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.utils.logger import logger


class PDFReport:

    def format_source(self, source):

        source = source.lower()

        if "kernel-pnp" in source:
            return "USB Device Connected"

        if "driverframeworks" in source:
            return "USB Driver Initialized"

        if "disk" in source:
            return "Storage Device Detected"

        if "partition" in source:
            return "Volume Mounted"

        if "bthusb" in source:
            return "Bluetooth USB Activity"

        return source

    def generate(self, scan_id, timeline, suspicious):

        logger.info(f"Generating PDF report for Scan ID {scan_id}.")

        os.makedirs("reports", exist_ok=True)

        filename = f"reports/scan_{scan_id}.pdf"

        doc = SimpleDocTemplate(filename)

        styles = getSampleStyleSheet()

        story = []

        # -------------------------
        # Title
        # -------------------------

        story.append(
            Paragraph(
                "<font size=22><b>USB DEVICE FORENSICS INVESTIGATION REPORT</b></font>",
                styles["Title"],
            )
        )

        story.append(Spacer(1, 20))

        # -------------------------
        # Investigation Summary
        # -------------------------

        summary = [

            ["Scan ID", str(scan_id)],

            ["Scan Status", "Completed"],

            ["Generated On", datetime.now().strftime("%d %B %Y %H:%M:%S")],

            ["Total Events", str(len(timeline))],

            ["Suspicious Findings", str(len(suspicious))]
        ]

        table = Table(summary, colWidths=[170, 280])

        table.setStyle(

            TableStyle([

                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),

                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

                ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),

                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),

                ("TOPPADDING", (0, 0), (-1, -1), 8),

                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),

            ])

        )

        story.append(table)

        story.append(Spacer(1, 25))

        # -------------------------
        # Timeline
        # -------------------------

        story.append(
            Paragraph(
                "<b><font size=16>Investigation Timeline</font></b>",
                styles["Heading2"]
            )
        )

        story.append(Spacer(1, 10))

        for event in timeline:

            description = self.format_source(event.source)

            story.append(
                Paragraph(
                    f"<b>{event.timestamp}</b>",
                    styles["BodyText"]
                )
            )

            story.append(
                Paragraph(
                    description,
                    styles["BodyText"]
                )
            )

            story.append(Spacer(1, 6))

        story.append(Spacer(1, 20))

        # -------------------------
        # Suspicious Findings
        # -------------------------

        story.append(
            Paragraph(
                "<b><font size=16>Suspicious Findings</font></b>",
                styles["Heading2"]
            )
        )

        story.append(Spacer(1, 10))

        if len(suspicious) == 0:

            story.append(
                Paragraph(
                    "No suspicious activity detected.",
                    styles["BodyText"]
                )
            )

        else:

            for finding in suspicious:

                story.append(
                    Paragraph(
                        f"<b>{finding['severity']}</b>",
                        styles["BodyText"]
                    )
                )

                story.append(
                    Paragraph(
                        finding["reason"],
                        styles["BodyText"]
                    )
                )

                story.append(
                    Paragraph(
                        finding["time"],
                        styles["BodyText"]
                    )
                )

                story.append(Spacer(1, 8))

        story.append(Spacer(1, 20))

        # -------------------------
        # Investigation Conclusion
        # -------------------------

        story.append(
            Paragraph(
                "<b><font size=16>Investigator Conclusion</font></b>",
                styles["Heading2"]
            )
        )

        story.append(Spacer(1, 8))

        if len(timeline) == 0:

            conclusion = """
            No forensic artifacts were discovered during this investigation.
            """

        else:

            conclusion = f"""
            This investigation analyzed <b>{len(timeline)}</b> Windows system
            events and identified <b>{len(suspicious)}</b> potentially suspicious
            activities.

            No USB storage device registry artifacts were found on this system.
            The collected evidence should be reviewed together with Windows Event
            Logs before reaching a final forensic conclusion.
            """

        story.append(
            Paragraph(
                conclusion,
                styles["BodyText"]
            )
        )

        story.append(Spacer(1, 30))

        story.append(
            Paragraph(
                "<font size=9 color='grey'>"
                "Generated by USB Device Forensics & Insider Threat Investigation System"
                "</font>",
                styles["BodyText"]
            )
        )

        logger.info("Building PDF document.")

        doc.build(story)

        logger.info(
            f"PDF report generated successfully: {filename}"
        )

        return filename
import winreg

from app.utils.logger import logger


class RegistryCollector:

    USBSTOR = r"SYSTEM\CurrentControlSet\Enum\USBSTOR"

    def collect(self):

        logger.info("Starting Windows Registry scan for USB devices.")

        devices = []

        try:

            registry = winreg.ConnectRegistry(
                None,
                winreg.HKEY_LOCAL_MACHINE
            )

            key = winreg.OpenKey(
                registry,
                self.USBSTOR
            )

            count = winreg.QueryInfoKey(key)[0]

            logger.info(f"Found {count} USB device key(s) in USBSTOR registry.")

            for i in range(count):

                device = winreg.EnumKey(key, i)

                devices.append(device)

            logger.info(
                f"Registry scan completed successfully. "
                f"Collected {len(devices)} USB device(s)."
            )

            return {

                "artifact": "USBSTOR",

                "status": "Success",

                "count": len(devices),

                "devices": devices
            }

        except FileNotFoundError:

            logger.warning(
                "USBSTOR registry key not found. "
                "No USB storage device history exists on this system."
            )

            return {

                "artifact": "USBSTOR",

                "status": "Not Found",

                "devices": []

            }

        except Exception as e:

            logger.error(
                f"Registry scan failed: {str(e)}"
            )

            return {

                "artifact": "USBSTOR",

                "status": "Error",

                "message": str(e),

                "devices": []

            }
# import winreg

# USBSTOR_PATH = r"SYSTEM\CurrentControlSet\Enum\USBSTOR"


# def parse_device_name(device_key):

#     details = {
#         "manufacturer": "",
#         "product": "",
#         "revision": ""
#     }

#     parts = device_key.split("&")

#     for part in parts:

#         if part.startswith("Ven_"):
#             details["manufacturer"] = part.replace("Ven_", "")

#         elif part.startswith("Prod_"):
#             details["product"] = part.replace("Prod_", " ").replace("_", " ")

#         elif part.startswith("Rev_"):
#             details["revision"] = part.replace("Rev_", "")

#     return details


# def get_usb_devices():

#     devices = []

#     try:

#         registry = winreg.ConnectRegistry(
#             None,
#             winreg.HKEY_LOCAL_MACHINE
#         )

#         key = winreg.OpenKey(
#             registry,
#             USBSTOR_PATH
#         )

#         index = 0

#         while True:

#             try:

#                 device_key = winreg.EnumKey(
#                     key,
#                     index
#                 )

#                 parsed = parse_device_name(device_key)

#                 device_registry = winreg.OpenKey(
#                     key,
#                     device_key
#                 )

#                 serial_index = 0

#                 while True:

#                     try:

#                         serial = winreg.EnumKey(
#                             device_registry,
#                             serial_index
#                         )

#                         devices.append({

#                             "manufacturer": parsed["manufacturer"],

#                             "product": parsed["product"],

#                             "revision": parsed["revision"],

#                             "serial_number": serial

#                         })

#                         serial_index += 1

#                     except OSError:
#                         break

#                 index += 1

#             except OSError:
#                 break

#     except Exception as e:

#         print(e)

#     return devices

import winreg

USBSTOR_PATH = r"SYSTEM\CurrentControlSet\Enum\USBSTOR"


def get_usb_devices():

    devices = []

    try:
        registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)

        key = winreg.OpenKey(registry, USBSTOR_PATH)

        count = winreg.QueryInfoKey(key)[0]

        print(f"Found {count} USB device categories")

        for i in range(count):

            name = winreg.EnumKey(key, i)

            print(name)

            devices.append({
                "device": name
            })

    except Exception as e:
        print("Registry Error:", e)

    return devices
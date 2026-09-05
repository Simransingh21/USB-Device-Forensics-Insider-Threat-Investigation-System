from sqlalchemy.orm import Session

from app.models.usb_device import USBDevice
from app.schemas.usb_schema import USBDeviceCreate

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException


def create_usb_device(db: Session, usb: USBDeviceCreate):

    device = USBDevice(
        device_name=usb.device_name,
        manufacturer=usb.manufacturer,
        serial_number=usb.serial_number,
        vendor_id=usb.vendor_id,
        product_id=usb.product_id,
    )

    try:
        db.add(device)
        db.commit()
        db.refresh(device)
        return device

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="USB Device with this serial number already exists."
        )


def get_all_usb_devices(db: Session):
    return db.query(USBDevice).all()
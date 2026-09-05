from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.usb_schema import USBDeviceCreate, USBDeviceResponse
from app.services import usb_service

router = APIRouter(
    prefix="/usb",
    tags=["USB Devices"]
)


@router.post("/", response_model=USBDeviceResponse)
def create_usb(
    usb: USBDeviceCreate,
    db: Session = Depends(get_db)
):
    return usb_service.create_usb_device(db, usb)


@router.get("/", response_model=list[USBDeviceResponse])
def get_usb_devices(
    db: Session = Depends(get_db)
):
    return usb_service.get_all_usb_devices(db)
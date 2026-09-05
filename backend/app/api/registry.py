from fastapi import APIRouter

from app.forensic.registry_reader import get_usb_devices

router = APIRouter(
    prefix="/registry",
    tags=["Registry"]
)


@router.get("/usb")
def read_registry():

    return get_usb_devices()
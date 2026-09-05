from pydantic import BaseModel


class USBDeviceCreate(BaseModel):
    device_name: str
    manufacturer: str
    serial_number: str
    vendor_id: str
    product_id: str


class USBDeviceResponse(USBDeviceCreate):
    id: int

    class Config:
        from_attributes = True
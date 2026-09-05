from sqlalchemy import Column, Integer, String

from app.database.database import Base


class USBDevice(Base):
    __tablename__ = "usb_devices"

    id = Column(Integer, primary_key=True, index=True)

    device_name = Column(String, nullable=False)

    manufacturer = Column(String)

    serial_number = Column(String, unique=True)

    vendor_id = Column(String)

    product_id = Column(String)
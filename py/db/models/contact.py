import enum

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, ForeignKey, Integer, Enum
from sqlalchemy.orm import relation, relationship

from .base import BaseModel
from .country import Country


class ContactType(enum.Enum):
    EMAIL = "0"
    WEBSITE = "1"
    PHONE = "2"
    TELEGRAM = "3"
    FACEBOOK = "4"
    VK = "5"
    INSTAGRAM = "6"

    @classmethod
    def __call__(cls):
        return [value for name, value in vars(cls).items() if name.isupper()]


class Contact(BaseModel):
	__tablename__ = "contact"

	vendor_id = Column(Integer, ForeignKey("vendor.id", ondelete="CASCADE", onupdate="CASCADE"))

	type = Column(Enum(ContactType, values_callable=lambda obj: [e.value for e in obj]))
	value = Column(String(255), nullable=False)
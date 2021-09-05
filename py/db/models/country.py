from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String

from .base import BaseModel


class Country(BaseModel):
	__tablename__ = "country"

	name = Column(String(255))
	alpha2 = Column(String(2))
	alpha3 = Column(String(3))
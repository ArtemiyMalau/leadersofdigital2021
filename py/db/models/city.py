from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relation, relationship

from .base import BaseModel
from .country import Country


class City(BaseModel):
	__tablename__ = "city"

	country_id = Column(Integer, ForeignKey("country.id", ondelete="CASCADE", onupdate="CASCADE"))
	name = Column(String(255))


class CityWithCountry(City):
	country = relationship(Country, primaryjoin=City.country_id == Country.id)
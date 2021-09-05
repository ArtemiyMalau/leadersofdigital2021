from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relation, relationship

from .base import BaseModel


class Gisp(BaseModel):
	__tablename__ = "gisp"

	name = Column(String(255))

	@classmethod
	def get_or_create(cls, session, gisp_name):
		gisp = session.query(cls).filter(cls.name == gisp_name).first()

		if not gisp:
			gisp = cls(name=gisp_name)
			session.add(category)
			session.flush()

		return gisp

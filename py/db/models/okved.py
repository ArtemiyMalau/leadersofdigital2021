from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey

from .base import BaseModel


class OkvedSection(BaseModel):
	__tablename__ = "okved_section"

	code = Column(String(2))
	name = Column(String(255))


class Okved(BaseModel):
	__tablename__ = "okved_1"

	okved_section_id = Column(Integer, ForeignKey("okved_section.id", ondelete="CASCADE", onupdate="CASCADE"))
	parent_okved_id = Column(Integer, ForeignKey("okved_1.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=True)

	level = Column(Integer)
	code = Column(String(10))
	name = Column(String(1000))

	def __repr__(self):
		return "<{0.__class__.__name__}(id={0.id!r}, code={0.code}, name={0.name!r}, level={0.level})>".format(self)


class OkvedVendor(BaseModel):
	__tablename__ = "okved_1_vendor"

	okved_id = Column(Integer, ForeignKey('okved_1.id', ondelete='CASCADE'), nullable=False, index=True)
	vendor_id = Column(Integer, ForeignKey('vendor.id', ondelete='CASCADE'), nullable=False, index=True)


class Okved2(BaseModel):
	__tablename__ = "okved_2"

	okved_section_id = Column(Integer, ForeignKey("okved_section.id", ondelete="CASCADE", onupdate="CASCADE"))
	parent_okved_id = Column(Integer, ForeignKey("okved_2.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=True)

	level = Column(Integer)
	code = Column(String(10))
	name = Column(String(1000))

	def __repr__(self):
		return "<{0.__class__.__name__}(id={0.id!r}, code={0.code}, name={0.name!r}, level={0.level})>".format(self)


class Okved2Vendor(BaseModel):
	__tablename__ = "okved_2_vendor"

	okved_id = Column(Integer, ForeignKey('okved_2.id', ondelete='CASCADE'), nullable=False, index=True)
	vendor_id = Column(Integer, ForeignKey('vendor.id', ondelete='CASCADE'), nullable=False, index=True)
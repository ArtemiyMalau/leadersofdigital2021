from sqlalchemy import Column, String, Text, Numeric, ForeignKey, Integer, BigInteger

from .base import BaseModel, BaseModelCU


class Vendor(BaseModelCU):
	__tablename__ = "vendor"

	ogrn = Column(String(25), nullable=True)
	inn = Column(String(25), nullable=True)
	kpp = Column(String(25), nullable=True)

	city_id = Column(Integer, ForeignKey("city.id", ondelete="SETNULL"), nullable=True)
	gisp_id = Column(Integer, ForeignKey("gisp.id", ondelete="SETNULL"), nullable=True)

	name = Column(String(350), nullable=True)
	address = Column(String(350), nullable=True)
	responsible_person = Column(String(255), nullable=True)

	email = Column(String(255), nullable=True)
	website = Column(String(255), nullable=True)
	phone = Column(String(20), nullable=True)

	reg_data = Column(Integer, nullable=True)
	authorized_capital = Column(BigInteger, nullable=True)
	is_unfair_supplier = Column(Integer, nullable=True, default=0)

	rate_minpromtorg = Column(Integer, nullable=True)
	rate_backend = Column(Integer, nullable=True)
	rate_client = Column(Integer, nullable=True)


class VendorFinances(BaseModel):
	__tablename__  = "vendor_finances"

	vendor_id = Column(Integer, ForeignKey("vendor.id", ondelete="CASCADE"), nullable=False)

	year = Column(Integer, nullable=False)

	f_2110 = Column(BigInteger, nullable=True)
	f_2200 = Column(BigInteger, nullable=True)
	f_2100 = Column(BigInteger, nullable=True)
	f_2300 = Column(BigInteger, nullable=True)
	f_2400 = Column(BigInteger, nullable=True)
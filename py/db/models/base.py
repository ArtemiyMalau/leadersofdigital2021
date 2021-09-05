import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, TIMESTAMP

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class BaseModelC(BaseModel):
    __abstract__ = True

    created_at = Column(TIMESTAMP, nullable=False)


class BaseModelU(BaseModel):
    __abstract__ = True

    updated_at = Column(TIMESTAMP, nullable=False)


class BaseModelCU(BaseModelC, BaseModelU):
    __abstract__ = True
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import *


__all__ = ["engine", "session"]

engine = create_engine("{type}+mysqldb://{user}:{password}@{host}:{port}/{dbname}?charset={charset}".format(**config["db"]))

session_factory = sessionmaker(bind=engine)
session = session_factory()
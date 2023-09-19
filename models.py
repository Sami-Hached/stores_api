from sqlalchemy import Column, Integer, String

from database import Base


class StoresDB(Base):
    __tablename__ = "stores_DE"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, nullable=False)
    email = Column(String, unique=True)
    brand = Column(String, nullable=False)

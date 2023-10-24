from sqlalchemy import Column, String
from sqlalchemy.dialects import postgresql
from .database import Base
import uuid


class StoresDB(Base):
    __tablename__ = "stores_DE"

    id = Column(postgresql.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    city = Column(String, nullable=False)
    email = Column(String, unique=True)
    brand = Column(String, nullable=False)

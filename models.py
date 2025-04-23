from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Float, text


class Boss(Base):
    __tablename__ = "boss"
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))

from sqlalchemy import (
    Column, Integer, String, Float,
    DateTime, Text, ForeignKey
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class RawRequest(Base):
    __tablename__ = 'raw_requests'

    id        = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    url       = Column(String, nullable=False, index=True)
    status    = Column(Integer)
    body      = Column(Text)

    # relación a Odds
    odds      = relationship("Odds", back_populates="raw_request")


class Odds(Base):
    __tablename__ = 'odds'

    id             = Column(Integer, primary_key=True)
    timestamp      = Column(DateTime, nullable=False)
    match_id       = Column(String, index=True)
    market         = Column(String)
    outcome        = Column(String)
    odd            = Column(Float)
    raw_request_id = Column(Integer, ForeignKey('raw_requests.id'))

    raw_request    = relationship("RawRequest", back_populates="odds")
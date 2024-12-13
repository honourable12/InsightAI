from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from database import Base
import enum

class InputSourceType(enum.Enum):
    CSV = "csv"
    JSON = "json"
    API = "api"

class InputSource(Base):
    __tablename__ = "input_sources"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(InputSourceType), nullable=False)
    path = Column(String, nullable=False)
    api_key = Column(String, nullable=True)  # Only used for API sources
    description = Column(String, nullable=True)
    user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_analyzed_at = Column(DateTime(timezone=True), nullable=True)
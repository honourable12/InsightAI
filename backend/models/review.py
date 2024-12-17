from sqlalchemy import Column, Integer, String, Float, DateTime
#from sqlalchemy.orm import declarative_base
from datetime import datetime
from database import Base

#Base = declarative_base()

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    review_text = Column(String, nullable=False)
    source = Column(String, nullable=True)
    sentiment_category = Column(String, nullable=True)
    polarity = Column(Float, nullable=True)
    subjectivity = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
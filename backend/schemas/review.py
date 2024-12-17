from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    review_text: str
    source: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int
    review_text: str
    source: Optional[str] = None
    sentiment_category: Optional[str] = None
    polarity: Optional[float] = None
    subjectivity: Optional[float] = None
    created_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True
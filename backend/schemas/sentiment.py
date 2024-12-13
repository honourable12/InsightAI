from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class SentimentAnalysisRequest(BaseModel):
    text: str

class SentimentAnalysisResponse(BaseModel):
    text: str
    polarity: float
    subjectivity: float
    sentiment_category: str
    error: Optional[str] = None

class InputSourceCreate(BaseModel):
    type: str
    path: str
    api_key: Optional[str] = None
    description: Optional[str] = None

class InputSourceResponse(BaseModel):
    id: int
    type: str
    path: str
    description: Optional[str]
    created_at: datetime
    last_analyzed_at: Optional[datetime]

    class Config:
        orm_mode = True
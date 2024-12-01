# routes/review.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.sentiment_service import SentimentAnalyzer
from core.security import get_current_active_user
from models.user import User
from database import get_db

router = APIRouter()

@router.post("/analyze-sentiment")
def analyze_review_sentiment(
    text: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Analyze sentiment of the review
    sentiment_result = SentimentAnalyzer.analyze_sentiment(text)
    return sentiment_result
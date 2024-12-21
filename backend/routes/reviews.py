from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from typing import Dict
from collections import Counter
from datetime import datetime

from core.config import settings
from schemas.review import SentimentCountResponse
from services.review_service import ReviewService
from models.review import Review
from database import get_db

router = APIRouter()
review_service = ReviewService()


# Helper function to count sentiment categories for a specific batch
def count_sentiments_by_batch(db: Session, batch_id: str) -> Dict[str, int]:
    sentiment_counts = Counter(
        review.sentiment_category
        for review in db.query(Review)
        .filter(Review.batch_id == batch_id)
        .all()
    )

    # Ensure all categories are represented, even if count is 0
    all_categories = {
        "very_positive": 0,
        "positive": 0,
        "neutral": 0,
        "negative": 0,
        "very_negative": 0,
    }
    all_categories.update(sentiment_counts)
    return all_categories


@router.post("/import/csv", response_model=Dict[str, int])
async def import_csv_reviews(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    with open(file.filename, "wb") as buffer:
        buffer.write(await file.read())

    # Create a unique batch ID for this import
    batch_id = f"batch_{datetime.now().isoformat()}"

    # Import reviews from the CSV file
    review_service.import_reviews_from_csv(db, file.filename, batch_id=batch_id)

    # Count sentiment categories for the imported batch
    sentiment_counts = count_sentiments_by_batch(db, batch_id)

    return sentiment_counts


@router.post("/import/json", response_model=Dict[str, int])
async def import_json_reviews(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    with open(file.filename, "wb") as buffer:
        buffer.write(await file.read())

    # Create a unique batch ID for this import
    batch_id = f"batch_{datetime.now().isoformat()}"

    # Import reviews from the JSON file
    review_service.import_reviews_from_json(db, file.filename, batch_id=batch_id)

    # Count sentiment categories for the imported batch
    sentiment_counts = count_sentiments_by_batch(db, batch_id)

    return sentiment_counts

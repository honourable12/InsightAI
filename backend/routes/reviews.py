from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from typing import List

from core.config import settings
from schemas.review import ReviewResponse
from services.review_service import ReviewService
from models.review import Review
from database import get_db
router = APIRouter()
review_service = ReviewService()


@router.post("/import/csv", response_model = List[ReviewResponse])
async def import_csv_reviews(
	file: UploadFile = File(...),
	db: Session = Depends(get_db)
):
	with open(file.filename, "wb") as buffer:
		buffer.write(await file.read())

	# Get the imported reviews instead of the counter
	reviews = review_service.import_reviews_from_csv(db, file.filename)

	# Convert the reviews to ReviewResponse objects
	return [
		ReviewResponse(
			id = review.id,
			review_text = review.review_text,
			source = review.source,
			sentiment_category = review.sentiment_category,
			polarity = review.polarity,
			subjectivity = review.subjectivity
		) for review in db.query(Review).filter(Review.source == 'csv').all()
	]


@router.post("/import/json", response_model = List[ReviewResponse])
async def import_json_reviews(
	file: UploadFile = File(...),
	db: Session = Depends(get_db)
):
	with open(file.filename, "wb") as buffer:
		buffer.write(await file.read())

	# Get the imported reviews instead of the counter
	reviews = review_service.import_reviews_from_json(db, file.filename)

	# Convert the reviews to ReviewResponse objects if not already done
	return [
		ReviewResponse(
			id = review.id,
			review_text = review.review_text,
			source = review.source,
			sentiment_category = review.sentiment_category,
			polarity = review.polarity,
			subjectivity = review.subjectivity
		) for review in db.query(Review).filter(Review.source == 'json').all()
	]
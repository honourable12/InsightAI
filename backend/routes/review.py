from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List

from core.security import get_current_active_user
from database import get_db
from models.user import User
from schemas.input_source import InputSourceType
from schemas.sentiment import SentimentAnalysisRequest, SentimentAnalysisResponse
from services.sentiment_service import SentimentAnalyzer
from services.input_source_service import InputSourceService
from services.review_importer import ReviewImporter

router = APIRouter()


@router.post("/analyze-batch", response_model = dict)
def analyze_batch_sentiment(
	source_type: InputSourceType,
	path: str,
	api_key: Optional[str] = None,
	description: Optional[str] = None,
	current_user: User = Depends(get_current_active_user),
	db: Session = Depends(get_db)
):
	"""
    Analyze sentiment for a batch of reviews from various sources.

    - Stores input source in database
    - Supports CSV, JSON, and API sources
    - Requires authentication
    """
	try:
		# Create input source record
		input_source = InputSourceService.create_input_source(
			db,
			current_user,
			source_type,
			path,
			api_key,
			description
		)

		# Initialize review importer
		importer = ReviewImporter()

		# Process reviews based on source type
		if source_type == InputSourceType.CSV:
			sentiment_counts = importer.import_csv_reviews(path)
		elif source_type == InputSourceType.JSON:
			sentiment_counts = importer.import_json_reviews(path)
		elif source_type == InputSourceType.API:
			sentiment_counts = importer.import_api_reviews(path, api_key)
		else:
			raise HTTPException(status_code = 400, detail = "Unsupported source type")

		# Update last analyzed timestamp
		InputSourceService.update_last_analyzed(db, input_source.id)

		# Return sentiment summary
		return {
			"input_source_id": input_source.id,
			"sentiment_summary": dict(sentiment_counts)
		}

	except Exception as e:
		raise HTTPException(status_code = 500, detail = str(e))


@router.get("/input-sources", response_model = List[dict])
def list_input_sources(
	current_user: User = Depends(get_current_active_user),
	db: Session = Depends(get_db)
):
	"""
    List all input sources for the current user.

    - Requires authentication
    - Returns list of input sources
    """
	sources = InputSourceService.get_input_sources_by_user(db, current_user)
	return [
		{
			"id": source.id,
			"type": source.type.value,
			"path": source.path,
			"description": source.description,
			"created_at": source.created_at,
			"last_analyzed_at": source.last_analyzed_at
		}
		for source in sources
	]
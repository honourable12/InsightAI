from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
import json

from database import get_db
from models.dataset import Dataset, SentimentAnalysis
from schemas.dataset import DatasetResponse, AnalysisResponse
from services.dataset_service import DatasetService
from models.user import User
from core.security import get_current_user

router = APIRouter()
dataset_service = DatasetService()


@router.post("/dataset")
async def upload_dataset(
	file: UploadFile = File(...),
	name: str = Form(...),
	description: str = Form(None),
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db)
):
	# Validate file type
	file_type = file.filename.split('.')[-1].lower()
	if file_type not in ['csv', 'json']:
		raise HTTPException(
			status_code = 400,
			detail = "Invalid file type. Please upload a CSV or JSON file."
		)

	file_data = await file.read()

	try:
		# Read the file and validate
		df = dataset_service.read_file(file_data, file_type)
		if df.empty:
			raise HTTPException(
				status_code = 400,
				detail = "Uploaded file is empty."
			)

		# Detect text columns
		text_columns = dataset_service.detect_text_columns(df)

		# Create dataset record
		dataset = Dataset(
			user_id = current_user.id,
			name = name,
			description = description,
			file_data = file_data,
			file_type = file_type,
			columns = json.dumps(df.columns.tolist()),
			row_count = len(df)
		)
		db.add(dataset)
		db.commit()
		db.refresh(dataset)

		return {
			"message": "Dataset uploaded successfully",
			"dataset_id": dataset.id,
			"text_columns": text_columns
		}
	except Exception as e:
		raise HTTPException(
			status_code = 500,
			detail = f"An error occurred while processing the file: {str(e)}"
		)


@router.get("/datasets", response_model = List[DatasetResponse])
async def get_datasets(
	skip: int = Query(0, ge = 0),
	limit: int = Query(10, ge = 1, le = 100),
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db)
):
	datasets = db.query(Dataset) \
		.filter(Dataset.user_id == current_user.id) \
		.offset(skip) \
		.limit(limit) \
		.all()
	return datasets


@router.get("/dataset/{dataset_id}", response_model = DatasetResponse)
async def get_dataset(
	dataset_id: int,
	preview: bool = Query(False),
	preview_rows: int = Query(5, ge = 1, le = 100),
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db)
):
	dataset = db.query(Dataset) \
		.filter(Dataset.id == dataset_id, Dataset.user_id == current_user.id) \
		.first()

	if not dataset:
		raise HTTPException(status_code = 404, detail = "Dataset not found")

	response = DatasetResponse.from_orm(dataset)

	if preview:
		df = dataset_service.read_file(dataset.file_data, dataset.file_type)
		response.preview = dataset_service.get_dataset_preview(df, preview_rows)

	return response

@router.post("/dataset/{dataset_id}/analyze")
async def analyze_dataset(
	dataset_id: int,
	text_column: str,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db)
):
	# Fetch dataset
	dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
	if not dataset:
		raise HTTPException(status_code = 404, detail = "Dataset not found")

	try:
		# Read the dataset
		df = dataset_service.read_file(dataset.file_data, dataset.file_type)

		if text_column not in df.columns:
			raise HTTPException(
				status_code = 400,
				detail = f"Column '{text_column}' not found in dataset"
			)

		# Perform sentiment analysis
		results = []
		for text in df[text_column].fillna(""):
			sentiment = dataset_service.analyze_sentiment(text)
			category = dataset_service.categorize_sentiment(sentiment["polarity"])
			results.append({
				"text": text[:100],  # Store preview of text
				"sentiment": sentiment,
				"category": category
			})

		# Store analysis results
		analysis = SentimentAnalysis(
			dataset_id = dataset_id,
			text_column = text_column,
			results = results
		)
		db.add(analysis)
		db.commit()

		# Calculate summary statistics
		sentiment_counts = {}
		for result in results:
			category = result["category"]
			sentiment_counts[category] = sentiment_counts.get(category, 0) + 1

		return {
			"message": "Sentiment analysis completed",
			"analysis_id": analysis.id,
			"sentiment_counts": sentiment_counts,
			"sample_results": results[:5]  # Return first 5 results as sample
		}

	except Exception as e:
		raise HTTPException(
			status_code = 500,
			detail = f"An error occurred during analysis: {str(e)}"
		)


@router.get("/dataset/{dataset_id}/analyses", response_model = List[AnalysisResponse])
async def get_dataset_analyses(
	dataset_id: int,
	skip: int = Query(0, ge = 0),
	limit: int = Query(10, ge = 1, le = 100),
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db)
):
	dataset = db.query(Dataset) \
		.filter(Dataset.id == dataset_id, Dataset.user_id == current_user.id) \
		.first()

	if not dataset:
		raise HTTPException(status_code = 404, detail = "Dataset not found")

	analyses = db.query(SentimentAnalysis) \
		.filter(SentimentAnalysis.dataset_id == dataset_id) \
		.offset(skip) \
		.limit(limit) \
		.all()

	# Add sentiment counts to each analysis response
	for analysis in analyses:
		results = analysis.results
		sentiment_counts = {}
		for result in results:
			category = result["category"]
			sentiment_counts[category] = sentiment_counts.get(category, 0) + 1
		analysis.sentiment_counts = sentiment_counts
		analysis.sample_results = results[:5]  # Include first 5 results as sample

	return analyses


@router.get("/analysis/{analysis_id}", response_model = AnalysisResponse)
async def get_analysis(
	analysis_id: int,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db)
):
	analysis = db.query(SentimentAnalysis) \
		.join(Dataset) \
		.filter(
		SentimentAnalysis.id == analysis_id,
		Dataset.user_id == current_user.id
	).first()

	if not analysis:
		raise HTTPException(status_code = 404, detail = "Analysis not found")

	# Calculate sentiment counts
	results = analysis.results
	sentiment_counts = {}
	for result in results:
		category = result["category"]
		sentiment_counts[category] = sentiment_counts.get(category, 0) + 1

	analysis.sentiment_counts = sentiment_counts
	analysis.sample_results = results[:5]  # Include first 5 results as sample

	return analysis
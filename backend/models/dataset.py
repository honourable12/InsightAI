from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Dataset(Base):
	__tablename__ = "datasets"

	id = Column(Integer, primary_key = True, index = True)
	user_id = Column(Integer, ForeignKey("users.id"))
	name = Column(String, nullable = False)
	description = Column(String)
	file_data = Column(LargeBinary)
	file_type = Column(String)  # 'csv' or 'json'
	columns = Column(JSON)
	row_count = Column(Integer)
	created_at = Column(DateTime, default = datetime.utcnow)

	# Relationship to sentiment analysis results
	analysis_results = relationship("SentimentAnalysis", back_populates = "dataset")


class SentimentAnalysis(Base):
	__tablename__ = "sentiment_analyses"

	id = Column(Integer, primary_key = True, index = True)
	dataset_id = Column(Integer, ForeignKey("datasets.id"))
	text_column = Column(String)
	results = Column(JSON)  # Stores the sentiment analysis results
	created_at = Column(DateTime, default = datetime.utcnow)

	dataset = relationship("Dataset", back_populates = "analysis_results")
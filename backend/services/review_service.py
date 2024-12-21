import pandas as pd
from textblob import TextBlob
import logging
from sqlalchemy.orm import Session
from typing import List, Dict
from models.review import Review
from datetime import datetime

class ReviewService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        try:
            blob = TextBlob(str(text))
            return {
                "polarity": blob.sentiment.polarity,
                "subjectivity": blob.sentiment.subjectivity,
            }
        except Exception as e:
            self.logger.warning(f"Sentiment analysis error: {e}")
            return {"polarity": 0, "subjectivity": 0}

    def categorize_sentiment(self, polarity: float) -> str:
        if polarity > 0.5:
            return "very_positive"
        elif polarity > 0:
            return "positive"
        elif polarity == 0:
            return "neutral"
        elif polarity > -0.5:
            return "negative"
        else:
            return "very_negative"

    def import_reviews_from_csv(self, db: Session, file_path: str, batch_id: str) -> None:
        df = pd.read_csv(file_path, on_bad_lines = "skip")
        for _, row in df.iterrows():
            sentiment = self.analyze_sentiment(row["review_text"])
            review = Review(
                review_text = row["review_text"],
                source = "csv",
                sentiment_category = self.categorize_sentiment(sentiment["polarity"]),
                polarity = sentiment["polarity"],
                subjectivity = sentiment["subjectivity"],
                batch_id = batch_id,
                created_at = datetime.now(),
            )
            db.add(review)
        db.commit()

    def import_reviews_from_json(self, db: Session, file_path: str, batch_id: str) -> None:
        df = pd.read_json(file_path)
        for _, row in df.iterrows():
            sentiment = self.analyze_sentiment(row["review_text"])
            review = Review(
                review_text = row["review_text"],
                source = "json",
                sentiment_category = self.categorize_sentiment(sentiment["polarity"]),
                polarity = sentiment["polarity"],
                subjectivity = sentiment["subjectivity"],
                batch_id = batch_id,
                created_at = datetime.now(),
            )
            db.add(review)
        db.commit()

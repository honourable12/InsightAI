import pandas as pd
from textblob import TextBlob
import logging
from sqlalchemy.orm import Session
from typing import List, Dict
from collections import Counter
from models.review import Review


class ReviewService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        try:
            blob = TextBlob(str(text))
            return {
                "polarity": blob.sentiment.polarity,
                "subjectivity": blob.sentiment.subjectivity
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

    def import_reviews_from_csv(self, db: Session, file_path: str) -> List[Review]:
	    """
		Import reviews from a CSV file and save them to the database.
		Returns a list of imported reviews.
		"""
	    try:
		    df = pd.read_csv(file_path, on_bad_lines = "skip")
		    reviews = []

		    for _, row in df.iterrows():
			    sentiment = self.analyze_sentiment(row['review_text'])
			    review = Review(
				    review_text = row['review_text'],
				    source = 'csv',
				    sentiment_category = self.categorize_sentiment(sentiment['polarity']),
				    polarity = sentiment['polarity'],
				    subjectivity = sentiment['subjectivity']
			    )
			    db.add(review)
			    reviews.append(review)

		    db.commit()
		    return reviews
	    except Exception as e:
		    self.logger.error(f"CSV import error: {e}")
		    db.rollback()
		    return []

    def import_reviews_from_json(self, db: Session, file_path: str) -> List[Review]:
	    """
		Import reviews from a JSON file and save them to the database.
		Returns a list of imported reviews.
		"""
	    try:
		    df = pd.read_json(file_path)
		    reviews = []

		    for _, row in df.iterrows():
			    sentiment = self.analyze_sentiment(row['review_text'])
			    review = Review(
				    review_text = row['review_text'],
				    source = 'json',
				    sentiment_category = self.categorize_sentiment(sentiment['polarity']),
				    polarity = sentiment['polarity'],
				    subjectivity = sentiment['subjectivity']
			    )
			    db.add(review)
			    reviews.append(review)

		    db.commit()
		    return reviews
	    except Exception as e:
		    self.logger.error(f"JSON import error: {e}")
		    db.rollback()
		    return []
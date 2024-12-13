import csv
import json
import requests
from typing import List, Dict, Union
from textblob import TextBlob
import pandas as pd
import logging
from collections import Counter

class ReviewImporter:
    def __init__(self, log_level=logging.INFO):
        """
        Initialize the ReviewImporter with configurable logging.

        :param log_level: Logging level (default: logging.INFO)
        """
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(levelname)s: %(message)s"
        )
        self.logger = logging.getLogger(__name__)

    def _base_sentiment_import(self, reviews_data: pd.DataFrame) -> Counter:
        """
        Base method to process sentiment for a DataFrame of reviews.

        :param reviews_data: DataFrame containing reviews
        :return: Counter of sentiment categories
        """
        reviews_data["sentiment_category"] = reviews_data["review_text"].apply(
            lambda x: self._categorize_sentiment(self._analyze_sentiment(x)["polarity"])
        )
        return Counter(reviews_data["sentiment_category"])

    def import_csv_reviews(self, file_path: str) -> Counter:
        """
        Import reviews from a CSV file.

        :param file_path: Path to the CSV file.
        :return: Counter summarizing sentiment categories.
        """
        try:
            df = pd.read_csv(file_path, on_bad_lines="skip")
            return self._base_sentiment_import(df)
        except FileNotFoundError:
            self.logger.error(f"CSV file not found: {file_path}")
            return Counter()
        except Exception as e:
            self.logger.error(f"Error importing CSV: {e}")
            return Counter()

    def import_json_reviews(self, file_path: str) -> Counter:
        """
        Import reviews from a JSON file.

        :param file_path: Path to the JSON file.
        :return: Counter summarizing sentiment categories.
        """
        try:
            with open(file_path, "r") as file:
                reviews = json.load(file)
            df = pd.DataFrame(reviews)
            return self._base_sentiment_import(df)
        except FileNotFoundError:
            self.logger.error(f"JSON file not found: {file_path}")
            return Counter()
        except json.JSONDecodeError:
            self.logger.error(f"Invalid JSON format in {file_path}")
            return Counter()
        except Exception as e:
            self.logger.error(f"Error importing JSON: {e}")
            return Counter()

    def import_api_reviews(self, api_url: str, api_key: str = None) -> Counter:
        """
        Import reviews from an external API.

        :param api_url: URL of the API endpoint.
        :param api_key: Optional API authentication key.
        :return: Counter summarizing sentiment categories.
        """
        try:
            headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()

            reviews = response.json()
            df = pd.DataFrame(reviews)
            return self._base_sentiment_import(df)
        except requests.RequestException as e:
            self.logger.error(f"API request error: {e}")
            return Counter()
        except Exception as e:
            self.logger.error(f"Error processing API reviews: {e}")
            return Counter()

    def _analyze_sentiment(self, text: str) -> Dict[str, float]:
        """
        Perform sentiment analysis using TextBlob.

        :param text: Review text to analyze.
        :return: Dictionary with sentiment scores.
        """
        try:
            blob = TextBlob(str(text))
            return {"polarity": blob.sentiment.polarity, "subjectivity": blob.sentiment.subjectivity}
        except Exception as e:
            self.logger.warning(f"Sentiment analysis error: {e}")
            return {"polarity": 0, "subjectivity": 0}

    def _categorize_sentiment(self, polarity: float) -> str:
        """
        Categorize sentiment based on polarity score.

        :param polarity: Sentiment polarity score.
        :return: Sentiment category.
        """
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
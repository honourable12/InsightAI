import argparse
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

    def import_csv_reviews(self, file_path: str) -> Counter:
        """
        Import reviews from a CSV file.

        :param file_path: Path to the CSV file.
        :return: Counter summarizing sentiment categories.
        """
        try:
            df = pd.read_csv(file_path, on_bad_lines="skip")
            df["sentiment_category"] = df["review_text"].apply(
                lambda x: self._categorize_sentiment(self._analyze_sentiment(x)["polarity"])
            )
            return Counter(df["sentiment_category"])
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
            df["sentiment_category"] = df["review_text"].apply(
                lambda x: self._categorize_sentiment(self._analyze_sentiment(x)["polarity"])
            )
            return Counter(df["sentiment_category"])
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
            df["sentiment_category"] = df["review_text"].apply(
                lambda x: self._categorize_sentiment(self._analyze_sentiment(x)["polarity"])
            )
            return Counter(df["sentiment_category"])
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

    def batch_process_reviews(self, input_sources: List[Dict[str, Union[str, Dict]]]) -> Counter:
        """
        Process reviews from multiple sources in a single batch.

        :param input_sources: List of review sources with type and path/url.
        :return: Consolidated Counter summarizing sentiment categories.
        """
        total_counts = Counter()

        for source in input_sources:
            source_type = source.get("type", "").lower()
            source_path = source.get("path", "")

            if source_type == "csv":
                counts = self.import_csv_reviews(source_path)
            elif source_type == "json":
                counts = self.import_json_reviews(source_path)
            elif source_type == "api":
                counts = self.import_api_reviews(
                    source_path, source.get("api_key", None)
                )
            else:
                self.logger.warning(f"Unsupported source type: {source_type}")
                continue

            total_counts.update(counts)

        return total_counts


# Updated Main Function with Dynamic Input
def main():
    importer = ReviewImporter()

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Analyze sentiment from reviews.")
    parser.add_argument(
        "--type",
        choices=["csv", "json", "api"],
        required=True,
        help="Specify the input source type (csv, json, or api).",
    )
    parser.add_argument(
        "--path",
        required=True,
        help="Path to the CSV/JSON file or URL of the API endpoint.",
    )
    parser.add_argument(
        "--api_key",
        required=False,
        help="API key for authenticating API requests (only required for API source).",
    )
    args = parser.parse_args()

    # Process the selected source type
    if args.type == "csv":
        result = importer.import_csv_reviews(args.path)
    elif args.type == "json":
        result = importer.import_json_reviews(args.path)
    elif args.type == "api":
        result = importer.import_api_reviews(args.path, args.api_key)
    else:
        print("Invalid source type selected.")
        return

    # Output the result
    print("Sentiment Summary:", result)


if __name__ == "__main__":
    main()

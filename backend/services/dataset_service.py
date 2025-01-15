import pandas as pd
import json
from typing import Dict, Any, Optional, List
from textblob import TextBlob
import io
from models.dataset import Dataset, SentimentAnalysis

class DatasetService:
    @staticmethod
    def read_file(file_data: bytes, file_type: str) -> pd.DataFrame:
        try:
            if file_type == 'csv':
                return pd.read_csv(io.BytesIO(file_data))
            elif file_type == 'json':
                return pd.read_json(io.BytesIO(file_data))
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
        except Exception as e:
            raise ValueError(f"Error reading file: {str(e)}")

    @staticmethod
    def detect_text_columns(df: pd.DataFrame) -> list:
        """Detect columns that are likely to contain text for sentiment analysis."""
        text_columns = []
        for column in df.columns:
            # Check if column has string data type and contains text-like content
            if df[column].dtype == 'object':
                sample = df[column].dropna().head(1).iloc[0] if not df[column].empty else None
                if isinstance(sample, str) and len(sample.split()) > 3:
                    text_columns.append(column)
        return text_columns

    @staticmethod
    def analyze_sentiment(text: str) -> Dict[str, float]:
        try:
            blob = TextBlob(str(text))
            return {
                "polarity": blob.sentiment.polarity,
                "subjectivity": blob.sentiment.subjectivity,
            }
        except Exception:
            return {"polarity": 0, "subjectivity": 0}

    @staticmethod
    def categorize_sentiment(polarity: float) -> str:
        if polarity > 0.5: return "very_positive"
        elif polarity > 0: return "positive"
        elif polarity == 0: return "neutral"
        elif polarity > -0.5: return "negative"
        else: return "very_negative"

    @staticmethod
    def get_dataset_preview(df: pd.DataFrame, max_rows: int = 5) -> List[Dict]:
        """Get a preview of the dataset."""
        return df.head(max_rows).to_dict(orient='records')
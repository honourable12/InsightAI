from textblob import TextBlob
from typing import Dict


class SentimentAnalyzer:
	@staticmethod
	def analyze_sentiment(text: str) -> Dict[str, str]:
		"""
        Analyze the sentiment of a given text.

        :param text: Input text to analyze
        :return: Dictionary with sentiment details
        """
		try:
			blob = TextBlob(str(text))
			polarity = blob.sentiment.polarity

			# Categorize sentiment based on polarity
			if polarity > 0.5:
				category = "very_positive"
			elif polarity > 0:
				category = "positive"
			elif polarity == 0:
				category = "neutral"
			elif polarity > -0.5:
				category = "negative"
			else:
				category = "very_negative"

			return {
				"text": text,
				"polarity": polarity,
				"subjectivity": blob.sentiment.subjectivity,
				"sentiment_category": category
			}
		except Exception as e:
			return {
				"text": text,
				"error": str(e),
				"polarity": 0,
				"subjectivity": 0,
				"sentiment_category": "unknown"
			}

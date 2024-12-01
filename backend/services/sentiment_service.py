from textblob import TextBlob
from typing import Dict, Any


class SentimentAnalyzer:
	@staticmethod
	def analyze_sentiment(text: str) -> Dict[str, Any]:
		blob = TextBlob(text)

		# Sentiment polarity (-1 to 1)
		polarity = blob.sentiment.polarity

		# Subjectivity (0 to 1)
		subjectivity = blob.sentiment.subjectivity

		# Sentiment classification
		if polarity > 0.05:
			sentiment = "Positive"
		elif polarity < -0.05:
			sentiment = "Negative"
		else:
			sentiment = "Neutral"

		return {
			"text": text,
			"sentiment": sentiment,
			"polarity": polarity,
			"subjectivity": subjectivity
		}
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

# Import your models
from schemas.input_source import InputSourceType
from models.user import User  # Adjust this import based on your actual user model
from database import Base  # Adjust based on your database setup


class InputSourceService:
	@staticmethod
	def create_input_source(
		db: Session,
		user: User,
		source_type: str,
		path: str,
		api_key: Optional[str] = None,
		description: Optional[str] = None
	):
		"""
		Create a new input source in the database.

		:param db: Database session
		:param user: Current user
		:param source_type: Type of input source (CSV, JSON, or API)
		:param path: File path or API URL
		:param api_key: Optional API key for API sources
		:param description: Optional description of the source
		:return: Created InputSource instance
		"""
		try:
			# Import here to avoid circular imports
			from models.review import InputSource

			# Create new input source
			new_source = InputSource(
				type = InputSourceType(source_type),
				path = path,
				api_key = api_key,
				description = description,
				user_id = user.id,
				created_at = datetime.utcnow()
			)

			# Add to database
			db.add(new_source)
			db.commit()
			db.refresh(new_source)

			return new_source

		except Exception as e:
			db.rollback()
			raise

	@staticmethod
	def get_input_sources_by_user(db: Session, user: User) -> List[Base]:
		"""
		Retrieve all input sources for a specific user.

		:param db: Database session
		:param user: Current user
		:return: List of InputSource instances
		"""
		# Import here to avoid circular imports
		from models.review import InputSource

		return db.query(InputSource).filter(InputSource.user_id == user.id).all()

	@staticmethod
	def update_last_analyzed(db: Session, input_source_id: int):
		"""
		Update the last_analyzed_at timestamp for an input source.

		:param db: Database session
		:param input_source_id: ID of the input source
		"""
		try:
			# Import here to avoid circular imports
			from models.review import InputSource

			source = db.query(InputSource).filter(InputSource.id == input_source_id).first()
			if source:
				source.last_analyzed_at = datetime.utcnow()
				db.commit()
		except Exception as e:
			db.rollback()
			raise
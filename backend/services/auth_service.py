from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from core.security import get_password_hash


def create_user(db: Session, user: UserCreate):
	role = 'user'

	db_user = User(
		username = user.username,
		email = user.email,
		full_name = user.full_name or user.username,
		hashed_password = get_password_hash(user.password),
		is_active = True,
		role = role
	)

	db.add(db_user)
	db.commit()
	db.refresh(db_user)

	return db_user


def authenticate_user(db: Session, username: str, password: str):
	from core.security import verify_password

	user = db.query(User).filter(User.username == username).first()

	if not user or not verify_password(password, user.hashed_password):
		return False

	return user
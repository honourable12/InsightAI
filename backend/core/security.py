from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import bcrypt
from sqlalchemy.orm import Session

from models.user import User
from core.config import settings
from database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def hash_password(password: str) -> str:
	salt = bcrypt.gensalt()
	hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
	return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
	return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))



def create_access_token(data: dict):
	to_encode = data.copy()
	expire = datetime.utcnow() + timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES)
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm = settings.ALGORITHM)
	return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
	credentials_exception = HTTPException(
		status_code = 401,
		detail = "Could not validate credentials",
		headers = {"WWW-Authenticate": "Bearer"},
	)
	try:
		payload = jwt.decode(token, settings.SECRET_KEY, algorithms = [settings.ALGORITHM])
		username: str = payload.get("sub")
		if username is None:
			raise credentials_exception
	except JWTError:
		raise credentials_exception

	user = db.query(User).filter(User.username == username).first()
	if user is None:
		raise credentials_exception
	return user


def get_current_active_user(current_user: User = Depends(get_current_user)):
	if not current_user.is_active:
		raise HTTPException(status_code = 400, detail = "Inactive user")
	return current_user
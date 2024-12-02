# routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session
from datetime import timedelta,datetime
from typing import Annotated

from core.security import create_access_token, get_current_active_user
from core.config import settings
from services.auth_service import create_user, authenticate_user
from schemas.user import User, UserCreate, Token
from database import get_db
from models.user import User as UserModel
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/register", response_model = User)
def register_user(
	user: UserCreate,
	db: Annotated[Session, Depends(get_db)]
):
	# Validate username
	if len(user.username) < 3:
		raise HTTPException(
			status_code = status.HTTP_400_BAD_REQUEST,
			detail = "Username must be at least 3 characters long"
		)

	# Validate password
	if len(user.password) < 8:
		raise HTTPException(
			status_code = status.HTTP_400_BAD_REQUEST,
			detail = "Password must be at least 8 characters long"
		)

	# Check if username already exists
	existing_user = db.query(UserModel).filter(UserModel.username == user.username).first()
	if existing_user:
		raise HTTPException(
			status_code = status.HTTP_400_BAD_REQUEST,
			detail = "Username already registered"
		)

	# Check if email already exists
	existing_email = db.query(UserModel).filter(UserModel.email == user.email).first()
	if existing_email:
		raise HTTPException(
			status_code = status.HTTP_400_BAD_REQUEST,
			detail = "Email already registered"
		)

	# Create and return the new user
	return create_user(db = db, user = user)


@router.post("/token", response_model = dict)
def login(
	form_data: OAuth2PasswordRequestForm = Depends(),
	db: Session = Depends(get_db)
):
	# Fetch user from the database
	user = db.query(User).filter(User.username == form_data.username).first()

	# Verify user and password
	if not user or not verify_password(form_data.password, user.hashed_password):
		raise HTTPException(
			status_code = status.HTTP_401_UNAUTHORIZED,
			detail = "Incorrect username or password",
			headers = {"WWW-Authenticate": "Bearer"},
		)

	# Generate access token
	access_token = create_access_token(
		data = {"sub": user.username, "role": user.role, "user_id": user.id}
	)

	return {
		"access_token": access_token,
		"token_type": "bearer"
	}


@router.get("/users/me", response_model = User)
def read_users_me(
	current_user: Annotated[User, Depends(get_current_active_user)]
):
	return current_user


@router.post("/change-password")
def change_password(
	current_password: str,
	new_password: str,
	current_user: Annotated[User, Depends(get_current_active_user)],
	db: Annotated[Session, Depends(get_db)]
):
	from core.security import verify_password, get_password_hash

	# Verify current password
	if not verify_password(current_password, current_user.hashed_password):
		raise HTTPException(
			status_code = status.HTTP_400_BAD_REQUEST,
			detail = "Incorrect current password"
		)

	# Validate new password
	if len(new_password) < 8:
		raise HTTPException(
			status_code = status.HTTP_400_BAD_REQUEST,
			detail = "New password must be at least 8 characters long"
		)

	# Hash and update the password
	current_user.hashed_password = get_password_hash(new_password)
	db.commit()

	return {"message": "Password successfully changed"}


@router.post("/reset-password")
def reset_password(
	email: str,
	db: Annotated[Session, Depends(get_db)]
):
	# Find user by email
	user = db.query(User).filter(User.email == email).first()

	if not user:
		raise HTTPException(
			status_code = status.HTTP_404_NOT_FOUND,
			detail = "User not found"
		)

	# Generate a temporary password
	import secrets
	temp_password = secrets.token_urlsafe(12)

	# Update user's password
	from core.security import get_password_hash
	user.hashed_password = get_password_hash(temp_password)
	db.commit()

	# In a real-world scenario, you would send this temporary password via email
	# Here, we're just returning it for demonstration
	return {
		"message": "Temporary password generated",
		"temp_password": temp_password
	}

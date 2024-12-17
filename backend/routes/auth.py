# routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, Form, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
import secrets
from core.security import verify_password, hash_password, create_access_token, get_current_user

from database import get_db
from models.user import User

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@router.post("/register")
def register(
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(None),
    full_name: str = Form(None),
    role: str = Form("user"),
    db: Session = Depends(get_db)
):
    # Validate username
    if len(username) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username must be at least 3 characters long"
        )

    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )

    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    if email and db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = hash_password(password)

    new_user = User(
        username=username,
        email=email,
        full_name=full_name,
        hashed_password=hashed_password,
        role=role,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "user_id": new_user.id}


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	user = db.query(User).filter(User.username == form_data.username).first()

	if not user or not verify_password(form_data.password, user.hashed_password):
		raise HTTPException(status_code = 400, detail = "Incorrect username or password")

	access_token = create_access_token(data = {"sub": user.username})

	return {"access_token": access_token, "token_type": "bearer"}


@router.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
	return {
		"username": current_user.username,
		"email": current_user.email,
		#"created_at": current_user.created_at
	}


@router.post("/change-password")
def change_password(
	current_password: str = Form(...),
	new_password: str = Form(...),
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db)
):
	if not verify_password(current_password, current_user.hashed_password):
		raise HTTPException(
			status_code = status.HTTP_400_BAD_REQUEST,
			detail = "Incorrect current password"
		)

	if len(new_password) < 8:
		raise HTTPException(
			status_code = status.HTTP_400_BAD_REQUEST,
			detail = "New password must be at least 8 characters long"
		)

	current_user.hashed_password = hash_password(new_password)
	db.commit()

	return {"message": "Password successfully changed"}


@router.post("/reset-password")
def reset_password(
	email: str = Form(...),
	db: Session = Depends(get_db)
):
	user = db.query(User).filter(User.email == email).first()

	if not user:
		raise HTTPException(
			status_code = status.HTTP_404_NOT_FOUND,
			detail = "User not found"
		)

	temp_password = secrets.token_urlsafe(12)

	user.password = hash_password(temp_password)
	db.commit()

	# In a real-world scenario, you would send this temporary password via email
	# Here, we're just returning it for demonstration
	return {
		"message": "Temporary password generated",
		"temp_password": temp_password
	}


@router.delete("/delete-account")
def delete_account(
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db)
):
	db.delete(current_user)
	db.commit()
	return {"message": "Account deleted successfully"}
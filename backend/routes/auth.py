# routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, Form, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
import secrets
import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta
from core.security import verify_password, hash_password, create_access_token, get_current_user
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

from database import get_db
from models.user import User
from core.config import settings

load_dotenv()
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# def hash_password(password: str) -> str:
# 	salt = bcrypt.gensalt()
# 	hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
# 	return hashed_password.decode('utf-8')


# def verify_password(plain_password: str, hashed_password: str) -> bool:
# 	return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

#
# def create_access_token(data: dict):
# 	to_encode = data.copy()
# 	expire = datetime.utcnow() + timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES)
# 	to_encode.update({"exp": expire})
# 	encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm = settings.ALGORITHM)
# 	return encoded_jwt


# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
# 	credentials_exception = HTTPException(
# 		status_code = 401,
# 		detail = "Could not validate credentials",
# 		headers = {"WWW-Authenticate": "Bearer"},
# 	)
# 	try:
# 		payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms = [settings.ALGORITHM])
# 		username: str = payload.get("sub")
# 		if username is None:
# 			raise credentials_exception
# 	except JWTError:
# 		raise credentials_exception
#
# 	user = db.query(User).filter(User.username == username).first()
# 	if user is None:
# 		raise credentials_exception
# 	return user


@router.post("/register")
def register(
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(None),
    full_name: str = Form(None),
    role: str = Form("user"),  # Default role
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
	# Find user by username
	user = db.query(User).filter(User.username == form_data.username).first()

	# Verify password
	if not user or not verify_password(form_data.password, user.hashed_password):
		raise HTTPException(status_code = 400, detail = "Incorrect username or password")

	# Create access token
	access_token = create_access_token(data = {"sub": user.username})

	return {"access_token": access_token, "token_type": "bearer"}


@router.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
	return {
		"username": current_user.username,
		"email": current_user.email,
		"created_at": current_user.created_at
	}


@router.post("/change-password")
def change_password(
	current_password: str = Form(...),
	new_password: str = Form(...),
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db)
):
	# Verify current password
	if not verify_password(current_password, current_user.password):
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
	current_user.password = hash_password(new_password)
	db.commit()

	return {"message": "Password successfully changed"}


@router.post("/reset-password")
def reset_password(
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    # Find user by email
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Generate a temporary password
    temp_password = secrets.token_urlsafe(12)

    # Hash and update the user's password
    user.password = hash_password(temp_password)
    db.commit()

    # Email configuration 
    sender_email = os.getenv("GMAIL_EMAIL")  
    app_password = os.getenv("GMAIL_APP_PASSWORD")  
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # This sends the message to the user
    subject = "Password Reset Request"
    message = f"Hello {user.username},\n\nYour temporary password is: {temp_password}\nPlease use this password to log in and reset your password immediately."

    # This part creates the email
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    try:
        # Sending the mail using Gmail's SMTP 
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls() 
            server.login(sender_email, app_password)  
            server.sendmail(sender_email, email, msg.as_string()) 
            print("Email sent successfully!")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send email: {e}"
        )

    return {
        "message": "Temporary password generated and sent to your email"
    }

@router.delete("/delete-account")
def delete_account(
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db)
):
	db.delete(current_user)
	db.commit()
	return {"message": "Account deleted successfully"}
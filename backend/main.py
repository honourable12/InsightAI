# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routes.auth import router as auth_router
from routes.review import router as review_router  # Note the change
from database import create_tables

# Create database tables
create_tables()

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(review_router, prefix="/reviews", tags=["reviews"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import requests

# Database setup
DATABASE_URL = "sqlite:///./mcn_server.db"  # Change to PostgreSQL/MySQL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class Channel(Base):
    __tablename__ = "channels"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

# API Setup
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "MCN Server is running!"}

# YouTube API Integration
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_API_KEY = "your_youtube_api_key"  # Replace with actual API key

@app.get("/youtube/search/{keyword}")
def search_youtube(keyword: str):
    params = {
        "part": "snippet",
        "q": keyword,
        "maxResults": 25,
        "key": YOUTUBE_API_KEY
    }
    response = requests.get(YOUTUBE_API_URL, params=params)
    return response.json()

# Initialize DB
Base.metadata.create_all(bind=engine)

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///dev.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "").split(",") if o.strip()] or ["http://localhost:5173"]
    BACKEND_PORT = int(os.getenv("BACKEND_PORT", "5001"))
    JWT_COOKIE_SECURE = os.getenv("JWT_COOKIE_SECURE", "false").lower() == "true"
    AI_KEY = os.getenv("AI_KEY", "")
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

APP_NAME = os.getenv("APP_NAME", "Business Management Tool")
APP_ENV = os.getenv("APP_ENV", "development")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{(DATA_DIR / 'app.db').as_posix()}")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
DEFAULT_CURRENCY = os.getenv("DEFAULT_CURRENCY", "KES")
BUSINESS_TIMEZONE = os.getenv("BUSINESS_TIMEZONE", "Africa/Nairobi")
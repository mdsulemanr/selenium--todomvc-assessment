from pathlib import Path
import os

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

BASE_URL = os.getenv("BASE_URL", "https://demo.playwright.dev").rstrip("/")
HEADLESS = os.getenv("HEADLESS", "true").lower() in {"1", "true", "yes", "on"}
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10"))

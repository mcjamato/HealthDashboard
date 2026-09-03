from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

DATABASE_PATH = BASE_DIR / "database" / "health_dashboard.db"
CSS_PATH = BASE_DIR / "assets" / "css" / "style.css"

APP_NAME = "Health & Wellness Analytics Dashboard"
APP_VERSION = "1.5.1"
APP_ICON = "💙"

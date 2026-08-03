from pathlib import Path

# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

DATABASE_DIR = BASE_DIR / "database"

DATABASE_FILE = DATABASE_DIR / "health_dashboard.db"

ASSET_DIR = BASE_DIR / "assets"

CSS_DIR = ASSET_DIR / "css"

IMAGE_DIR = ASSET_DIR / "images"

# ==========================================================
# APPLICATION
# ==========================================================

APP_NAME = "Health & Wellness Analytics Dashboard"

APP_VERSION = "0.1.0"

APP_ICON = "💙"

APP_LAYOUT = "wide"

# ==========================================================
# COLORS
# ==========================================================

PRIMARY = "#4A90E2"

SECONDARY = "#64B5F6"

BACKGROUND = "#EAF4FF"

CARD = "#FFFFFF"

TEXT = "#1F2937"

# ==========================================================
# SECURITY
# ==========================================================

SESSION_TIMEOUT = 60
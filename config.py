# config.py (อัปเดต)
import os

APP_NAME = "Investigation Documents System"
APP_VERSION = "1.0.0"
CURRENT_USER = "พ.ต.ท. วรนันท์"

FONT_FAMILY = "Sarabun, TH Sarabun PSK, Segoe UI, sans-serif"
FONT_SIZE_BASE = 14

PRIMARY_NAV_BG = "#1A2B4C"
SIDEBAR_BG = "#EAEFF5"
MAIN_CONTENT_BG = "#F0F3F8"
CARD_BG = "#FFFFFF"

CARD_TOTAL_BLUE = "#70A6E8"
CARD_SUCCESS_GREEN = "#82C79B"
CARD_WARNING_YELLOW = "#F2D36B"

CARD_DUI_BLUE = "#82B2EA"
CARD_DRUG_GREEN = "#A1D9B2"
CARD_GAMBLE_RED = "#E8A2A2"
CARD_VEHICLE_ORANGE = "#E8C58C"

DANGER_LOGOUT_RED = "#D9534F"

# --- [เพิ่มเติมสำหรับ SQLAlchemy] ---
DB_NAME = "investigation_system.db"
DATABASE_URL = f"sqlite:///{DB_NAME}"

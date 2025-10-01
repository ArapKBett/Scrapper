"""Configuration settings"""
import os

# Base configuration
BASE_URL = "https://mlb.tickets.com"
EVENT_ID = "9573829"
AGENCY = "MILB_MPV"
ORG_ID = "56877"
PID = "9573829"

# API Endpoints
AVAILABILITY_ENDPOINT = f"/availability/"
SEATMAP_ENDPOINT = f"/seatmap/"

# Full event URL
EVENT_URL = f"{BASE_URL}/?agency={AGENCY}&orgid={ORG_ID}&pid={PID}#/event/{EVENT_ID}/seatmap/?minPrice=63.54&maxPrice=63.54&quantity=2&sort=price_desc&ada=false&seatSelection=true&onlyCoupon=true&onlyVoucher=false"

# Output directories
OUTPUT_DIR = "output"
SCREENSHOT_DIR = os.path.join(OUTPUT_DIR, "screenshots")
LOG_DIR = "logs"

# Browser settings
HEADLESS = False  # Set to True for production
TIMEOUT = 60000  # 60 seconds
WAIT_TIME = 5  # Wait time after page load

# Stealth settings
USER_AGENTS = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
]

VIEWPORTS = [
    {'width': 1920, 'height': 1080},
    {'width': 1366, 'height': 768},
    {'width': 1536, 'height': 864},
]

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

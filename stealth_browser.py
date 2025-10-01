"""Stealth browser implementation with anti-detection"""
import random
import time
import json
from playwright.sync_api import sync_playwright
from config import USER_AGENTS, VIEWPORTS, TIMEOUT
import logging

logger = logging.getLogger(__name__)


class StealthBrowser:
    """Production-ready stealth browser for Akamai bypass"""
    
    def __init__(self, headless=False):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.user_agent = random.choice(USER_AGENTS)
        self.viewport = random.choice(VIEWPORTS)
    
    def start(self):
        """Initialize stealth browser"""
        logger.info("Starting stealth browser...")
        
        self.playwright = sync_playwright().start()
        
        # Launch args to avoid detection
        launch_args = [
            '--disable-blink-features=AutomationControlled',
            '--disable-dev-shm-usage',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-web-security',
            '--disable-features=IsolateOrigins,site-per-process',
            '--window-size=1920,1080',
        ]
        
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=launch_args,
        )
        
        # Create context with stealth settings
        self.context = self.browser.new_context(
            user_agent=self.user_agent,
            viewport=self.viewport,
            locale='en-US',
            timezone_id='America/New_

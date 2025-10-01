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
extra_http_headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
        )
        
        # Inject anti-detection scripts
        self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            
            window.chrome = { runtime: {} };
            
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
        """)
        
        self.page = self.context.new_page()
        logger.info(f"Browser started - UA: {self.user_agent[:50]}...")
        
    def navigate(self, url, wait_for='networkidle'):
        """Navigate to URL with stealth timing"""
        logger.info(f"Navigating to: {url}")
        
        time.sleep(random.uniform(1, 2))
        
        try:
            self.page.goto(url, wait_until=wait_for, timeout=TIMEOUT)
            time.sleep(random.uniform(2, 4))
            logger.info("Page loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Navigation failed: {e}")
            return False
    
    def screenshot(self, filename):
        """Take screenshot"""
        self.page.screenshot(path=filename, full_page=True)
        logger.info(f"Screenshot saved: {filename}")
    
    def close(self):
        """Clean shutdown"""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        logger.info("Browser closed")

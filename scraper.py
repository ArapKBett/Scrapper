"""Main scraper logic"""
import json
import time
import os
from stealth_browser import StealthBrowser
from parser import DataParser
from config import *
import logging

logger = logging.getLogger(__name__)


class TicketScraper:
    """Scrape ticket availability from Tickets.com"""
    
    def __init__(self, headless=False):
        self.browser = StealthBrowser(headless=headless)
        self.parser = DataParser()
        self.api_data = []
        
    def start(self):
        """Initialize scraper"""
        self.browser.start()
        
        # Setup API interception
        self.browser.page.on('response', self._handle_response)
    
    def _handle_response(self, response):
        """Handle all API responses"""
        url = response.url
        
        # Capture availability endpoints
        if '/availability' in url.lower():
            try:
                data = response.json()
                self.api_data.append({
                    'type': 'availability',
                    'url': url,
                    'data': data
                })
                logger.info(f"✓ Captured availability: {url}")
            except:
                pass
        
        # Capture seatmap endpoints
        if '/seatmap' in url.lower():
            try:
                # Try JSON first
                data = response.json()
                self.api_data.append({
                    'type': 'seatmap_json',
                    'url': url,
                    'data': data
                })
                logger.info(f"✓ Captured seatmap JSON: {url}")
            except:
                # Try XML
                try:
                    text = response.text()
                    if text.strip().startswith('<'):
                        self.api_data.append({
                            'type': 'seatmap_xml',
                            'url': url,
                            'data': text
                        })
                        logger.info(f"✓ Captured seatmap XML: {url}")
                except:
                    pass
    
    def scrape_event(self, event_url):
        """Scrape event availability"""
        logger.info("="*60)
        logger.info("STARTING SCRAPE")
        logger.info("="*60)
        
        # Navigate to event page
        if not self.browser.navigate(event_url):
            logger.error("Failed to load event page")
            return None
        
        # Take initial screenshot
        screenshot_path = os.path.join(SCREENSHOT_DIR, 'event_loaded.png')
        self.browser.screenshot(screenshot_path)
        
        # Wait for API calls to complete
        logger.info("Waiting for API calls...")
        time.sleep(WAIT_TIME)
        
        # Additional interactions to trigger more API calls
        self._interact_with_page()
        
        # Process captured data
        results = self._process_api_data()
        
        return results
    
    def _interact_with_page(self):
        """Interact with page to trigger API calls"""
        try:
            # Scroll to load more content
            self.browser.page.mouse.wheel(0, 500)
            time.sleep(2)
            
            # Click on different price filters if available
            filters = self.browser.page.query_selector_all('[class*="filter"], [class*="price"]')
            if filters:
                logger.info(f"Found {len(filters)} interactive elements")
                for i, filter_elem in enumerate(filters[:3]):
                    try:
                        filter_elem.click()
                        time.sleep(1)
                    except:
                        pass
        except Exception as e:
            logger.warning(f"Interaction error: {e}")
    
    def _process_api_data(self):
        """Process all captured API data"""
        logger.info("="*60)
        logger.info(f"PROCESSING {len(self.api_data)} API CALLS")
        logger.info("="*60)
        
        results = {
            'availability': [],
            'seatmaps': [],
            'seats': [],
            'summary': {}
        }
        
        # Process each captured API call
        for item in self.api_data:
            if item['type'] == 'availability':
                parsed = self.parser.parse_availability_json(item['data'])
                results['availability'].append(parsed)
                logger.info(f"✓ Processed availability data")
                
            elif item['type'] == 'seatmap_xml':
                seats = self.parser.parse_seatmap_xml(item['data'])
                results['seats'].extend(seats)
                logger.info(f"✓ Parsed {len(seats)} seats from XML")
                
            elif item['type'] == 'seatmap_json':
                seats = self.parser.parse_seatmap_json(item['data'])
                results['seats'].extend(seats)
                logger.info(f"✓ Parsed {len(seats)} seats from JSON")
        
        # Generate summary
        if results['seats']:
            results['summary'] = self.parser.summarize_availability(results['seats'])
        
        return results
    
    def save_results(self, results, filename='results.json'):
        """Save results to file"""
        output_path = os.path.join(OUTPUT_DIR, filename)
        
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"✓ Results saved: {output_path}")
        
        # Also save summary separately
        if results.get('summary'):
            summary_path = os.path.join(OUTPUT_DIR, 'summary.json')
            with open(summary_path, 'w') as f:
                json.dump(results['summary'], f, indent=2)
            logger.info(f"✓ Summary saved: {summary_path}")
    
    def close(self):
        """Cleanup"""
        self.browser.close()

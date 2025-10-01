#!/usr/bin/env python3
"""
Tickets.com Availability Scraper
Main execution script
"""
import os
import sys
import logging
from datetime import datetime
from scraper import TicketScraper
from config import *


def setup_logging():
    """Setup logging configuration"""
    os.makedirs(LOG_DIR, exist_ok=True)
    
    log_file = os.path.join(LOG_DIR, f'scraper_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)


def create_directories():
    """Create necessary directories"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)


def print_banner():
    """Print application banner"""
    banner = """
    ╔══════════════════════════════════════════════╗
    ║   TICKETS.COM AVAILABILITY SCRAPER v1.0      ║
    ║   Stealth Mode: ✓ Active                     ║
    ╚══════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Main execution"""
    # Setup
    create_directories()
    logger = setup_logging()
    print_banner()
    
    logger.info("Initializing scraper...")
    logger.info(f"Target Event: {EVENT_ID}")
    logger.info(f"Headless Mode: {HEADLESS}")
    
    scraper = None
    
    try:
        # Initialize scraper
        scraper = TicketScraper(headless=HEADLESS)
        scraper.start()
        
        # Scrape event
        logger.info("\nStarting scrape...")
        results = scraper.scrape_event(EVENT_URL)
        
        if results:
            # Save results
            scraper.save_results(results)
            
            # Print summary
            print("\n" + "="*60)
            print("SCRAPE COMPLETE")
            print("="*60)
            
            if results.get('summary'):
                summary = results['summary']
                print(f"\n📊 AVAILABILITY SUMMARY:")
                print(f"   Total Seats Found: {summary.get('total_seats', 0)}")
                print(f"   Available: {summary.get('available_seats', 0)}")
                print(f"   Unavailable: {summary.get('unavailable_seats', 0)}")
                
                if summary.get('price_ranges'):
                    print(f"\n💰 PRICE RANGES:")
                    for price_range in summary['price_ranges']:
                        print(f"   ${price_range['price']}: {price_range['count']} seats")
                
                if summary.get('sections'):
                    print(f"\n🎫 SECTIONS:")
                    for section, count in summary['sections'].items():
                        print(f"   {section}: {count} seats")
            
            print(f"\n✓ Full results saved to: {OUTPUT_DIR}/")
            print("="*60)
        else:
            logger.error("No results obtained")
            return 1
        
        # Keep browser open for inspection
        if not HEADLESS:
            input("\n👉 Press Enter to close browser...")
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("\nScrape interrupted by user")
        return 130
        
    except Exception as e:
        logger.error(f"Scrape failed: {e}", exc_info=True)
        return 1
        
    finally:
        if scraper:
            scraper.close()
            logger.info("Cleanup complete")


if __name__ == "__main__":
    sys.exit(main())
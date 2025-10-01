# Tickets.com Availability Scraper

Production-ready ticket availability scraper with Akamai bypass.

## Features

- ✅ Stealth browser with anti-detection
- ✅ Intercepts /availability/ and /seatmap/ API calls
- ✅ Parses XML and JSON seatmap data
- ✅ Extracts price and availability info
- ✅ Generates detailed availability reports

## Installation (Kali Linux)

```bash
# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

## Usage

```bash
# Activate virtual environment
source venv/bin/activate

# Run scraper (with visible browser)
python3 main.py

# Run scraper (headless mode)
# Edit config.py and set HEADLESS = True
python3 main.py
```

## Configuration

Edit `config.py` to modify:
- Event URL and IDs
- Browser settings (headless mode)
- Timeout values
- Output directories

## Output

Results are saved in the `output/` directory:
- `results.json` - Complete raw data
- `summary.json` - Availability summary
- `screenshots/` - Page screenshots

## Project Structure

```
ticket-scraper/
├── main.py              # Main entry point
├── scraper.py           # Core scraper logic
├── stealth_browser.py   # Browser automation
├── parser.py            # Data parsing
├── config.py            # Configuration
├── requirements.txt     # Dependencies
├── setup.sh             # Setup script
├── output/              # Results
└── logs/                # Log files
```

## Troubleshooting

If browser fails to launch:
```bash
# Reinstall Playwright
playwright install chromium
playwright install-deps chromium
```

If permissions error:
```bash
chmod +x setup.sh main.py
```

## Legal Notice

This tool is for authorized testing of your own systems only.
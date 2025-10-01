#!/bin/bash
# Setup script for Kali Linux

echo "========================================"
echo "Tickets.com Scraper Setup"
echo "========================================"

# Update system
echo "[1/5] Updating system..."
sudo apt-get update -qq

# Install Python dependencies
echo "[2/5] Installing Python dependencies..."
sudo apt-get install -y python3 python3-pip python3-venv

# Create virtual environment
echo "[3/5] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python packages
echo "[4/5] Installing Python packages..."
pip install -r requirements.txt

# Install Playwright browsers
echo "[5/5] Installing Playwright browsers..."
playwright install chromium
playwright install-deps chromium

echo ""
echo "✓ Setup complete!"
echo ""
echo "To run the scraper:"
echo "  source venv/bin/activate"
echo "  python3 main.py"
echo ""

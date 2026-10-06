# Release Notes - v1.6.0

## Release Package

**File**: `FairGame_Stock_Defender_v1.6.0_Windows.zip`
**Size**: ~72MB (compressed)
**Contents**:
- `FairGame_Stock_Defender.exe` - Main application (73MB)
- `install_browsers.bat` - Browser installation script
- `USER_INSTALL_GUIDE.md` - User installation guide
- `README.md` - Full documentation

## Installation Instructions for Users

### Step 1: Download
Download the ZIP file from GitHub Releases

### Step 2: Extract
Extract all files to a folder of your choice

### Step 3: Install Browsers (Required)
Double-click `install_browsers.bat` to install the Playwright Chromium browser
- This downloads ~300MB of data
- Required for the application to work
- Only needs to be done once

### Step 4: Run
Double-click `FairGame_Stock_Defender.exe` to launch the application

## Features

### Core Functionality
- ✅ Real-time stock monitoring
- ✅ Multi-product tracking
- ✅ Instant alerts (sound + desktop notifications)
- ✅ Multi-store support (Amazon, Best Buy, Target, Walmart)
- ✅ Configurable check intervals
- ✅ Zero false positives

### User Interface
- ✅ Modern dark theme with green accents
- ✅ Three-column responsive layout
- ✅ Live tracker grid with color-coded status
- ✅ Alert history logging
- ✅ Product watchlist management
- ✅ Alert settings toggles

### Safety & Privacy
- ✅ User-agent rotation
- ✅ Anti-detection measures
- ✅ Fully local operation
- ✅ No registration required
- ✅ No data collection

### Auto-Updates
- ✅ GitHub Releases integration
- ✅ Automatic version checking
- ✅ Background update downloads
- ✅ Safe file replacement

## System Requirements

- **OS**: Windows 10 or 11
- **Disk Space**: ~350MB (300MB for browser + 73MB for app)
- **Internet**: Required for stock checking and updates
- **Python**: Not required (standalone executable)

## Known Issues

- Browser installation requires internet connection
- First launch may be slower as browser initializes
- Some niche stores may require custom selectors

## Future Updates

Planned features for future versions:
- [ ] Price tracking
- [ ] Email/SMS alerts
- [ ] Historical stock data
- [ ] Custom notification sounds
- [ ] Multi-language support
- [ ] Mobile companion app

## Support

- **GitHub**: https://github.com/marleypumpkin08-ctrl/FairGame-Stock-Defender
- **Issues**: Report bugs via GitHub Issues
- **Documentation**: See README.md and USER_INSTALL_GUIDE.md

## License

MIT License - See LICENSE file for details

## Credits

Built with:
- Python 3.14
- CustomTkinter
- Playwright
- BeautifulSoup4
- PyInstaller

Generated with [Devin](https://devin.ai)

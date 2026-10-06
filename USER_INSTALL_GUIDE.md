# FairGame Stock Defender - Installation Guide

## Quick Installation (Windows)

### Step 1: Install Browsers (Required)

The application requires the Playwright Chromium browser to monitor websites.

**Option A: Automatic Setup (Recommended)**
1. Double-click `install_browsers.bat`
2. Wait for the download to complete (~300MB)
3. Once complete, you can run the application

**Option B: Manual Setup**
1. Open Command Prompt
2. Run: `python -m playwright install chromium`

### Step 2: Run the Application

Once browsers are installed:
1. Double-click `FairGame_Stock_Defender.exe`
2. The application will launch automatically

## Requirements

- Windows 10 or 11
- No Python installation required (for the .exe version)
- Internet connection (for checking stock and updates)
- ~350MB free disk space (300MB for browser + 73MB for application)

## Troubleshooting

### "Browser not found" Error

If you see this error when running the application:
1. Run `install_browsers.bat` again
2. Or manually run: `python -m playwright install chromium`

### Application Won't Start

1. Make sure you've installed the browsers first
2. Check that you have Windows 10 or 11
3. Try running as Administrator

### Browser Installation Fails

1. Make sure you have an internet connection
2. Temporarily disable your antivirus/firewall
3. Try running the command manually in Command Prompt:
   ```
   python -m playwright install chromium
   ```

## Features

- ✅ Monitor multiple products simultaneously
- ✅ Real-time stock checking
- ✅ Instant alerts (sound + notifications)
- ✅ Multi-store support (Amazon, Best Buy, Target, Walmart)
- ✅ Automatic updates
- ✅ No registration required
- ✅ Fully local and private

## First Run

1. Launch `FairGame_Stock_Defender.exe`
2. Click "+ Add Product" in the left sidebar
3. Enter product name, store, and URL
4. Click "Add Product"
5. The app will start monitoring automatically

## Support

For issues or questions:
- GitHub: https://github.com/marleypumpkin08-ctrl/FairGame-Stock-Defender
- Email: (add your email)

## License

MIT License - See LICENSE file for details.

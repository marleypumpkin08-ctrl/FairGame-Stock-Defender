# FairGame Stock Defender

A lightweight, cross-platform desktop application for monitoring product web pages for stock availability. Built with Python and CustomTkinter to help legitimate retail users bypass scalper bot advantages.

## Features

- **Real-time Stock Monitoring**: Automatically checks product pages at user-defined intervals
- **Intelligent Parsing Engine**: Uses Playwright with BeautifulSoup to detect stock status with zero false positives
- **Multi-Store Support**: Pre-configured selectors for Amazon, Best Buy, Target, Walmart, and more
- **Instant Alerts**: System sound alerts and desktop notifications when stock is detected
- **Clean Modern UI**: Dark theme with green accents, responsive design
- **Auto-Updater**: Automatically checks for and installs updates from GitHub releases
- **Privacy-Focused**: Fully local operation with no tracking or registration required
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Screenshots

The application features a three-column layout:
- **Left Sidebar**: Product watchlist management and alert settings
- **Main Content**: Live tracker grid showing product status
- **Right Sidebar**: Version info, alert history logs, and donation button

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Platform-Specific Requirements

**Windows:**
- No additional requirements

**macOS:**
- Xcode Command Line Tools (for pyobjc)
- Install with: `xcode-select --install`

**Linux:**
- libnotify-bin for desktop notifications
- Install with: `sudo apt-get install libnotify-bin` (Debian/Ubuntu)

### Setup

1. Clone or download this repository:
```bash
git clone https://github.com/yourusername/FairGame-Stock-Defender.git
cd FairGame-Stock-Defender
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
playwright install chromium
```

4. Run the application:
```bash
python main.py
```

## Configuration

Edit `config.json` to customize the application:

```json
{
  "app_name": "FairGame Stock Defender",
  "version": "1.6.0",
  "github_repo": "yourusername/FairGame-Stock-Defender",
  "check_interval": 10,
  "alert_sound_enabled": true,
  "desktop_notifications_enabled": true,
  "donation_url": "https://ko-fi.com/yourusername",
  "user_agents": [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36..."
  ]
}
```

### Configuration Options

- `check_interval`: Seconds between stock checks (default: 10)
- `alert_sound_enabled`: Enable/disable system sound alerts
- `desktop_notifications_enabled`: Enable/disable OS notifications
- `donation_url`: URL for the support development button
- `user_agents`: List of user agent strings for rotation

## Usage

### Adding Products

1. Click the "+ Add Product" button in the left sidebar
2. Enter the product name, store, and product URL
3. Click "Add Product" to start monitoring

### Monitoring

- The application automatically checks stock status at the configured interval
- Status indicators:
  - **Green**: IN STOCK!
  - **Red**: Out of Stock
  - **Brown**: Error or Timeout
- "Last Check" column shows when the product was last verified

### Alerts

When stock is detected:
- System sound alert plays (if enabled)
- Desktop notification appears (if enabled)
- Alert is logged in the Alert History
- Product status in the grid turns green

### Auto-Updates

On startup, the application checks GitHub for updates:
- If an update is available, a dialog prompts you to download and install
- The update downloads in the background
- After installation, you'll be prompted to restart

## Building Executable

To create a standalone executable:

### Windows

```bash
pyinstaller --onefile --windowed --name "FairGame_Stock_Defender" --icon=assets/icon.ico main.py
```

### macOS

```bash
pyinstaller --onefile --windowed --name "FairGame_Stock_Defender" --icon=assets/icon.icns main.py
```

### Linux

```bash
pyinstaller --onefile --name "FairGame_Stock_Defender" main.py
```

The executable will be in the `dist/` directory.

## Project Structure

```
FairGame-Stock-Defender/
├── main.py              # Application entry point
├── config.json          # Configuration file
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── src/
│   ├── __init__.py
│   ├── updater.py      # Auto-updater module
│   ├── scraper.py      # Stock monitoring engine
│   └── ui.py           # User interface
├── assets/             # Icons and resources
└── data/               # Runtime data (watchlist, logs)
```

## Architecture

### Updater Module (`src/updater.py`)
- Checks GitHub Releases API for version updates
- Downloads platform-specific binaries
- Handles safe file replacement and restart

### Scraper Module (`src/scraper.py`)
- Uses Playwright for headless browser automation
- Implements anti-detection measures (user-agent rotation, stealth scripts)
- Store-specific parsing logic for major retailers
- Custom selector support for niche stores

### UI Module (`src/ui.py`)
- CustomTkinter-based modern dark theme UI
- Three-column responsive layout
- Real-time status updates
- Alert history logging
- Donation link integration

## Safety & Anti-Detection

The application includes several safety features:

- **User-Agent Rotation**: Randomly selects from configured user agents
- **Stealth Scripts**: Injects JavaScript to avoid bot detection
- **Request Headers**: Sets realistic browser headers
- **Graceful Error Handling**: Recovers from timeouts and network errors
- **Rate Limiting**: Respects configured check intervals

## Troubleshooting

### Playwright Browser Not Found

```bash
playwright install chromium
```

### Port Already in Use

Change the check interval in `config.json` or close other browser instances.

### Notifications Not Appearing (Windows)

Ensure Windows notifications are enabled in Settings > System > Notifications.

### macOS Notifications

Install `pyobjc` framework for notification support:
```bash
pip install pyobjc-framework-Cocoa
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

If you find this tool helpful, consider supporting its development via the Ko-fi button in the application.

## Disclaimer

This tool is for educational and personal use only. Always respect retailer terms of service and rate limits. The authors are not responsible for any misuse of this software.

## Changelog

### v1.6.0
- Initial release
- Core stock monitoring functionality
- Auto-updater system
- Modern CustomTkinter UI
- Multi-store support
- Desktop notifications

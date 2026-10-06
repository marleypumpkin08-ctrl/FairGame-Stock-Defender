# Quick Start Guide

## First-Time Setup

1. **Install Dependencies**
   ```bash
   python setup.py
   ```

2. **Configure the Application**
   - Edit `config.json` to set your GitHub repository and donation URL
   - Adjust `check_interval` to change how often products are checked (default: 10 seconds)

3. **Run the Application**
   ```bash
   python main.py
   ```

## Adding Your First Product

1. Click the **"+ Add Product"** button in the left sidebar
2. Fill in the fields:
   - **Product Name**: e.g., "NVIDIA RTX 5080 FE"
   - **Store**: e.g., "Best Buy"
   - **Product URL**: Paste the full product page URL
3. Click **"Add Product"**

The product will now appear in your watchlist and begin monitoring immediately.

## Understanding the Status Grid

- **Green "IN STOCK!"**: Product is available for purchase
- **Red "Out of Stock"**: Product is not available
- **Brown "Error/Timeout"**: Check failed (will retry automatically)
- **"Checking..."**: Currently verifying stock status

## Configuring Alerts

Toggle alerts in the left sidebar:
- **System Sound Alerts**: Plays beep sounds when stock is detected
- **Desktop Notifications**: Shows OS notification banners

## Tips for Best Results

1. **Check Interval**: Set to 5-10 seconds for high-demand items, 30-60 seconds for less critical items
2. **Multiple Stores**: Add the same product from different stores to increase chances
3. **Custom Selectors**: For niche stores, you can add custom CSS selectors in the code (see scraper.py)
4. **Keep App Running**: The app must be open to monitor products

## Troubleshooting

**"Playwright browser not found" error:**
```bash
playwright install chromium
```

**Application won't start:**
- Ensure Python 3.8+ is installed
- Run `python setup.py` to reinstall dependencies

**No notifications appearing:**
- Check system notification settings
- Ensure notification toggles are ON in the app

## Building an Executable

To create a standalone executable:

```bash
python build.py
```

The executable will be in the `dist/` directory and can be run without Python installed.

## Support

For issues or questions:
- Check the README.md for detailed documentation
- Review the code comments in src/ files
- Open an issue on GitHub

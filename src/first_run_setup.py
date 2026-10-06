"""
First-run setup for FairGame Stock Defender.
Installs Playwright browsers on first launch.
"""

import subprocess
import sys
import os


def install_playwright_browsers():
    """Install Playwright Chromium browser."""
    print("Installing Playwright Chromium browser...")
    print("This will download approximately 300MB of data.")
    print("Please wait...")

    try:
        # Install chromium using playwright
        result = subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            capture_output=True,
            text=True,
            timeout=600
        )

        if result.returncode == 0:
            print("✓ Playwright Chromium installed successfully!")
            return True
        else:
            print(f"✗ Installation failed: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("✗ Installation timed out. Please try again.")
        return False
    except Exception as e:
        print(f"✗ Error installing Playwright: {e}")
        return False


def check_browsers_installed():
    """Check if Playwright browsers are already installed."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            # Try to launch chromium - if it fails, browsers aren't installed
            browser = p.chromium.launch(headless=True)
            browser.close()
            return True
    except:
        return False


def main():
    """Main setup function."""
    print("=" * 60)
    print("FairGame Stock Defender - First Run Setup")
    print("=" * 60)

    # Check if browsers are already installed
    if check_browsers_installed():
        print("✓ Playwright browsers already installed.")
        print("Setup complete!")
        return

    # Install browsers
    print("\nPlaywright browsers not found.")
    print("Installing now...\n")

    if install_playwright_browsers():
        print("\n" + "=" * 60)
        print("Setup complete! You can now run the application.")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("Setup failed. Please try running this setup again.")
        print("Or manually run: python -m playwright install chromium")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()

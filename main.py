"""
FairGame Stock Defender - Main Application Entry Point
A lightweight desktop application for monitoring product stock availability.
"""

import asyncio
import json
import os
import sys
import threading
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.updater import Updater
from src.scraper import StockScraper
from src.ui import StockDefenderUI


def load_config():
    """
    Load configuration from config.json.

    Returns:
        Configuration dictionary
    """
    config_path = os.path.join(os.path.dirname(__file__), "config.json")

    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: config.json not found. Using default configuration.")
        return {
            "app_name": "FairGame Stock Defender",
            "version": "1.6.0",
            "github_repo": "yourusername/FairGame-Stock-Defender",
            "check_interval": 10,
            "alert_sound_enabled": True,
            "desktop_notifications_enabled": True,
            "donation_url": "https://ko-fi.com/yourusername",
            "user_agents": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ]
        }
    except json.JSONDecodeError as e:
        print(f"Error parsing config.json: {e}. Using default configuration.")
        return {
            "app_name": "FairGame Stock Defender",
            "version": "1.6.0",
            "check_interval": 10,
            "alert_sound_enabled": True,
            "desktop_notifications_enabled": True
        }


async def initialize_scraper(config):
    """
    Initialize the stock scraper.

    Args:
        config: Configuration dictionary

    Returns:
        Initialized StockScraper instance
    """
    scraper = StockScraper(config)
    await scraper.initialize()
    return scraper


def check_for_updates(config, ui_instance):
    """
    Check for application updates on startup.

    Args:
        config: Configuration dictionary
        ui_instance: UI instance to update version status
    """
    updater = Updater(config)

    def update_check():
        update_available, latest_version, download_url = updater.check_for_updates()

        if update_available:
            # Show update dialog
            from tkinter import messagebox
            response = messagebox.askyesno(
                "Update Available",
                f"A new version (v{latest_version}) is available!\n\n"
                f"Current version: v{config['version']}\n"
                f"Latest version: v{latest_version}\n\n"
                f"Would you like to download and install the update?"
            )

            if response:
                # Download and install update
                success, update_path = updater.download_update(download_url)
                if success:
                    updater.install_update(update_path)
                    sys.exit(0)
        else:
            # Update UI to show up to date
            if ui_instance:
                ui_instance.set_version_status(True, latest_version)

    # Run update check in background thread
    thread = threading.Thread(target=update_check, daemon=True)
    thread.start()


def main():
    """Main application entry point."""
    print("Starting FairGame Stock Defender...")

    # Load configuration
    config = load_config()
    print(f"Loaded configuration for {config['app_name']} v{config['version']}")

    # Initialize scraper
    print("Initializing stock scraper...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    scraper = loop.run_until_complete(initialize_scraper(config))
    print("Stock scraper initialized successfully")

    # Create and run UI
    print("Launching UI...")
    ui = StockDefenderUI(scraper, config)

    # Check for updates
    print("Checking for updates...")
    check_for_updates(config, ui)

    # Add initial log entry
    ui._add_alert_log("Application started")

    # Run the UI
    try:
        ui.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        # Cleanup
        print("Cleaning up resources...")
        loop.run_until_complete(scraper.close())
        loop.close()
        print("FairGame Stock Defender closed.")


if __name__ == "__main__":
    main()

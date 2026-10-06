"""
Auto-updater module for FairGame Stock Defender.
Checks GitHub releases for updates and handles automatic updates.
"""

import requests
import json
import os
import sys
import subprocess
import threading
from typing import Optional, Tuple


class Updater:
    """Handles application updates from GitHub releases."""

    def __init__(self, config: dict):
        """
        Initialize the updater.

        Args:
            config: Configuration dictionary containing app info
        """
        self.config = config
        self.current_version = config.get("version", "1.0.0")
        self.github_repo = config.get("github_repo", "")
        self.api_url = f"https://api.github.com/repos/{self.github_repo}/releases/latest"

    def check_for_updates(self) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Check if a newer version is available on GitHub.

        Returns:
            Tuple of (update_available, latest_version, download_url)
        """
        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()

            release_data = response.json()
            latest_version = release_data.get("tag_name", "").lstrip("v")

            # Compare versions
            if self._compare_versions(latest_version, self.current_version) > 0:
                # Find appropriate asset for current platform
                download_url = self._find_platform_asset(release_data.get("assets", []))
                return True, latest_version, download_url

            return False, latest_version, None

        except requests.RequestException as e:
            print(f"Error checking for updates: {e}")
            return False, None, None
        except Exception as e:
            print(f"Unexpected error checking for updates: {e}")
            return False, None, None

    def _compare_versions(self, version1: str, version2: str) -> int:
        """
        Compare two version strings.

        Args:
            version1: First version string
            version2: Second version string

        Returns:
            1 if version1 > version2, -1 if version1 < version2, 0 if equal
        """
        v1_parts = [int(x) for x in version1.split(".")]
        v2_parts = [int(x) for x in version2.split(".")]

        for v1, v2 in zip(v1_parts, v2_parts):
            if v1 > v2:
                return 1
            elif v1 < v2:
                return -1

        return 0

    def _find_platform_asset(self, assets: list) -> Optional[str]:
        """
        Find the appropriate download asset for the current platform.

        Args:
            assets: List of asset objects from GitHub release

        Returns:
            Download URL for the appropriate asset, or None
        """
        if sys.platform == "win32":
            for asset in assets:
                name = asset.get("name", "").lower()
                if "win" in name or "exe" in name:
                    return asset.get("browser_download_url")
        elif sys.platform == "darwin":
            for asset in assets:
                name = asset.get("name", "").lower()
                if "mac" in name or "dmg" in name:
                    return asset.get("browser_download_url")
        elif sys.platform.startswith("linux"):
            for asset in assets:
                name = asset.get("name", "").lower()
                if "linux" in name or "appimage" in name:
                    return asset.get("browser_download_url")

        # Fallback: return first asset
        if assets:
            return assets[0].get("browser_download_url")

        return None

    def download_update(self, download_url: str, progress_callback=None) -> bool:
        """
        Download the update in the background.

        Args:
            download_url: URL to download the update from
            progress_callback: Optional callback for download progress

        Returns:
            True if download successful, False otherwise
        """
        try:
            response = requests.get(download_url, stream=True, timeout=30)
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))
            downloaded = 0

            # Determine destination path
            if sys.platform == "win32":
                temp_path = os.path.join(os.environ["TEMP"], "FairGame_Stock_Defender_Update.exe")
            elif sys.platform == "darwin":
                temp_path = os.path.join(os.environ["TMPDIR"], "FairGame_Stock_Defender_Update.dmg")
            else:
                temp_path = os.path.join("/tmp", "FairGame_Stock_Defender_Update.AppImage")

            with open(temp_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if progress_callback and total_size > 0:
                            progress = (downloaded / total_size) * 100
                            progress_callback(progress)

            return True, temp_path

        except Exception as e:
            print(f"Error downloading update: {e}")
            return False, None

    def install_update(self, update_path: str) -> bool:
        """
        Install the downloaded update.

        Args:
            update_path: Path to the downloaded update file

        Returns:
            True if installation initiated successfully, False otherwise
        """
        try:
            if sys.platform == "win32":
                # Create a batch script to replace the executable and restart
                script_path = os.path.join(os.environ["TEMP"], "update_script.bat")
                current_exe = sys.executable
                script_content = f"""
@echo off
timeout /t 2 /nobreak >nul
copy /Y "{update_path}" "{current_exe}"
start "" "{current_exe}"
del "{script_path}"
del "{update_path}"
"""
                with open(script_path, "w") as f:
                    f.write(script_content)

                # Execute the batch script in a new process
                subprocess.Popen(script_path, shell=True)
                return True

            elif sys.platform == "darwin":
                # For macOS, open the DMG and guide user
                subprocess.Popen(["open", update_path])
                return True

            elif sys.platform.startswith("linux"):
                # For Linux, make AppImage executable and run it
                os.chmod(update_path, 0o755)
                subprocess.Popen([update_path])
                return True

            return False

        except Exception as e:
            print(f"Error installing update: {e}")
            return False

    def background_update_check(self, update_callback=None):
        """
        Check for updates in the background thread.

        Args:
            update_callback: Callback function to notify of update availability
        """
        def check():
            update_available, latest_version, download_url = self.check_for_updates()
            if update_available and update_callback:
                update_callback(latest_version, download_url)

        thread = threading.Thread(target=check, daemon=True)
        thread.start()

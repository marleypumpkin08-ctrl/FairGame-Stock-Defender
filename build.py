"""
Build script for FairGame Stock Defender.
Creates a standalone executable using PyInstaller.
"""

import os
import sys
import subprocess
import platform


def build_executable():
    """Build the standalone executable."""
    print("Building FairGame Stock Defender executable...")

    # Determine platform-specific settings
    system = platform.system().lower()
    icon = None
    name = "FairGame_Stock_Defender"

    if system == "windows":
        icon = "assets/icon.ico" if os.path.exists("assets/icon.ico") else None
    elif system == "darwin":
        icon = "assets/icon.icns" if os.path.exists("assets/icon.icns") else None
    elif system == "linux":
        icon = None

    # Build PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", name,
        "--add-data", "config.json:.",
        "--add-data", "src:src",
        "--hidden-import", "customtkinter",
        "--hidden-import", "playwright",
        "--hidden-import", "bs4",
    ]

    if icon:
        cmd.extend(["--icon", icon])

    cmd.append("main.py")

    # Run PyInstaller
    print(f"Running: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
        print(f"\nBuild successful! Executable located in: dist/{name}")
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    build_executable()

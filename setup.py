"""
Setup script for FairGame Stock Defender.
Run this to install dependencies and set up the application.
"""

import subprocess
import sys
import os
import platform


def run_command(command, description):
    """Run a command and print status."""
    print(f"\n{description}...")
    try:
        subprocess.run(command, check=True, shell=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        return False


def main():
    """Main setup function."""
    print("=" * 60)
    print("FairGame Stock Defender - Setup")
    print("=" * 60)
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version.split()[0]}")
    print("=" * 60)

    # Install Python dependencies
    if not run_command(
        "pip install -r requirements.txt",
        "Installing Python dependencies"
    ):
        print("\nSetup failed. Please check the error above.")
        sys.exit(1)

    # Install Playwright browsers
    if not run_command(
        "playwright install chromium",
        "Installing Playwright Chromium browser"
    ):
        print("\nSetup failed. Please check the error above.")
        sys.exit(1)

    # Platform-specific setup
    if platform.system() == "Windows":
        print("\n✓ Windows-specific dependencies included in requirements.txt")
    elif platform.system() == "Darwin":
        print("\n✓ macOS-specific dependencies included in requirements.txt")
    elif platform.system() == "Linux":
        print("\n⚠ Note: On Linux, you may need to install libnotify-bin for notifications:")
        print("  sudo apt-get install libnotify-bin  # Debian/Ubuntu")
        print("  sudo dnf install libnotify          # Fedora")

    # Create data directory
    if not os.path.exists("data"):
        os.makedirs("data")
        print("\n✓ Created data directory")

    # Create assets directory
    if not os.path.exists("assets"):
        os.makedirs("assets")
        print("✓ Created assets directory")

    print("\n" + "=" * 60)
    print("Setup completed successfully!")
    print("=" * 60)
    print("\nTo run the application:")
    print("  python main.py")
    print("\nTo build an executable:")
    print("  python build.py")
    print("\nFor more information, see README.md")


if __name__ == "__main__":
    main()

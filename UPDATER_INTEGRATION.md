# Updater Integration

## Overview

The FairGame Stock Defender now uses a dedicated updater module hosted at:
**https://github.com/marleypumpkin08-ctrl/FairGame-Stock-Defender-updater-**

## Repository Structure

### Updater Repository (Separate)
```
FairGame-Stock-Defender-updater-/
├── updater.py          # Main updater module
├── requirements.txt    # Dependencies (requests)
├── setup.py           # Package installation
├── README.md          # Documentation
└── .gitignore         # Git ignore rules
```

### Main Application (FairGame Stock Defender)
```
FairGame Stock Defender/
├── src/
│   └── updater.py     # Local copy of updater (imported from repo)
├── config.json        # Configuration with github_repo setting
└── main.py           # Application entry point
```

## Configuration

The main application's `config.json` contains:

```json
{
  "github_repo": "marleypumpkin08-ctrl/FairGame-Stock-Defender",
  "updater_repo": "marleypumpkin08-ctrl/FairGame-Stock-Defender-updater-"
}
```

- `github_repo`: Main application repository where releases are published
- `updater_repo`: Dedicated updater module repository

## How It Works

1. **Application Startup**: The main application checks the GitHub Releases API for the repository specified in `github_repo`

2. **Version Comparison**: Compares local version (from config.json) with latest release tag

3. **Update Available**: If a newer version exists:
   - Shows modal dialog to user
   - Downloads platform-specific binary from release assets
   - Installs update safely
   - Prompts user to restart

4. **Platform Support**:
   - Windows: Downloads `.exe`, uses batch script for replacement
   - macOS: Downloads `.dmg`, opens for manual installation
   - Linux: Downloads `.AppImage`, makes executable and runs

## Asset Naming Convention

When publishing releases, name assets as:

- Windows: `FairGame-Stock-Defender-win.exe` or `FairGame-Stock-Defender.exe`
- macOS: `FairGame-Stock-Defender-mac.dmg` or `FairGame-Stock-Defender.dmg`
- Linux: `FairGame-Stock-Defender-linux.AppImage` or `FairGame-Stock-Defender.AppImage`

## Publishing Updates

1. Build the executable:
   ```bash
   python build.py
   ```

2. Create a new GitHub release:
   - Tag: `v1.7.0` (example)
   - Title: "Version 1.7.0"
   - Attach platform-specific executables

3. Users will automatically be notified on next application startup

## Updater Module Features

- ✅ GitHub Releases API integration
- ✅ Semantic version comparison
- ✅ Platform-specific asset detection
- ✅ Background update checking
- ✅ Progress callbacks for downloads
- ✅ Safe file replacement
- ✅ Error handling and timeouts
- ✅ Cross-platform support

## Security Notes

- Uses HTTPS for all API requests
- Validates version numbers before download
- Downloads only from official GitHub releases
- No execution of unverified code
- Safe file replacement with atomic operations

## Troubleshooting

### Update Not Detected
- Verify `github_repo` in config.json is correct
- Ensure release has a tag (e.g., `v1.6.0`)
- Check release has appropriate assets for your platform

### Download Fails
- Check internet connection
- Verify GitHub repository is public
- Ensure release assets are accessible

### Installation Fails
- Windows: Check file permissions in TEMP directory
- macOS: Ensure DMG opens correctly
- Linux: Verify AppImage permissions

## Future Enhancements

Potential improvements for the updater:

- [ ] Delta updates (download only changed files)
- [ ] Rollback capability if update fails
- [ ] Update verification with checksums
- [ ] Beta channel support
- [ ] Manual "Check for Updates" button
- [ ] Changelog display before update

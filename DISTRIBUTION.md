# Distribution Guide for FairGame Stock Defender

## File Size Issue

GitHub Releases has a 25MB file size limit. The FairGame Stock Defender executable is 73MB, which exceeds this limit.

## Distribution Options

### Option 1: External File Hosting (Recommended)

Use a free file hosting service and link from GitHub Releases:

**Free Hosting Services:**
- **Google Drive** - 15GB free storage
- **Dropbox** - 2GB free storage
- **MediaFire** - 10GB free storage
- **MEGA** - 20GB free storage
- **WeTransfer** - Free file transfer (no account needed)

**Steps:**
1. Upload `FairGame_Stock_Defender.exe` to your chosen service
2. Get the shareable link
3. Create a GitHub Release with the link in the description
4. Users download from the external link

**Example Release Description:**
```
## Download

Download the executable from: [External Link]

## Installation

1. Download FairGame_Stock_Defender.exe
2. Run install_browsers.bat (one-time setup)
3. Launch FairGame_Stock_Defender.exe

See USER_INSTALL_GUIDE.md for detailed instructions.
```

### Option 2: GitHub Actions (Build on Demand)

Set up GitHub Actions to build the executable on-demand and store it as an artifact.

**Advantages:**
- Builds are fresh
- No large files in git
- Artifacts stored for 90 days (free)
- Can extend storage with GitHub Actions cache

**Steps:**
1. Create `.github/workflows/build.yml`
2. Configure it to build the executable
3. Users trigger the build via GitHub Actions
4. Download the artifact from the Actions page

### Option 3: Split the File

Split the executable into smaller chunks that fit within the 25MB limit.

**Steps:**
1. Use a file splitter to divide the exe into 3 parts (~25MB each)
2. Upload all parts to GitHub Releases
3. Provide a script to recombine them

**Example using Python:**
```python
# Split file
import os
chunk_size = 25 * 1024 * 1024  # 25MB
with open('FairGame_Stock_Defender.exe', 'rb') as f:
    chunk_num = 0
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        with open(f'part{chunk_num}.bin', 'wb') as chunk_file:
            chunk_file.write(chunk)
        chunk_num += 1

# Combine file
with open('FairGame_Stock_Defender.exe', 'wb') as outfile:
    for i in range(3):  # Adjust based on number of parts
        with open(f'part{i}.bin', 'rb') as infile:
            outfile.write(infile.read())
```

### Option 4: Use GitHub LFS (Large File Storage)

GitHub LFS allows you to store large files up to 2GB per file.

**Steps:**
1. Install Git LFS: `git lfs install`
2. Track large files: `git lfs track "*.exe"`
3. Commit and push as normal
4. LFS files are stored separately and don't count toward repo size

**Cost:**
- Free: 1GB storage + 1GB bandwidth per month
- Paid: $5/month for 50GB storage + 50GB bandwidth

**Setup:**
```bash
git lfs install
git lfs track "*.exe"
git lfs track "*.zip"
git add .gitattributes
git commit -m "Track large files with LFS"
git push
```

### Option 5: Use a CDN or Dedicated Release Platform

**Options:**
- **Cloudflare R2** - Free tier (10GB storage, 10GB Class A operations/month)
- **Backblaze B2** - $0.005/GB/month storage, $0.01/GB download
- **AWS S3** - Free tier for first 12 months (5GB storage, 20GB transfer)

## Recommended Approach

**For Open Source Projects:**
Use **Option 1 (External Hosting)** with Google Drive or MediaFire. It's free, simple, and requires no configuration.

**For Professional Projects:**
Use **Option 2 (GitHub Actions)** or **Option 4 (GitHub LFS)** for better integration with GitHub.

## Current Status

The repository now contains:
- ✅ Source code
- ✅ Installation scripts
- ✅ Documentation
- ✅ Build scripts

To distribute:
1. Build the executable locally: `python build.py`
2. Upload to external hosting service
3. Create GitHub Release with download link
4. Or set up GitHub Actions for automated builds

## Building the Executable

```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browser
python -m playwright install chromium

# Build executable
python build.py

# Result: dist/FairGame_Stock_Defender.exe (73MB)
```

## Creating a Release with External Link

1. Go to GitHub Releases page
2. Click "Create a new release"
3. Tag: `v1.6.0`
4. Title: "Version 1.6.0"
5. Description:
   ```
   ## Download

   Windows (73MB): [Download from Google Drive]
   [Download from MediaFire]
   [Download from Dropbox]

   ## Installation

   1. Download FairGame_Stock_Defender.exe
   2. Run install_browsers.bat (one-time setup)
   3. Launch FairGame_Stock_Defender.exe

   See USER_INSTALL_GUIDE.md for detailed instructions.
   ```
6. Publish release

## Future Improvements

- [ ] Set up GitHub Actions for automated builds
- [ ] Implement GitHub LFS for large file tracking
- [ ] Add automated release workflow
- [ ] Create macOS and Linux builds
- [ ] Set up CDN for faster downloads

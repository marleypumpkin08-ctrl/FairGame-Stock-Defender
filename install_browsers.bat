@echo off
echo ========================================
echo FairGame Stock Defender - Browser Setup
echo ========================================
echo.
echo This will install the Playwright Chromium browser.
echo This is required for the application to work.
echo.
echo Download size: ~300MB
echo.
pause

echo Installing Playwright Chromium...
python -m playwright install chromium

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Installation successful!
    echo ========================================
    echo.
    echo You can now run FairGame_Stock_Defender.exe
    pause
) else (
    echo.
    echo ========================================
    echo Installation failed!
    echo ========================================
    echo.
    echo Please make sure Python is installed and try again.
    echo Or run: python -m playwright install chromium
    pause
)

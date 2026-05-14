@echo off
REM Update Professional Statistics Dashboard
REM This script generates fresh statistics from GitHub

echo.
echo ========================================
echo   PROFESSIONAL STATISTICS GENERATOR
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo [*] Collecting data from GitHub...
echo [*] This may take a moment...
echo.

python generate_stats.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to generate statistics
    echo.
    echo TROUBLESHOOTING:
    echo - Ensure you have internet connection
    echo - Check if your GitHub username is correct
    echo - Try setting GITHUB_TOKEN environment variable
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   SUCCESS! Statistics Updated
echo ========================================
echo.
echo FILES GENERATED:
echo   - stats.json (data file)
echo   - README.md (updated with stats)
echo   - activity_dashboard.html (view locally)
echo.
echo NEXT STEPS:
echo 1. Open 'activity_dashboard.html' to view the dashboard
echo 2. Check 'README.md' for the updated statistics section
echo 3. Commit changes to GitHub
echo.
pause

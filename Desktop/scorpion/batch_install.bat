@echo off
REM Scorpion-Effect Batch Installation Script for Windows
title Scorpion-Effect Installer
color 0A

echo ========================================
echo    🦂 SCORPION-EFFECT INSTALLER v2.0
echo ========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo [✓] Python found: 
python --version

REM Create virtual environment
echo.
echo [1/5] Creating virtual environment...
python -m venv scorpion_venv

REM Activate virtual environment
echo [2/5] Activating virtual environment...
call scorpion_venv\Scripts\activate.bat

REM Upgrade pip
echo [3/5] Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo [4/5] Installing Python packages...
pip install -r requirements.txt

REM Install additional Windows tools (optional)
echo [5/5] Installing optional tools...
where nmap >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Nmap not found. Installing Nmap is recommended.
    echo Download from: https://nmap.org/download.html
)

REM Create directories
mkdir .scorpion-effect 2>nul
mkdir reports 2>nul
mkdir phishing_data 2>nul
mkdir logs 2>nul

REM Create initial config
if not exist .scorpion-effect\config.json (
    echo Creating initial configuration...
    echo {> .scorpion-effect\config.json
    echo   "web_port": 5000,>> .scorpion-effect\config.json
    echo   "enable_web": true>> .scorpion-effect\config.json
    echo }>> .scorpion-effect\config.json
)

echo.
echo ========================================
echo    ✅ INSTALLATION COMPLETE!
echo ========================================
echo.
echo To run Scorpion-Effect:
echo   1. scorpion_venv\Scripts\activate
echo   2. python scorpion_effect.py
echo.
echo Or run directly:
echo   scorpion_venv\Scripts\python scorpion_effect.py
echo.

pause
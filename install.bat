@echo off
:: install.bat - BIG-PHISH Installation Script for Windows
:: Author: Ian Carter Kulani
:: Version: 2.0.0

setlocal enabledelayedexpansion

:: Colors for Windows (ANSI escape codes if supported)
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "RESET=[0m"

:: Configuration
set "APP_NAME=bigphish"
set "APP_DIR=%ProgramFiles%\BigPhish"
set "DATA_DIR=%ProgramData%\BigPhish"
set "LOG_DIR=%ProgramData%\BigPhish\logs"
set "CONFIG_DIR=%ProgramData%\BigPhish\config"

echo %BLUE%[*] Starting BIG-PHISH installation...%RESET%
echo.

:: Check for Administrator privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo %RED%[!] This script must be run as Administrator!%RESET%
    echo    Right-click on Command Prompt and select "Run as administrator"
    pause
    exit /b 1
)

:: Check Python installation
echo %BLUE%[*] Checking Python installation...%RESET%
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo %RED%[!] Python not found!%RESET%
    echo    Download and install Python 3.7+ from https://python.org
    echo    Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

python --version
echo %GREEN%[+] Python found%RESET%
echo.

:: Create directories
echo %BLUE%[*] Creating directories...%RESET%
if not exist "%APP_DIR%" mkdir "%APP_DIR%"
if not exist "%DATA_DIR%" mkdir "%DATA_DIR%"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
if not exist "%CONFIG_DIR%" mkdir "%CONFIG_DIR%"

:: Create data subdirectories
mkdir "%DATA_DIR%\payloads" 2>nul
mkdir "%DATA_DIR%\workspaces" 2>nul
mkdir "%DATA_DIR%\scans" 2>nul
mkdir "%DATA_DIR%\nikto_results" 2>nul
mkdir "%DATA_DIR%\whatsapp_session" 2>nul
mkdir "%DATA_DIR%\phishing_pages" 2>nul
mkdir "%DATA_DIR%\traffic_logs" 2>nul
mkdir "%DATA_DIR%\phishing_templates" 2>nul
mkdir "%DATA_DIR%\captured_credentials" 2>nul
mkdir "%DATA_DIR%\ssh_keys" 2>nul
mkdir "%DATA_DIR%\ssh_logs" 2>nul
mkdir "%DATA_DIR%\time_history" 2>nul
mkdir "%DATA_DIR%\wordlists" 2>nul

echo %GREEN%[+] Directories created%RESET%
echo.

:: Copy files
echo %BLUE%[*] Copying application files...%RESET%
copy "bigphish.py" "%APP_DIR%\" >nul
copy "requirements.txt" "%APP_DIR%\" >nul
echo %GREEN%[+] Files copied to %APP_DIR%%RESET%
echo.

:: Install Python dependencies
echo %BLUE%[*] Installing Python dependencies...%RESET%
echo    This may take a few minutes...

cd /d "%APP_DIR%"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if %errorLevel% neq 0 (
    echo %YELLOW%[⚠] Some dependencies may have failed to install%RESET%
    echo    You may need to install Visual C++ Build Tools
    echo    Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
) else (
    echo %GREEN%[+] Python dependencies installed%RESET%
)
echo.

:: Create configuration file
echo %BLUE%[*] Creating configuration...%RESET%
(
echo {
echo     "monitoring": {"enabled": true, "port_scan_threshold": 10},
echo     "scanning": {"default_ports": "1-1000", "timeout": 30},
echo     "security": {"auto_block": false, "log_level": "INFO"},
echo     "nikto": {"enabled": true, "timeout": 300},
echo     "traffic_generation": {"enabled": true, "max_duration": 300, "allow_floods": false},
echo     "social_engineering": {"enabled": true, "default_port": 8080, "capture_credentials": true},
echo     "crunch": {"enabled": true, "max_file_size_mb": 1024, "default_output_dir": "%DATA_DIR%\\wordlists"},
echo     "ssh": {"enabled": true, "default_timeout": 30, "max_connections": 5}
echo }
) > "%CONFIG_DIR%\config.json"

echo %GREEN%[+] Configuration created%RESET%
echo.

:: Create startup script
echo %BLUE%[*] Creating startup scripts...%RESET%

:: Create batch launcher
(
echo @echo off
echo set "PYTHONUNBUFFERED=1"
echo cd /d "%APP_DIR%"
echo python bigphish.py
echo pause
) > "%APP_DIR%\run.bat"

:: Create PowerShell launcher
(
echo $env:PYTHONUNBUFFERED = "1"
echo Set-Location "%APP_DIR%"
echo python bigphish.py
echo Read-Host "Press Enter to exit"
) > "%APP_DIR%\run.ps1"

echo %GREEN%[+] Startup scripts created%RESET%
echo.

:: Create Windows Service using NSSM (if available)
echo %BLUE%[*] Checking for NSSM...%RESET%
where nssm >nul 2>&1
if %errorLevel% equ 0 (
    echo %GREEN%[+] NSSM found, creating Windows Service...%RESET%
    nssm install BigPhish "%APP_DIR%\run.bat"
    nssm set BigPhish DisplayName "BIG-PHISH Cybersecurity Command Center"
    nssm set BigPhish Description "Ultimate Cybersecurity & Phishing Command Center"
    nssm set BigPhish Start SERVICE_AUTO_START
    echo %GREEN%[+] Windows Service created%RESET%
) else (
    echo %YELLOW%[⚠] NSSM not found%RESET%
    echo    Download NSSM from https://nssm.cc/download
    echo    Then run: nssm install BigPhish "%APP_DIR%\run.bat"
)
echo.

:: Create firewall rule
echo %BLUE%[*] Creating firewall rule...%RESET%
netsh advfirewall firewall add rule name="BigPhish Web UI" dir=in action=allow protocol=tcp localport=8080 >nul
netsh advfirewall firewall add rule name="BigPhish SSH" dir=in action=allow protocol=tcp localport=22 >nul
echo %GREEN%[+] Firewall rules created%RESET%
echo.

:: Create scheduled task for monitoring
echo %BLUE%[*] Creating scheduled task for monitoring...%RESET%
schtasks /create /tn "BigPhish Health Check" /tr "powershell -Command \"try { (Invoke-WebRequest -Uri http://localhost:8080 -UseBasicParsing).StatusCode } catch { exit 1 }\"" /sc hourly /mo 1 /ru SYSTEM >nul 2>&1
echo %GREEN%[+] Scheduled task created%RESET%
echo.

:: Create log rotation script
echo %BLUE%[*] Creating log rotation script...%RESET%
(
echo $logPath = "%LOG_DIR%\bigphish.log"
echo $maxSizeMB = 100
echo $backupCount = 7
echo 
echo if (Test-Path $logPath) {
echo     $fileInfo = Get-Item $logPath
echo     if ($fileInfo.Length -gt ($maxSizeMB * 1MB)) {
echo         $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
echo         $backupPath = "%LOG_DIR%\bigphish_$timestamp.log"
echo         Move-Item $logPath $backupPath
echo         Compress-Archive -Path $backupPath -DestinationPath "$backupPath.zip"
echo         Remove-Item $backupPath
echo         
echo         # Remove old backups
echo         Get-ChildItem "%LOG_DIR%\bigphish_*.zip" ^| Sort-Object LastWriteTime -Descending ^| Select-Object -Skip $backupCount ^| Remove-Item
echo     }
echo }
) > "%APP_DIR%\rotate-logs.ps1"

echo %GREEN%[+] Log rotation script created%RESET%
echo.

:: Create desktop shortcut
echo %BLUE%[*] Creating desktop shortcut...%RESET%
set "DESKTOP=%USERPROFILE%\Desktop"
if exist "%DESKTOP%" (
    powershell -Command "$WScriptShell = New-Object -ComObject WScript.Shell; $Shortcut = $WScriptShell.CreateShortcut('%DESKTOP%\BigPhish.lnk'); $Shortcut.TargetPath = '%APP_DIR%\run.bat'; $Shortcut.WorkingDirectory = '%APP_DIR%'; $Shortcut.Save()"
    echo %GREEN%[+] Desktop shortcut created%RESET%
)
echo.

:: Display summary
echo.
echo ==========================================
echo %GREEN%BIG-PHISH Installation Complete!%RESET%
echo ==========================================
echo.
echo %BLUE%Installation Details:%RESET%
echo   Application Directory: %APP_DIR%
echo   Data Directory: %DATA_DIR%
echo   Log Directory: %LOG_DIR%
echo   Config Directory: %CONFIG_DIR%
echo.
echo %BLUE%Access Information:%RESET%
echo   Web Interface: http://localhost:8080
echo   API Endpoint: http://localhost:8080/api
echo.
echo %BLUE%Management Commands:%RESET%
echo   Start: Run "%APP_DIR%\run.bat"
echo   OR: Start "BigPhish" service if installed with NSSM
echo.
echo %BLUE%Logs:%RESET%
echo   Log File: %LOG_DIR%\bigphish.log
echo.
echo %YELLOW%[⚠] Important Notes:%RESET%
echo   1. Run as Administrator for full functionality
echo   2. Configure platform bots in the web interface
echo   3. Check Windows Firewall if accessing remotely
echo   4. Default configuration: %CONFIG_DIR%\config.json
echo.
echo %GREEN%Thank you for installing BIG-PHISH!%RESET%
echo.

:: Ask to start application
set /p "start_now=Start BIG-PHISH now? (y/n): "
if /i "!start_now!"=="y" (
    start "" "%APP_DIR%\run.bat"
    echo %GREEN%BIG-PHISH started!%RESET%
)

pause
@echo off
REM Maintainer script: builds Ormyn and puts the exe + checksum into release\v<VER>\
setlocal
set VER=1.0.0
cd /d "%~dp0.."

where dotnet >nul 2>nul
if errorlevel 1 (
  echo .NET 8 SDK not found.
  pause
  exit /b 1
)

if not exist "manual-download\src\Ormyn\Ormyn.csproj" (
  echo Could not find manual-download\src\Ormyn\Ormyn.csproj. Run this from inside the full repo folder.
  pause
  exit /b 1
)

dotnet publish manual-download\src\Ormyn\Ormyn.csproj -c Release -r win-x64 --self-contained false ^
  -p:PublishSingleFile=true -p:PublishReadyToRun=true -p:DebugType=None -p:DebugSymbols=false ^
  -p:Version=%VER% -o release\v%VER%
if errorlevel 1 (
  echo BUILD FAILED
  pause
  exit /b 1
)

powershell -NoProfile -Command "(Get-FileHash 'release\v%VER%\Ormyn.exe' -Algorithm SHA256).Hash.ToLower() + '  Ormyn.exe' | Set-Content -Encoding ascii 'release\v%VER%\SHA256SUMS.txt'"
echo.
echo Staged release\v%VER%\Ormyn.exe and SHA256SUMS.txt
pause

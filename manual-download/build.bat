@echo off
setlocal
cd /d "%~dp0"

where dotnet >nul 2>nul
if errorlevel 1 (
  echo .NET 8 SDK not found. Install it from https://dotnet.microsoft.com/download/dotnet/8.0
  echo or run:  winget install Microsoft.DotNet.SDK.8
  pause
  exit /b 1
)

if not exist "src\Ormyn\Ormyn.csproj" (
  echo Could not find src\Ormyn\Ormyn.csproj next to this script.
  echo Extract the WHOLE zip first. Do not run build.bat from inside the zip viewer or copy it on its own.
  pause
  exit /b 1
)
if not exist "..\theme\ormyn.ico" (
  echo NOTE: the theme folder was not found next to manual-download, so Ormyn will build with a default icon.
  echo       Keep the theme folder beside manual-download to get the custom icon.
)

echo Building Ormyn...
dotnet publish src\Ormyn\Ormyn.csproj -c Release -r win-x64 --self-contained false ^
  -p:PublishSingleFile=true -p:PublishReadyToRun=true -p:DebugType=None -p:DebugSymbols=false -o publish
if errorlevel 1 (
  echo.
  echo BUILD FAILED - see the errors above.
  pause
  exit /b 1
)

echo.
echo Built: %~dp0publish\Ormyn.exe
echo Needs the .NET 8 Desktop Runtime to run (the SDK already includes it).
pause

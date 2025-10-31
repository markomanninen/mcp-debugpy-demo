@echo off
REM Setup script for mcp-debugpy-demo (Windows)

echo Setting up mcp-debugpy-demo...
echo.

REM Check Python version
python --version
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8 or higher.
    exit /b 1
)
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    exit /b 1
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    exit /b 1
)
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo Installing dependencies...
pip install pytest pytest-asyncio
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)
echo.

REM Install mcp-debugpy from GitHub
echo Installing mcp-debugpy from GitHub...
pip install git+https://github.com/markomanninen/mcp-debugpy.git
if errorlevel 1 (
    echo ERROR: Failed to install mcp-debugpy
    exit /b 1
)
echo.

echo ========================================
echo Setup complete!
echo ========================================
echo.
echo To activate the environment, run:
echo   .venv\Scripts\activate
echo.
echo To run the buggy application:
echo   python shopping_cart.py
echo.
echo To run tests and see the bug:
echo   pytest test_shopping_cart.py -v
echo.
echo To configure MCP for VS Code, the settings are in .vscode\settings.json
echo Make sure you have the MCP extension installed in VS Code.
echo.
pause

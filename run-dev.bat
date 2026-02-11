@echo off
REM HomeBuddy Development Server Startup Script (Windows)
REM This script starts the backend in development mode

echo.
echo 🏠 HomeBuddy Development Setup (Windows)
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH. Please install Python 3.9 or higher.
    echo    Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Navigate to Backend
echo 📦 Setting up Backend...
cd Backend

REM Create virtual environment if it doesn't exist
if not exist "myenv" (
    echo Creating virtual environment...
    python -m venv myenv
)

REM Activate virtual environment
call myenv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Setup database
echo Setting up database...
python -c "from db.database import Base, engine; Base.metadata.create_all(bind=engine); print('✓ Database ready')"

REM Start backend server
echo.
echo 🚀 Starting Backend API Server...
echo    API will be available at: http://localhost:8000
echo    API Docs at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause

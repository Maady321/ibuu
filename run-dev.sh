#!/bin/bash

# HomeBuddy Development Server Startup Script
# This script starts both the backend and frontend in development mode

echo "🏠 HomeBuddy Development Setup"
echo "=============================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip is not installed. Please install pip."
    exit 1
fi

# Set up Backend
echo ""
echo "📦 Setting up Backend..."
cd Backend

# Create virtual environment if it doesn't exist
if [ ! -d "myenv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv myenv
fi

# Activate virtual environment
if [ -f "myenv/bin/activate" ]; then
    source myenv/bin/activate
elif [ -f "myenv/Scripts/activate" ]; then
    source myenv/Scripts/activate
fi

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Run migrations/setup
echo "Setting up database..."
python -c "from db.database import Base, engine; Base.metadata.create_all(bind=engine); print('✓ Database ready')"

# Start backend server
echo ""
echo "🚀 Starting Backend API Server..."
echo "   API will be available at: http://localhost:8000"
echo "   API Docs at: http://localhost:8000/docs"
echo ""

python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

cd ..

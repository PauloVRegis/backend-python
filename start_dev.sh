#!/bin/bash

# SmartForce Development Startup Script
# This script sets up and runs the SmartForce workout app in development mode

set -e

echo "🚀 Starting SmartForce Development Environment"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.11+"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.11"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python $REQUIRED_VERSION+ is required, but you have $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Set development environment variables
export ENVIRONMENT=development
export DEBUG=true
export DATABASE_URL=sqlite+aiosqlite:///./smart_force.db
export SECRET_KEY=dev-secret-key-change-in-production
export LOG_LEVEL=DEBUG

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
# Development Environment Configuration
DATABASE_URL=sqlite+aiosqlite:///./smart_force.db
SECRET_KEY=dev-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=true
ENVIRONMENT=development
LOG_LEVEL=DEBUG
ALLOWED_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]
RATE_LIMIT_PER_MINUTE=100
EOF
    echo "✅ .env file created"
fi

# Initialize database
echo "🗄️ Initializing database..."
python -c "
from app.database.session import init_db
init_db()
print('Database initialized successfully')
"

# Check if Redis is available (optional for development)
if command -v redis-cli &> /dev/null; then
    if redis-cli ping &> /dev/null; then
        echo "✅ Redis is available"
        export REDIS_URL=redis://localhost:6379
    else
        echo "⚠️ Redis is not running (optional for development)"
    fi
else
    echo "⚠️ Redis not installed (optional for development)"
fi

# Start the application
echo "🎯 Starting SmartForce application..."
echo "📍 API will be available at: http://localhost:8000"
echo "📖 API documentation at: http://localhost:8000/docs"
echo "🏥 Health check at: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Run the application with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug 
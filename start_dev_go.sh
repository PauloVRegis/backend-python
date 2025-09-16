#!/bin/bash

# SmartForce Go Development Startup Script

echo "🚀 Starting SmartForce Go Backend Development Environment"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please review and update the configuration."
fi

# Install dependencies
echo "📦 Installing Go dependencies..."
go mod tidy

# Check if database exists, if not create it
if [ ! -f smart_force.db ]; then
    echo "🗄️  Creating SQLite database..."
    touch smart_force.db
fi

# Run the application
echo "🏃 Starting SmartForce Go backend..."
echo "📡 Server will be available at: http://localhost:8000"
echo "📊 Health check: http://localhost:8000/health"
echo "📈 Metrics: http://localhost:8000/metrics"
echo "📚 API Documentation will be available when Swagger is implemented"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Set environment for development
export DEBUG=true
export ENVIRONMENT=development
export LOG_LEVEL=DEBUG

# Run the application with live reload using Air (if available)
if command -v air &> /dev/null; then
    echo "🔄 Running with Air for live reload..."
    air
else
    echo "💡 Tip: Install Air for live reload: go install github.com/cosmtrek/air@latest"
    echo "🚀 Running Go application..."
    go run main.go
fi

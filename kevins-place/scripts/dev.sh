#!/bin/bash
# KEVIN's Place - Development Setup Script

echo "🏠 KEVIN's Place - Setting up development environment..."
echo "=================================================="

# Navigate to backend
cd "$(dirname "$0")/../backend" || exit 1

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt --quiet

# Run the server
echo ""
echo "🚀 Starting KEVIN's Place API..."
echo "   API Docs: http://localhost:8000/docs"
echo "   Health:   http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop"
echo "=================================================="

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

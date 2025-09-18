#!/bin/bash

# Smart Email Reply System Setup Script

echo "🤖 Setting up Smart Email Reply System..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3."
    exit 1
fi

echo "✅ pip3 found"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📋 Installing dependencies..."
pip install -r requirements.txt

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama is not installed. Please install Ollama from https://ollama.ai"
    echo "   After installation, run: ollama pull llama3.1:8b"
else
    echo "✅ Ollama found"
    echo "🔄 Pulling llama3.1:8b model..."
    ollama pull llama3.1:8b
fi

# Create config file from template
if [ ! -f "config.py" ]; then
    echo "⚙️  Creating configuration file..."
    cp config_template.py config.py
    echo "📝 Please edit config.py with your actual credentials before running the system."
else
    echo "✅ Configuration file already exists"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p data
mkdir -p logs

echo "✅ Setup completed!"
echo ""
echo "📋 Next steps:"
echo "1. Edit config.py with your actual credentials"
echo "2. Set up Gmail app-specific password"
echo "3. Configure AWS Textract credentials"
echo "4. Run the application: cd src && python app.py"
echo ""
echo "📖 For detailed instructions, see README.md"
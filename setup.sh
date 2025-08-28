#!/bin/bash
# Setup script for Web Audit Project

echo "🚀 Setting up Web Audit Project..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv web_audit_env

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source web_audit_env/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "1. Activate the environment: source web_audit_env/bin/activate"
echo "2. Run the app: streamlit run streamlit_web_audit.py"
echo ""
echo "🌐 The app will be available at: http://localhost:8501"

#!/bin/bash

set -e

echo "🔧 Installing system dependencies..."
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git ffmpeg

echo "📁 Setting up project directory..."
mkdir -p ~/birdnet
cd ~/birdnet

echo "🐍 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install influxdb-client pandas

echo "⬇️ Cloning BirdNET-Analyzer..."
git clone https://github.com/kahst/BirdNET-Analyzer.git
cd BirdNET-Analyzer
pip install -r requirements.txt
cd ..

echo "✅ Setup complete."
echo "To start, activate your environment:"
echo "  source ~/birdnet/venv/bin/activate"
echo "Then run:"
echo "  python birding.py"


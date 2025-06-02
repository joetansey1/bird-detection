# bird-detection
📸 Birding.py – Automated Bird & Wildlife Detection on Raspberry Pi
Birding.py is a lightweight Python-based detection loop that captures audio (and optionally video), runs it through a species identification model (BirdNET), and logs the detections locally and to InfluxDB. Can also be extended to run general object detection (e.g. humans, cars, bikes) using YOLOv5 or other models.

🐦 Features
Records short audio clips (configurable)
Runs detections using BirdNET-Analyzer

Logs:
Detected species
Timestamp
Confidence
.wav and .csv output
Writes results:
Local CSV
InfluxDB HTTP API (for Grafana dashboards)
Configurable confidence thresholds
Future support for video inference and multi-object detection

🧰 Requirements
Raspberry Pi 4 or better (w/ Linux OS)
Microphone (USB or I2S)
Python 3.9+
InfluxDB v2
BirdNET-Analyzer

⚙️ Installation
Run the setup script to install dependencies and clone BirdNET-Analyzer:
curl -sSL https://raw.githubusercontent.com/YOUR_USERNAME/birding/main/install.sh | bash
Manual installation:
git clone https://github.com/YOUR_USERNAME/birding.git
cd birding

# Create Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Download BirdNET-Analyzer
git clone https://github.com/kahst/BirdNET-Analyzer.git
cd BirdNET-Analyzer
pip install -r requirements.txt

🔁 Usage
python birding.py
This will:
Record an audio sample (e.g. 15s)
Analyze with BirdNET
Log results to InfluxDB and CSV

📊 Grafana Integration
InfluxDB schema (example):
measurement: detections
tags: species
fields: confidence, filename
timestamp: detection time
Panel ideas:
Top species (last 24h)
Detection confidence over time
Sound activity map (heatmap)

🔧 Configuration
Update variables in birding.py to customize:
RECORD_DURATION_SEC
MIN_CONFIDENCE
INFLUXDB_URL, TOKEN, ORG, BUCKET

🐛 Known Issues
Autofocus may require manual tuning (camera-dependent)
Microphone quality heavily impacts detection accuracy
May require CPU throttling or batching if run 24/7

# birdnet_loop.py
import os
import time
import datetime
import subprocess
import csv
import requests

INFLUX_URL = "http://localhost:8086/api/v2/write"
INFLUX_BUCKET = "birdnet"
INFLUX_ORG = "localorg"
INFLUX_TOKEN = "HzqaSJhhHpPfdbYq4PJ7hawzux5u5_DsQGd5ByYQf0Hpd6vGNd6UwsgV09Q_ieu-dUinROiqHadWBrs_7_pyWg==" # Make sur>

RECORD_SECONDS = 20
SLEEP_SECONDS = 5
AUDIO_DIR = os.path.expanduser("~/birdnet")

print("🐦 BirdNET Python loop started...")

import socket

def wait_for_influx(host, port, timeout=60):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=5):
                print("✅ InfluxDB is reachable!")
                return True
        except OSError:
            print("🔁 Waiting for InfluxDB to come online...")
            time.sleep(5)
    print("❌ Timeout waiting for InfluxDB.")
    return False

# Add this before the main while loop
if not wait_for_influx("192.168.1.75", 8086):
    exit(1)



while True:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_path = os.path.join(AUDIO_DIR, f"recording_{timestamp}.wav")
    mono_path = raw_path.replace(".wav", "_mono.wav")
  
    print(f"🎙️ Recording to {raw_path}...")
    arecord_cmd = [
        "arecord", "-D", "hw:2,0", "-f", "cd", "-r", "48000", "-c", "2",
        "-d", str(RECORD_SECONDS), raw_path
    ]
    subprocess.run(arecord_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("🎛️ Converting to mono...")
    sox_cmd = [
        "sox", raw_path, mono_path, "remix", "1"
    ]
    subprocess.run(sox_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"🔍 Analyzing {mono_path}...")
    analyze_cmd = [
        "/home/joetanse/birdnet-env/bin/birdnet-analyze",
        mono_path,
        "-o", AUDIO_DIR,
        "--lat", "37.7749",
        "--lon", "-122.4194",
        "--min_conf", "0.1",
        "--rtype", "csv",
        "--sensitivity", "1.0",
        "--sf_thresh", "0.07",
        "--combine_results"
    ]
    subprocess.run(analyze_cmd)

    result_csv = mono_path.replace(".wav", ".BirdNET.results.csv")
    if os.path.exists(result_csv):
        with open(result_csv, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                confidence = float(row['Confidence'])
                if confidence < 0.15:
                    continue

                timestamp = datetime.datetime.now().isoformat()
                species = row['Common name'].replace(" ", "_")
                line = f"detections,species={species} confidence={confidence} {int(time.time() * 1e9)}"

                headers = {
                    "Authorization": f"Token {INFLUX_TOKEN}",
                    "Content-Type": "text/plain"
                }

                response = requests.post(
                    f"{INFLUX_URL}?org={INFLUX_ORG}&bucket={INFLUX_BUCKET}&precision=ns",
                    headers=headers,
                    data=line
                )

                if response.status_code != 204:
                    print(f"⚠️ InfluxDB write failed: {response.text}")
                else:
                    print(f"✅ Logged {species} ({confidence}) to InfluxDB")
                      else:
        print(f"⚠️ No result CSV found for {mono_path}")

    print(f"😴 Sleeping {SLEEP_SECONDS} seconds...")
    time.sleep(SLEEP_SECONDS)

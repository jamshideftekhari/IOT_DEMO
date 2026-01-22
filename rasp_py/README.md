# Raspberry Pi Client Scripts

Python scripts for sending temperature and humidity data from Raspberry Pi to the IoT API.

## Scripts Overview

| Script | Description |
|--------|-------------|
| `01_fake_measurement.py` | Sends fake test data to verify API connection |
| `02_sensehat_joystick.py` | Reads real data from Sense HAT, sends on joystick press |

## Prerequisites

### On Raspberry Pi

1. **Python 3** (pre-installed on Raspberry Pi OS)

2. **requests library** - for making HTTP requests:
   ```bash
   pip install requests
   ```

3. **Sense HAT library** (for Script 2):
   ```bash
   sudo apt install sense-hat
   ```

### On Server

Make sure the IoT API server is running and accessible on the network:
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Configuration

Before running the scripts, update the `API_URL` to match your server's IP address.

Find your server's IP address:
- **Windows:** Run `ipconfig` and look for "IPv4 Address"
- **Linux/Mac:** Run `hostname -I` or `ip addr`

Edit the scripts and change:
```python
API_URL = "http://192.168.1.100:8000"  # Change to your server's IP
```

You can also customize the `DEVICE_ID` to identify each Raspberry Pi:
```python
DEVICE_ID = "raspberry-pi-01"  # Change for each device
```

---

## Script 1: Fake Measurement

**File:** `01_fake_measurement.py`

This script sends hardcoded (fake) temperature and humidity values to the API. Use it to test your network connection and API setup before working with real sensors.

### Purpose
- Verify the API server is reachable
- Test the connection from Raspberry Pi to server
- Understand the basic structure of sending data

### Usage
```bash
python 01_fake_measurement.py
```

### Expected Output
```
Sending fake measurement to http://192.168.1.100:8000
  Device ID: raspberry-pi-01
  Temperature: 22.5°C
  Humidity: 55.0%

Measurement sent successfully!
Response: {'id': 1, 'device_id': 'raspberry-pi-01', 'temperature': 22.5, 'humidity': 55.0, 'timestamp': '2026-01-22T12:00:00.000000'}
```

### Troubleshooting
- **"Could not connect to API"** - Check the IP address and ensure the server is running
- **Connection timeout** - Check firewall settings on the server

---

## Script 2: Sense HAT with Joystick

**File:** `02_sensehat_joystick.py`

This script reads real temperature and humidity from the Sense HAT sensor and sends the data to the API each time you press the joystick.

### Purpose
- Read real sensor data from Sense HAT
- Interactive control using the joystick
- Visual feedback via LED matrix

### Hardware Required
- Raspberry Pi (any model with GPIO)
- Sense HAT attached to GPIO header

### Usage
```bash
python 02_sensehat_joystick.py
```

### Controls
| Action | Result |
|--------|--------|
| Press joystick (middle) | Send current reading to API |
| Ctrl+C | Exit the program |

### LED Feedback
| Colour | Meaning |
|--------|---------|
| Blue | Ready - waiting for joystick press |
| Green | Success - data sent successfully |
| Red | Error - connection failed or API error |

### Expected Output
```
==================================================
Sense HAT IoT Client
==================================================
API Server: http://192.168.1.100:8000
Device ID: raspberry-pi-01

Press the joystick to send a reading.
Press Ctrl+C to exit.
==================================================

Reading: 24.3°C, 62.1%
Sent: 24.3°C, 62.1% - OK

Reading: 24.5°C, 61.8%
Sent: 24.5°C, 61.8% - OK
```

### Note on Temperature Accuracy
The Sense HAT temperature sensor can read slightly high due to heat from the Raspberry Pi CPU. To compensate, you can uncomment this line in the script:
```python
# temperature = temperature - 5
```

---

## Quick Start Guide

### Step 1: Start the API Server
On your server machine:
```bash
cd IOT_DEMO
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Step 2: Copy Scripts to Raspberry Pi
Copy the `rasp_py` folder to your Raspberry Pi using SCP, USB drive, or direct download.

Using SCP from your server:
```bash
scp -r rasp_py/ pi@<raspberry-pi-ip>:~/
```

### Step 3: Configure and Run
On the Raspberry Pi:
```bash
cd ~/rasp_py

# Edit the API_URL in the script
nano 01_fake_measurement.py

# Test with fake data first
python 01_fake_measurement.py

# Then try with real Sense HAT data
python 02_sensehat_joystick.py
```

---

## Exercises for Students

1. **Modify fake data** - Change the temperature and humidity values in Script 1 and observe the API response

2. **Change device ID** - Use different `DEVICE_ID` values and query the API to filter by device

3. **Add continuous sending** - Modify Script 2 to send data automatically every 10 seconds instead of on joystick press

4. **Display on LED** - Modify Script 2 to scroll the temperature value on the LED matrix before sending

5. **Add error retry** - Implement automatic retry if the API connection fails

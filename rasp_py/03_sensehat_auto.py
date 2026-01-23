"""
Script 3: Sense HAT Automatic Measurements (15 min interval)
============================================================
This script automatically reads temperature and humidity from the Sense HAT
and sends data to the API every 15 minutes. Each iteration displays
measurements in a different color on the LED matrix.

Requirements:
    - Raspberry Pi with Sense HAT attached
    - sense-hat library: sudo apt install sense-hat
    - requests library: pip install requests

Usage:
    python 03_sensehat_auto.py

Controls:
    - Ctrl+C: Exit the program
"""

import time
import requests
from sense_hat import SenseHat

# API Configuration
API_URL = "http://192.168.1.100:8080"  # Change to your server's IP address
DEVICE_ID = "raspberry-pi-01"

# Interval in seconds (15 minutes = 900 seconds)
INTERVAL_SECONDS = 15 * 60

# Colors to cycle through (R, G, B)
COLORS = [
    (255, 0, 0),      # Red
    (0, 255, 0),      # Green
    (0, 0, 255),      # Blue
    (255, 255, 0),    # Yellow
    (255, 0, 255),    # Magenta
    (0, 255, 255),    # Cyan
    (255, 128, 0),    # Orange
    (128, 0, 255),    # Purple
]

# Initialize Sense HAT
sense = SenseHat()

def get_sensor_data():
    """Read temperature and humidity from Sense HAT."""
    temperature = sense.get_temperature()
    humidity = sense.get_humidity()

    # Optional: Compensate for CPU heat
    # temperature = temperature - 5

    return round(temperature, 1), round(humidity, 1)

def send_measurement(temperature, humidity):
    """Send a measurement to the API."""
    endpoint = f"{API_URL}/measurements"

    data = {
        "device_id": DEVICE_ID,
        "temperature": temperature,
        "humidity": humidity
    }

    try:
        response = requests.post(endpoint, json=data, timeout=10)

        if response.status_code == 201:
            return True, "OK"
        else:
            return False, f"Error {response.status_code}"

    except requests.exceptions.ConnectionError:
        return False, "Connection failed"
    except requests.exceptions.Timeout:
        return False, "Timeout"

def display_measurement(temperature, humidity, color):
    """Display measurement on LED matrix with scrolling text."""
    sense.clear()

    # Show color briefly
    sense.clear(color)
    time.sleep(0.5)

    # Scroll temperature
    message = f"{temperature}C {humidity}%"
    sense.show_message(message, text_colour=color, scroll_speed=0.06)

def show_status(success, color):
    """Show success or failure status on LED."""
    if success:
        # Flash the color 3 times for success
        for _ in range(3):
            sense.clear(color)
            time.sleep(0.2)
            sense.clear()
            time.sleep(0.2)
    else:
        # Show red X pattern for error
        error_pattern = [
            (255, 0, 0) if (x == y or x == 7 - y) else (0, 0, 0)
            for y in range(8) for x in range(8)
        ]
        sense.set_pixels(error_pattern)
        time.sleep(2)

    # Dim the color to show idle/waiting state
    dim_color = tuple(c // 10 for c in color)
    sense.clear(dim_color)

def main():
    print("=" * 50)
    print("Sense HAT Auto IoT Client")
    print("=" * 50)
    print(f"API Server: {API_URL}")
    print(f"Device ID: {DEVICE_ID}")
    print(f"Interval: {INTERVAL_SECONDS // 60} minutes")
    print()
    print("Press Ctrl+C to exit.")
    print("=" * 50)

    iteration = 0

    try:
        while True:
            # Get color for this iteration
            color = COLORS[iteration % len(COLORS)]
            color_name = ["Red", "Green", "Blue", "Yellow",
                         "Magenta", "Cyan", "Orange", "Purple"][iteration % len(COLORS)]

            # Read sensor data
            temperature, humidity = get_sensor_data()

            # Get current time
            current_time = time.strftime("%H:%M:%S")

            print(f"\n[{current_time}] Iteration {iteration + 1} ({color_name})")
            print(f"  Temperature: {temperature}°C")
            print(f"  Humidity: {humidity}%")

            # Display on LED matrix
            display_measurement(temperature, humidity, color)

            # Send to API
            success, message = send_measurement(temperature, humidity)
            print(f"  Status: {message}")

            # Show status on LED
            show_status(success, color)

            # Increment iteration counter
            iteration += 1

            # Wait for next interval
            print(f"\nNext reading in {INTERVAL_SECONDS // 60} minutes...")
            time.sleep(INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\n\nExiting...")
        sense.clear()

if __name__ == "__main__":
    main()

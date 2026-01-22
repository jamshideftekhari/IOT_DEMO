"""
Script 2: Sense HAT Temperature & Humidity with Joystick
========================================================
This script reads real temperature and humidity from the Sense HAT
and sends the data to the API when the joystick is pressed.

Requirements:
    - Raspberry Pi with Sense HAT attached
    - sense-hat library: sudo apt install sense-hat
    - requests library: pip install requests

Usage:
    python 02_sensehat_joystick.py

Controls:
    - Press joystick (middle button): Send current reading to API
    - Ctrl+C: Exit the program
"""

import requests
from sense_hat import SenseHat

# API Configuration
API_URL = "http://192.168.1.100:8000"  # Change to your server's IP address
DEVICE_ID = "raspberry-pi-01"

# Initialize Sense HAT
sense = SenseHat()

def get_sensor_data():
    """Read temperature and humidity from Sense HAT."""
    temperature = sense.get_temperature()
    humidity = sense.get_humidity()

    # Optional: Compensate for CPU heat (Sense HAT reads slightly high)
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
        response = requests.post(endpoint, json=data)

        if response.status_code == 201:
            # Show green on LED matrix for success
            sense.clear(0, 255, 0)
            print(f"Sent: {temperature}°C, {humidity}% - OK")
            return True
        else:
            # Show red on LED matrix for error
            sense.clear(255, 0, 0)
            print(f"Error: {response.status_code}")
            return False

    except requests.exceptions.ConnectionError:
        # Show red on LED matrix for connection error
        sense.clear(255, 0, 0)
        print(f"Connection failed to {API_URL}")
        return False

def display_reading(temperature, humidity):
    """Display current reading on the LED matrix."""
    # Clear and show blue to indicate ready state
    sense.clear(0, 0, 50)
    # You could also scroll the values:
    # sense.show_message(f"{temperature}C", scroll_speed=0.05)

def main():
    print("=" * 50)
    print("Sense HAT IoT Client")
    print("=" * 50)
    print(f"API Server: {API_URL}")
    print(f"Device ID: {DEVICE_ID}")
    print()
    print("Press the joystick to send a reading.")
    print("Press Ctrl+C to exit.")
    print("=" * 50)

    # Show blue to indicate ready
    sense.clear(0, 0, 50)

    try:
        while True:
            # Wait for joystick event
            event = sense.stick.wait_for_event()

            # Only trigger on button press (not release)
            if event.action == "pressed" and event.direction == "middle":
                # Read sensor data
                temperature, humidity = get_sensor_data()
                print(f"\nReading: {temperature}°C, {humidity}%")

                # Send to API
                send_measurement(temperature, humidity)

                # Brief pause then return to ready state
                import time
                time.sleep(0.5)
                sense.clear(0, 0, 50)

    except KeyboardInterrupt:
        print("\n\nExiting...")
        sense.clear()

if __name__ == "__main__":
    main()

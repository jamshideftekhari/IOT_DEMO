"""
Script 1: Send Fake Measurement to API
======================================
This script demonstrates how to send temperature and humidity
data to the IoT API using Python requests library.

Run this script to test your API connection before using real sensors.

Usage:
    python 01_fake_measurement.py
"""

import requests

# API Configuration
API_URL = "http://192.168.1.100:8080"  # Change to your server's IP address
DEVICE_ID = "raspberry-pi-01"

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
            print("Measurement sent successfully!")
            print(f"Response: {response.json()}")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)

    except requests.exceptions.ConnectionError:
        print(f"Could not connect to API at {API_URL}")
        print("Make sure the server is running and the IP address is correct.")

def main():
    # Fake measurement data
    fake_temperature = 22.5  # degrees Celsius
    fake_humidity = 55.0     # percentage

    print(f"Sending fake measurement to {API_URL}")
    print(f"  Device ID: {DEVICE_ID}")
    print(f"  Temperature: {fake_temperature}°C")
    print(f"  Humidity: {fake_humidity}%")
    print()

    send_measurement(fake_temperature, fake_humidity)

if __name__ == "__main__":
    main()

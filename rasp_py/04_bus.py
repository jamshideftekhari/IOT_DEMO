"""
Script 4: City Bus Simulation on Sense HAT
==========================================
This script simulates city buses on their routes. Every 4 seconds a
random bus is picked and a random number of passengers (1-40) is
generated. The result is shown on the Sense HAT LED matrix as a bus
icon followed by a rolling text with the bus number and passenger count.

Requirements:
    - Raspberry Pi with Sense HAT attached
    - sense-hat library: sudo apt install sense-hat

Usage:
    python 04_bus.py

Controls:
    - Ctrl+C: Exit the program
"""

import random
import time
from sense_hat import SenseHat

# Simulation settings
INTERVAL = 4             # seconds between each update
MIN_PASSENGERS = 1
MAX_PASSENGERS = 40
BUS_LINES = ["5C", "4A", "350S", "1A", "2A", "6A", "9A", "250S"]

# Initialize Sense HAT
sense = SenseHat()

# Colors
Y = (255, 200, 0)    # bus body (yellow)
W = (150, 220, 255)  # windows (light blue)
B = (60, 60, 60)     # wheels (dark grey)
O = (0, 0, 0)        # off

# 8x8 bus icon
BUS_ICON = [
    O, O, O, O, O, O, O, O,
    Y, Y, Y, Y, Y, Y, Y, O,
    Y, W, Y, W, Y, W, Y, Y,
    Y, W, Y, W, Y, W, Y, Y,
    Y, Y, Y, Y, Y, Y, Y, Y,
    Y, Y, Y, Y, Y, Y, Y, Y,
    O, B, B, O, O, B, B, O,
    O, O, O, O, O, O, O, O,
]


def get_passenger_color(passengers):
    """Green = few passengers, yellow = medium, red = almost full."""
    if passengers <= 15:
        return (0, 255, 0)
    elif passengers <= 30:
        return (255, 255, 0)
    else:
        return (255, 0, 0)


def generate_bus_data():
    """Generate fake data for a random bus."""
    bus_number = random.choice(BUS_LINES)
    passengers = random.randint(MIN_PASSENGERS, MAX_PASSENGERS)
    return bus_number, passengers


def show_bus(bus_number, passengers):
    """Show bus icon followed by rolling text on the LED matrix."""
    sense.set_pixels(BUS_ICON)
    time.sleep(1)

    message = f"Bus {bus_number}: {passengers} pas."
    sense.show_message(message,
                       scroll_speed=0.06,
                       text_colour=get_passenger_color(passengers))

    sense.set_pixels(BUS_ICON)


def main():
    print("City bus simulation started")
    print(f"  Bus lines: {', '.join(BUS_LINES)}")
    print(f"  Interval: {INTERVAL} seconds")
    print("Press Ctrl+C to exit")
    print()

    try:
        while True:
            bus_number, passengers = generate_bus_data()
            print(f"Bus {bus_number}: {passengers} passengers")

            show_bus(bus_number, passengers)
            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\nSimulation stopped")
        sense.clear()


if __name__ == "__main__":
    main()

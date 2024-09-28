# -*- coding: utf-8 -
import sys
import os
import time
import board
import adafruit_scd4x
import mysql.connector
from mysql.connector import Error

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from DFRobot_MultiGasSensor import *

# Initialize I2C for all sensors (shared between SCD4x and DFRobot sensors)
i2c = board.I2C()  # This will use the default SCL and SDA pins on the Raspberry Pi

# Initialize SCD4x (CO2, humidity, temperature sensor) at address 0x62 (default for SCD4x)
scd4x = adafruit_scd4x.SCD4X(i2c)
print("SCD4x Serial number:", [hex(i) for i in scd4x.serial_number])
scd4x.start_periodic_measurement()

# Initialize DFRobot MultiGas Sensors
I2C_ADDRESS_1 = 0x74  # Sensor 1 (at address 0x74)
I2C_ADDRESS_2 = 0x76  # Sensor 2 (at address 0x76)
gas1 = DFRobot_MultiGasSensor_I2C(1, I2C_ADDRESS_1)  # Use i2c1 for the DFRobot sensor
gas2 = DFRobot_MultiGasSensor_I2C(1, I2C_ADDRESS_2)  # Use i2c1 for the DFRobot sensor

# Database connection setup
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="AMIGO",
            password="123",
            database="Gas_Sensors"
        )
        if connection.is_connected():
            print("Connected to MariaDB server")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to insert sensor data into the database
def insert_sensor_data(connection, methane, o2, co2, so2, humidity, temp):
    cursor = connection.cursor()
    query = """INSERT INTO sensor_data (timestamp, Methane, O2, CO2, SO2, Humidity, Temp)
               VALUES (NOW(), %s, %s, %s, %s, %s, %s)"""
    cursor.execute(query, (methane, o2, co2, so2, humidity, temp))
    connection.commit()

# Setup function for the DFRobot MultiGas Sensors
def setup_sensor(gas, address):
    while not gas.change_acquire_mode(gas.PASSIVITY):
        print(f"Waiting for acquire mode change for sensor at {hex(address)}")
        time.sleep(1)
    print(f"Sensor at {hex(address)} acquire mode change success!")
    gas.set_temp_compensation(gas.ON)
    time.sleep(1)

# Read gas concentration from the DFRobot sensor
def read_gas(gas, address):
    return gas.read_gas_concentration()

# Setup both DFRobot gas sensors
def setup():
    setup_sensor(gas1, I2C_ADDRESS_1)
    setup_sensor(gas2, I2C_ADDRESS_2)

# Loop to read data from all sensors and insert into MariaDB
def loop(connection):
    # Read data from DFRobot gas sensors
    methane = read_gas(gas1, I2C_ADDRESS_1)
    o2 = read_gas(gas2, I2C_ADDRESS_2)

    # Check if SCD4x data is ready and read it
    if scd4x.data_ready:
        co2 = scd4x.CO2
        temp = scd4x.temperature
        humidity = scd4x.relative_humidity
        so2 = 0  # Placeholder, replace with actual SO2 reading if available

        # Print data to the console
        print(f"CO2: {co2} ppm")
        print(f"Temperature: {temp:.1f} °C")
        print(f"Humidity: {humidity:.1f} %")
        print(f"Methane: {methane} ppm")
        print(f"O2: {o2} ppm")

        # Insert the data into the database
        insert_sensor_data(connection, methane, o2, co2, so2, humidity, temp)

    time.sleep(1)

# Main function
if __name__ == "__main__":
    setup()
    connection = create_connection()
    if connection:
        try:
            while True:
                loop(connection)
        finally:
            connection.close()

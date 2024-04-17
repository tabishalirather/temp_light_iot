import paho.mqtt.client as mqtt
import mysql.connector
from mysql.connector import Error
import time

# Database configuration
db_config = {
    'user': 'admin',
    'password': 'root',
    'host': 'localhost',
    'database': 'temp_db',
    'raise_on_warnings': True
}

# MQTT configuration
mqtt_server = "192.168.113.148"  # Replace with your MQTT broker IP
mqtt_port = 1883
mqtt_topic = "fan/control"

# Temperature threshold for turning the fan on (in Celsius)
fan_on_threshold = 23.0

# Connect to the database
try:
    db_conn = mysql.connector.connect(**db_config)
    cursor = db_conn.cursor()
    print("Successfully connected to the database.")
except Error as e:
    print(f"Error connecting to the database: {e}")
    exit(1)

# MQTT client setup
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(mqtt_server, mqtt_port, 60)
# Function to check temperature and control fan
def check_temperature_and_control_fan(db_config):
    try:
        # Connect to the database inside the function
        with mysql.connector.connect(**db_config) as db_conn:
            with db_conn.cursor() as cursor:
                # Retrieve the latest temperature reading from the database
                cursor.execute("SELECT temperature FROM temp_reads ORDER BY timestamp DESC LIMIT 1")
                latest_temperature = cursor.fetchone()[0]
                print(f"Latest temp from db is: {latest_temperature}")
                # Check if the temperature exceeds the threshold
                if latest_temperature > fan_on_threshold:
                    # Send a message to turn the fan on
                    client.publish(mqtt_topic, "ON")
                    print("Fan turned ON")
                else:
                    # Send a message to turn the fan off
                    client.publish(mqtt_topic, "OFF")
                    print("Fan turned OFF")
    except Error as e:
        print(f"Error retrieving temperature data from database: {e}")

# Main loop to continuously monitor temperature and control fan
try:
    while True:
        check_temperature_and_control_fan(db_config)
        time.sleep(2)  # Check temperature every 2 seconds
except KeyboardInterrupt:
    # Handle keyboard interrupt to gracefully exit
    client.disconnect()
    print("\nScript terminated by user.")

except KeyboardInterrupt:
    # Handle keyboard interrupt to gracefully exit
    cursor.close()
    db_conn.close()
    client.disconnect()
    print("\nScript terminated by user.")

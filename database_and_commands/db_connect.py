import paho.mqtt.client as mqtt
import mysql.connector
from mysql.connector import Error
from datetime import datetime

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
mqtt_topic = "sensor/temperature"

# Connect to the database
try:
    db_conn = mysql.connector.connect(**db_config)
    cursor = db_conn.cursor()
    print("Successfully connected to the database.")

    # create_table_query = """
#         CREATE TABLE IF NOT EXISTS temp_reads (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             timestamp DATETIME,
#             temperature FLOAT
#         )
#     """
#     cursor.execute(create_table_query)
#     db_conn.commit()
except Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    exit(1)

# MQTT callbacks
def on_connect(client, userdata, flags, rc, properties):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    temperature = float(msg.payload.decode())
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"Temperature received: {temperature} °C")
    try:
        cursor.execute("INSERT INTO temp_reads (timestamp, temperature) VALUES (%s, %s)", (timestamp, temperature))
        db_conn.commit()
        print(f"Successfully inserted temperature {temperature} and timestamp {timestamp} into database.")
    except Error as e:
        print(f"Error inserting temperature data: {e}")

# Create and configure MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)  # Provide a unique client ID here
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_server, mqtt_port, 60)

# Start the MQTT client
client.loop_forever()

# Close the database connection when done
cursor.close()
db_conn.close()
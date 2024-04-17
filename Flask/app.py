from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as mqtt
import mysql.connector
from mysql.connector import Error
import datetime

app = Flask(__name__)

# Database configuration
db_config = {
    'user': 'admin',
    'password': 'root',
    'host': 'localhost',
    'database': 'temp_db'
}

# MQTT Configuration
mqtt_server = "192.168.113.148"
mqtt_port = 1883
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

def connect_mqtt():
    mqtt_client.connect(mqtt_server, mqtt_port, 60)
    mqtt_client.loop_start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/temp')
def temp():
	return render_template('temp.html')


@app.route('/get-light-data', methods=['GET'])
def get_light_data():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, light_value FROM light_reads ORDER BY timestamp DESC LIMIT 10")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(rows)
    except Error as e:
        print(f"Database Error: {e}")
        return str(e)
        
@app.route('/hourly-light-data')
def hourly_light_data():
    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Query to fetch hourly light data
        query = """SELECT AVG(light_value) AS average_light, 
				DATE_FORMAT(timestamp, '%Y-%m-%d %H:00:00') AS date_hour
				FROM light_reads
				WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
				GROUP BY DATE_FORMAT(timestamp, '%Y-%m-%d %H:00:00')
				ORDER BY timestamp;"""

        cursor.execute(query)
        rows = cursor.fetchall()
		
        # Convert the result into a list of dictionaries
        #hourly_light_data = [{'timestamp': row[0].strftime('%Y-%m-%d %H:%M:%S'), #'light_value': row[1]} for row in rows]
        hourly_light_data = [{'timestamp': datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S'), 'light_value': row[0]} for row in rows]


        return jsonify(hourly_light_data)
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        # Close the database connection
        cursor.close()
        connection.close()





@app.route('/control-led', methods=['POST'])
def control_led():
    led_state = request.form.get('led_state')
    if led_state == 'ON':
        mqtt_client.publish("light/control", "TurnLedON")
    else:
        mqtt_client.publish("light/control", "TurnLedOFF")
    return jsonify({"status": "Success", "message": "LED state changed to " + led_state})
    
@app.route('/get-temperature-data', methods=['GET'])
def get_temperature_data():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, temperature FROM temp_reads ORDER BY timestamp DESC LIMIT 10")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(rows)
    except Error as e:
        print(f"Database Error: {e}")
        return str(e)

@app.route('/hourly-temperature-data')
def hourly_temperature_data():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = """SELECT AVG(temperature) AS average_temperature,
                DATE_FORMAT(timestamp, '%Y-%m-%d %H:00:00') AS date_hour
                FROM temp_reads
                WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
                GROUP BY DATE_FORMAT(timestamp, '%Y-%m-%d %H:00:00')
                ORDER BY timestamp;"""
        cursor.execute(query)
        rows = cursor.fetchall()
        hourly_temperature_data = [{'timestamp': 
			datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S'), 
			'temperature': row[0]} for row in rows]
        return jsonify(hourly_temperature_data)
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        cursor.close()
        connection.close()


if __name__ == '__main__':
    connect_mqtt()
    app.run(debug=True, host='0.0.0.0', port = 5000)

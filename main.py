from flask import Flask, redirect, url_for, request, render_template
import paho.mqtt.client as mqtt
import time
from flask_socketio import SocketIO
import cv2

app = Flask(__name__)

# Create a Flask-SocketIO instance
socketio = SocketIO(app)

# Create a MQTT client
client = mqtt.Client()

# Connect to the MQTT broker
client.connect("100.112.18.97", 1883, 60)

client.subscribe("/state/spindleFan")


# Define a callback function for when an MQTT message is received
def on_message(client, userdata, message):
    socketio.emit('state', message.payload.decode('utf-8'))

# Set the callback function
client.on_message = on_message


@socketio.on('fan_button/pressed')
def handle_button_pressed():
    client.publish('ctl/spindleFanButton', 'TOGGLE')


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/control')
def control():
    return render_template('control.html')

@app.route('/status')
def status():
    return render_template('status.html')

@app.route('/cameras')
def cameras():
    return render_template('camera.html')


if __name__ == '__main__':
    # Start the MQTT client
    client.loop_start()

    # Run the Flask-SocketIO server
    socketio.run(app, host='0.0.0.0', debug=False, allow_unsafe_werkzeug=True)

